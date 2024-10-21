import io
from pathlib import Path
from openai import OpenAI
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from ..utils.api_utils import get_openai_client
from ..exceptions import ConversionError, ConcatenationError


def convert_text_to_speech(input_file: Path, output_file: Path, model: str, voice: str):
    client = get_openai_client()

    try:
        with open(input_file, "r") as file:
            text = file.read()

        response = client.audio.speech.create(model=model, voice=voice, input=text)

        with open(output_file, "wb") as out:
            for chunk in response.iter_bytes():
                out.write(chunk)
    except Exception as e:
        raise ConversionError(f"Failed to convert text to speech: {str(e)}")


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
