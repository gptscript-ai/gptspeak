import subprocess
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio
from pathlib import Path
from tqdm import tqdm
import time
from ..exceptions import PlaybackError


def play_audio(audio_file: Path):
    try:
        audio = AudioSegment.from_file(audio_file, format="mp3")
        duration_ms = len(audio)

        with tqdm(
            total=int(duration_ms / 1000), unit="sec", desc="Playing audio"
        ) as pbar:
            start_time = time.time()

            try:
                playback = _play_with_simpleaudio(audio)
                while playback.is_playing():
                    elapsed_time = int(time.time() - start_time)
                    pbar.update(elapsed_time - pbar.n)
                    time.sleep(0.1)
                pbar.update(int(duration_ms / 1000) - pbar.n)
            except OSError as e:
                if "ALSA" in str(e):
                    print("ALSA playback failed. Attempting to use mpg123...")
                    try:
                        subprocess.run(["mpg123", "-q", str(audio_file)], check=True)
                    except subprocess.CalledProcessError:
                        raise PlaybackError(
                            "Failed to play audio: mpg123 playback failed."
                        )
                    except FileNotFoundError:
                        raise PlaybackError(
                            "Failed to play audio: mpg123 not found. Please install mpg123."
                        )
                else:
                    raise PlaybackError(f"Failed to play audio: {str(e)}")

    except Exception as e:
        raise PlaybackError(f"Failed to play audio: {str(e)}")
