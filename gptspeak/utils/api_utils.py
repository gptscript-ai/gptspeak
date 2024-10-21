import os
from pathlib import Path
import configparser
from openai import OpenAI
from ..exceptions import APIConfigError
import click

VALID_MODELS = ["tts-1", "tts-1-hd"]
VALID_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


def get_api_key():
    # Check environment variable
    env_key = os.environ.get("OPENAI_API_KEY")
    if env_key:
        return env_key

    # Check config file
    config = configparser.ConfigParser()
    config_file = Path.home() / ".gptspeak.ini"
    if config_file.exists():
        config.read(config_file)
        if "DEFAULT" in config and "api_key" in config["DEFAULT"]:
            return config["DEFAULT"]["api_key"]

    # If no key found, raise an exception
    raise APIConfigError(
        "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable "
        "or add it to ~/.gptspeak.ini."
    )


def get_openai_client() -> OpenAI:
    api_key = get_api_key()
    return OpenAI(api_key=api_key)


def validate_model(ctx, param, value):
    if value is not None and value not in VALID_MODELS:
        raise click.BadParameter(
            f"Invalid model. Choose from: {', '.join(VALID_MODELS)}"
        )
    return value


def validate_voice(ctx, param, value):
    if value is not None and value not in VALID_VOICES:
        raise click.BadParameter(
            f"Invalid voice. Choose from: {', '.join(VALID_VOICES)}"
        )
    return value


def save_config(model, voice):
    if model not in VALID_MODELS:
        raise ValueError(f"Invalid model. Choose from: {', '.join(VALID_MODELS)}")
    if voice not in VALID_VOICES:
        raise ValueError(f"Invalid voice. Choose from: {', '.join(VALID_VOICES)}")

    config = configparser.ConfigParser()
    config_file = Path.home() / ".gptspeak.ini"

    if config_file.exists():
        config.read(config_file)

    if "DEFAULT" not in config:
        config["DEFAULT"] = {}

    config["DEFAULT"]["model"] = model
    config["DEFAULT"]["voice"] = voice

    with open(config_file, "w") as f:
        config.write(f)


def get_config():
    config = configparser.ConfigParser()
    config_file = Path.home() / ".gptspeak.ini"

    if config_file.exists():
        config.read(config_file)
        if "DEFAULT" in config:
            model = config["DEFAULT"].get("model", "tts-1")
            voice = config["DEFAULT"].get("voice", "alloy")
            return (
                model if model in VALID_MODELS else "tts-1",
                voice if voice in VALID_VOICES else "alloy",
            )

    return "tts-1", "alloy"


def interactive_configure():
    while True:
        model = click.prompt(
            "Enter default model", default="tts-1", type=click.Choice(VALID_MODELS)
        )
        voice = click.prompt(
            "Enter default voice", default="alloy", type=click.Choice(VALID_VOICES)
        )
        try:
            save_config(model, voice)
            click.echo("Configuration saved successfully.")
            break
        except ValueError as e:
            click.echo(f"Error: {str(e)}")
