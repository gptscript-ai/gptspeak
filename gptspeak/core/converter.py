import io
from pathlib import Path
from openai import OpenAI
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from ..utils.api_utils import get_openai_client
from ..exceptions import ConversionError, ConcatenationError
import logging
from ..config.logging_config import setup_logging
import tempfile

setup_logging()

MAX_CHARS = 4096


def split_text(text: str, max_chars: int = MAX_CHARS) -> list[str]:
    chunks = []
    while len(text) > max_chars:
        split_index = max_chars
        while split_index > 0 and text[split_index] not in ("\n", ".", ",", " "):
            split_index -= 1
        if split_index == 0:
            split_index = max_chars
        chunks.append(text[:split_index].strip())
        text = text[split_index:].strip()
    if text:
        chunks.append(text)
    return chunks


def convert_text_chunk_to_speech(
    client: OpenAI, text: str, model: str, voice: str
) -> io.BytesIO:
    try:
        response = client.audio.speech.create(model=model, voice=voice, input=text)
        return io.BytesIO(response.content)
    except Exception as e:
        raise ConversionError(f"Failed to convert text chunk to speech: {str(e)}")


def convert_text_to_speech(input_file: Path, output_file: Path, model: str, voice: str):
    client = get_openai_client()

    try:
        with open(input_file, "r") as file:
            text = file.read()

        if len(text) <= MAX_CHARS:
            # Use the original logic for short texts
            response = client.audio.speech.create(model=model, voice=voice, input=text)
            with open(output_file, "wb") as out:
                for chunk in response.iter_bytes():
                    out.write(chunk)
        else:
            # Use the new chunking logic for longer texts
            convert_long_text_to_speech(text, output_file, model, voice, client)

    except Exception as e:
        raise ConversionError(f"Failed to convert text to speech: {str(e)}")


def convert_long_text_to_speech(
    text: str, output_file: Path, model: str, voice: str, client: OpenAI
):
    chunks = split_text(text)

    logging.info(
        f"Text length exceeds {MAX_CHARS} characters. Splitting into {len(chunks)} chunks for processing."
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_files = []

        for i, chunk in tqdm(
            enumerate(chunks), total=len(chunks), desc="Processing chunks", unit="chunk"
        ):
            audio_data = convert_text_chunk_to_speech(client, chunk, model, voice)
            temp_file = Path(temp_dir) / f"chunk_{i}.mp3"
            with open(temp_file, "wb") as out:
                out.write(audio_data.getvalue())
            temp_files.append(temp_file)

        if len(temp_files) == 1:
            temp_files[0].rename(output_file)
        else:
            logging.info(f"Concatenating {len(temp_files)} audio chunks")
            concatenate_audio_files(temp_files, output_file)

    logging.info(f"Long text conversion completed. Output saved to {output_file}")
    print(f"Long text conversion completed. Output saved to {output_file}")


def convert_text_to_speech_direct(text: str, output_file: Path, model: str, voice: str):
    client = get_openai_client()

    try:
        response = client.audio.speech.create(model=model, voice=voice, input=text)

        with open(output_file, "wb") as out:
            for chunk in response.iter_bytes():
                out.write(chunk)
    except Exception as e:
        raise ConversionError(f"Failed to convert text to speech: {str(e)}")


def convert_text_to_speech_stream(text: str, model: str, voice: str) -> io.BytesIO:
    client = get_openai_client()

    try:
        response = client.audio.speech.create(model=model, voice=voice, input=text)
        audio_data = io.BytesIO(response.content)
        return audio_data
    except Exception as e:
        raise ConversionError(f"Failed to convert text to speech: {str(e)}")


def concatenate_audio_files(
    input_files: list[Path], output_file: Path, chunk_size: int = 1000
):
    """
    Concatenate multiple audio files efficiently.

    :param input_files: List of input audio file paths
    :param output_file: Output audio file path
    :param chunk_size: Number of files to process in each chunk
    """
    try:
        total_files = len(input_files)

        def process_chunk(chunk):
            combined = AudioSegment.empty()
            for file in chunk:
                combined += AudioSegment.from_mp3(file)
            return combined

        with ThreadPoolExecutor() as executor:
            futures = []
            for i in range(0, total_files, chunk_size):
                chunk = input_files[i : i + chunk_size]
                futures.append(executor.submit(process_chunk, chunk))

            final_audio = AudioSegment.empty()
            for future in tqdm(
                as_completed(futures), total=len(futures), desc="Concatenating audio"
            ):
                final_audio += future.result()

        final_audio.export(output_file, format="mp3")
        print(f"Successfully concatenated {total_files} audio files into {output_file}")

    except Exception as e:
        raise ConcatenationError(f"Failed to concatenate audio files: {str(e)}")
