import os
from pathlib import Path
from gptspeak.core.converter import convert_text_to_speech_stream
from gptspeak.core.player import play_audio
import tempfile

# Set your OpenAI API key
# os.environ["OPENAI_API_KEY"] = "your-openai-api-key-here"

# Your text input
text = "Why don’t skeletons fight each other? ...... [pause]\nBecause they don’t have the guts! [laugh]"

# Set the voice (optional, default is 'alloy')
voice = "nova"

# Set the model (optional, default is 'tts-1')
model = "tts-1"

try:
    print("Converting text to speech...")
    audio_data = convert_text_to_speech_stream(text, model, voice)

    # Save the audio data to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
        temp_file.write(audio_data.getvalue())
        temp_file_path = temp_file.name

    # Play the audio
    play_audio(Path(temp_file_path))

    # Clean up the temporary file
    Path(temp_file_path).unlink()

except Exception as e:
    print(f"Error: {str(e)}")
