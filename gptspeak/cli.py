import click
from pathlib import Path
from io import BytesIO
from .core.converter import (
    convert_text_to_speech,
    convert_text_to_speech_direct,
    convert_text_to_speech_stream,
    concatenate_audio_files,
)
from .core.player import play_audio
from .utils.file_utils import validate_input_file, validate_output_file
from .config.logging_config import setup_logging
import logging
import tempfile
from .utils.api_utils import (
    get_api_key,
    save_config,
    get_config,
    interactive_configure,
    validate_model,
    validate_voice,
    VALID_MODELS,
    VALID_VOICES,
)
from .exceptions import APIConfigError, PlaybackError


@click.command(
    context_settings=dict(ignore_unknown_options=True, allow_extra_args=True)
)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def cli(ctx, args):
    """GPTSpeak: Convert text to speech and play audio files."""
    setup_logging()

    try:
        api_key = get_api_key()
    except APIConfigError as e:
        click.echo(str(e), err=True)
        ctx.exit(1)

    if not args or args[0] in ["convert", "play", "concat", "configure"]:
        # If no arguments or a subcommand is provided, invoke the group command
        cli_group.main(args=args)
    else:
        # Check if the first argument is a file
        if Path(args[0]).is_file():
            # Treat it as a file conversion
            input_file = args[0]
            output = None
            default_model, default_voice = get_config()
            model = default_model
            voice = default_voice

            i = 1
            while i < len(args):
                if args[i] in ["-o", "--output"] and i + 1 < len(args):
                    output = args[i + 1]
                    i += 2
                elif args[i] in ["-m", "--model"] and i + 1 < len(args):
                    try:
                        model = validate_model(None, None, args[i + 1])
                    except click.BadParameter as e:
                        click.echo(f"Error: {str(e)}", err=True)
                        ctx.exit(1)
                    i += 2
                elif args[i] in ["-v", "--voice"] and i + 1 < len(args):
                    try:
                        voice = validate_voice(None, None, args[i + 1])
                    except click.BadParameter as e:
                        click.echo(f"Error: {str(e)}", err=True)
                        ctx.exit(1)
                    i += 2
                else:
                    click.echo(f"Unexpected argument: {args[i]}", err=True)
                    ctx.exit(1)

            try:
                input_file = validate_input_file(input_file)
                output = validate_output_file(output or "speech.mp3")
                convert_text_to_speech(input_file, output, model, voice)
                click.echo(f"Successfully converted {input_file} to {output}")
            except Exception as e:
                logging.error(f"Error during conversion: {str(e)}")
                click.echo(f"Error: {str(e)}", err=True)
        else:
            # Direct text-to-speech conversion
            output = None
            default_model, default_voice = get_config()
            model = default_model
            voice = default_voice
            text = []

            i = 0
            while i < len(args):
                if args[i] in ["-o", "--output"] and i + 1 < len(args):
                    output = args[i + 1]
                    i += 2
                elif args[i] in ["-m", "--model"] and i + 1 < len(args):
                    try:
                        model = validate_model(None, None, args[i + 1])
                    except click.BadParameter as e:
                        click.echo(f"Error: {str(e)}", err=True)
                        ctx.exit(1)
                    i += 2
                elif args[i] in ["-v", "--voice"] and i + 1 < len(args):
                    try:
                        voice = validate_voice(None, None, args[i + 1])
                    except click.BadParameter as e:
                        click.echo(f"Error: {str(e)}", err=True)
                        ctx.exit(1)
                    i += 2
                else:
                    text.append(args[i])
                    i += 1

            text = " ".join(text)

            try:
                if output:
                    output = validate_output_file(output)
                    convert_text_to_speech_direct(text, Path(output), model, voice)
                    click.echo(f"Successfully converted text to {output}")
                else:
                    click.echo("Converting text to speech...")
                    audio_data = convert_text_to_speech_stream(text, model, voice)
                    with tempfile.NamedTemporaryFile(
                        suffix=".mp3", delete=False
                    ) as temp_file:
                        temp_file.write(audio_data.getvalue())
                        temp_file_path = temp_file.name

                    play_audio(Path(temp_file_path))
                    Path(
                        temp_file_path
                    ).unlink()  # Delete the temporary file after playing
            except PlaybackError as e:
                logging.error(f"Playback error: {str(e)}")
                click.echo(f"Error during audio playback: {str(e)}", err=True)
                click.echo(
                    click.style(
                        "No audio output device was found. Please check your sound settings.",
                        fg="red",
                        bold=True,
                    )
                )
            except Exception as e:
                logging.error(f"Error during conversion or playback: {str(e)}")
                click.echo(f"Error: {str(e)}", err=True)


@click.group()
def cli_group():
    pass


@cli_group.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    default="speech.mp3",
    help="Output audio file path",
)
@click.option("-m", "--model", help="TTS model to use", callback=validate_model)
@click.option("-v", "--voice", help="Voice to use for speech", callback=validate_voice)
def convert(input_file, output, model, voice):
    """Convert a text file to speech."""
    try:
        api_key = get_api_key()
        input_file = validate_input_file(input_file)
        output = validate_output_file(output)
        default_model, default_voice = get_config()
        model = model or default_model
        voice = voice or default_voice
        convert_text_to_speech(input_file, output, model, voice, api_key)
        click.echo(f"Successfully converted {input_file} to {output}")
    except APIConfigError as e:
        click.echo(str(e), err=True)
    except Exception as e:
        logging.error(f"Error during conversion: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)


@cli_group.command()
@click.argument("audio_file", type=click.Path(exists=True))
def play(audio_file):
    """Play an audio file."""
    try:
        play_audio(audio_file)
    except Exception as e:
        logging.error(f"Error during playback: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)


@cli_group.command()
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    default="concatenated.mp3",
    help="Output audio file path",
)
@click.argument("input_files", nargs=-1, type=click.Path(exists=True), required=True)
def concat(output, input_files):
    """Concatenate multiple audio files."""
    try:
        if len(input_files) < 2:
            raise click.UsageError(
                "At least two input files are required for concatenation."
            )

        output = validate_output_file(output)
        input_files = [Path(f) for f in input_files]
        concatenate_audio_files(input_files, output)
    except click.UsageError as e:
        click.echo(f"Error: {str(e)}", err=True)
    except Exception as e:
        logging.error(f"Error during concatenation: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)


@cli_group.command()
@click.option("-m", "--model", help="Set default TTS model", callback=validate_model)
@click.option("-v", "--voice", help="Set default voice", callback=validate_voice)
def configure(model, voice):
    """Configure default settings for GPTSpeak."""
    if model or voice:
        current_model, current_voice = get_config()
        model = model or current_model
        voice = voice or current_voice
        try:
            save_config(model, voice)
            click.echo("Configuration saved successfully.")
        except ValueError as e:
            click.echo(f"Error: {str(e)}", err=True)
    else:
        interactive_configure()


if __name__ == "__main__":
    cli()
