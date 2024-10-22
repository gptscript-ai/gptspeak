# GPTSpeak

GPTSpeak is a tool designed to convert text into high-quality audio files using OpenAI's Text-to-Speech (TTS) API. It can be used both as a command-line interface (CLI) tool and as a Python module. GPTSpeak provides functionality to play the generated audio files directly and concatenate multiple audio files, making it an ideal solution for developers, writers, educators, and content creators who need to transform written content into spoken audio efficiently.

With GPTSpeak, you can:

- Convert text files or direct text input into natural-sounding audio .
- Choose from multiple voices and TTS models to suit your needs.
- Play generated audio files directly from the command line.
- Concatenate multiple audio files into a single file.

It's as simple as:

```bash
gptspeak "Hello, world!"
```

## Features

- **Dual-Use Design**: Use GPTSpeak as a CLI tool for quick operations or as a Python module for integration into larger projects.
- **Convert Text to Speech**: Transform text files or direct text input into high-quality audio files using OpenAI's TTS API.
- **Handle Long Texts**: Automatically split long texts into appropriate chunks and combine the resulting audio, allowing for conversion of texts of any length.
- **Multiple Voice Options**: Choose from a variety of available voices to match the tone of your content.
- **Model Selection**: Select different TTS models based on quality, speed, or other attributes.
- **Audio Playback**: Play generated audio files directly from the command line or within your Python scripts.
- **Audio Concatenation**: Efficiently combine multiple audio files into a single file.
- **Cross-platform Compatibility**: Works on macOS, Linux, and Windows.
- **Customizable Output**: Specify output file paths and formats.
- **Error Handling and Logging**: Robust error detection with informative messages and logging for troubleshooting.

## Table of Contents

- [Installation](#installation)
  - [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Setting Up Environment Variables](#setting-up-environment-variables)
  - [Using GPTSpeak as a Python Package](#using-gptspeak-as-a-python-package)
  - [Using GPTSpeak via the CLI](#using-gptspeak-via-the-cli)
    - [CLI Options](#cli-options)
- [Available Models and Voices](#available-models-and-voices)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Installation

Install GPTSpeak using pip:

```bash
pip install gptspeak
```

### Prerequisites

Ensure you have the following installed:

- Python 3.9 or higher
- ffmpeg (for audio processing)

#### Installing ffmpeg

ffmpeg is required for audio processing. You can check if you already have it installed by running `ffmpeg -version` in your terminal/command prompt.

- **macOS (with Homebrew)**:

  ```bash
  brew install ffmpeg
  ```

- **Ubuntu/Debian**:

  ```bash
  sudo apt-get install ffmpeg
  ```

- **Windows**:
  1. Download the latest ffmpeg build from the [official ffmpeg website](https://ffmpeg.org/download.html).
  2. Extract the downloaded package and move the extracted directory to your desired location.
  3. Add the `bin/` directory from the extracted folder to your system PATH.
  4. Verify the installation by opening a new command prompt and running `ffmpeg -version`.

After installing ffmpeg, you should be ready to use GPTSpeak.

## Quick Start

Here's how you can quickly get started with GPTSpeak:

```bash
# Set your API key
export OPENAI_API_KEY="your-openai-api-key"

# Convert direct text input to audio
gptspeak "Hello, world!" -o hello.mp3

# Play direct text input without saving to a file (turn your audio up) 
gptspeak "Hello, world!" -o hello.mp3

# Convert a text file to audio
gptspeak convert input.txt -o output.mp3

# Play the generated audio file
gptspeak play output.mp3

# Concatenate multiple audio files
gptspeak concat -o combined.mp3 file1.mp3 file2.mp3
```

## Usage

### Setting Up Environment Variables

Before using GPTSpeak, set up the API key for OpenAI by setting the appropriate environment variable:

```bash
export OPENAI_API_KEY="your-openai-api-key"
```

You can set this variable in your shell profile (`~/.bashrc`, `~/.zshrc`, etc.) or include it in your Python script before importing GPTSpeak.

> **Note**: Keep your API key secure and do not expose it in code repositories.

### Using GPTSpeak as a Python Package

Here's an example of how to use GPTSpeak in your Python code:

```python
import os
from pathlib import Path
from gptspeak.core.converter import convert_text_to_speech, convert_text_to_speech_direct
from gptspeak.core.player import play_audio

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# Convert text file to speech
input_file = Path("input.txt")
output_file = Path("output.mp3")
model = "tts-1"
voice = "alloy"

convert_text_to_speech(input_file, output_file, model, voice)
print(f"Audio file created: {output_file}")

# Convert direct text input to speech
text = "Hello, world!"
direct_output_file = Path("hello.mp3")

convert_text_to_speech_direct(text, direct_output_file, model, voice)
print(f"Audio file created: {direct_output_file}")

# Play the generated audio
play_audio(output_file)
```

### Configuring Default Settings

GPTSpeak allows you to configure default settings for the TTS model and voice. You can do this interactively or by specifying the options directly:

```bash
# Interactive configuration
gptspeak configure

# Set default model and voice directly
gptspeak configure -m tts-1-hd -v nova
```

The configuration is saved in `~/.gptspeak.ini` and will be used for future conversions unless overridden by command-line options.

### Using GPTSpeak via the CLI

When using the command-line interface, ensure you've set the appropriate environment variable for the OpenAI API key.

To convert direct text input to audio:

```bash
gptspeak "Hello, world!" -o hello.mp3 -m tts-1 -v alloy
```

To convert a text file to audio:

```bash
gptspeak convert input.txt -o output.mp3 -m tts-1 -v alloy
```

To concatenate multiple audio files:

```bash
gptspeak concat -o combined.mp3 file1.mp3 file2.mp3 file3.mp3
```

To play an audio file:

```bash
gptspeak play output.mp3
```

#### CLI Options

For direct text input and the `convert` command:

- `-o`, `--output`: Output audio file path (default: speech.mp3)
- `-m`, `--model`: TTS model to use (default: tts-1)
- `-v`, `--voice`: Voice to use for speech (default: alloy)

For the `play` command:

- No additional options; just provide the path to the audio file.

For the `concat` command:

- `-o`, `--output`: Output audio file path (default: concatenated.mp3)

For the `configure` command:

- `-m`, `--model`: Set the default TTS model
- `-v`, `--voice`: Set the default voice

## Available Models and Voices

GPTSpeak supports the following models and voices from OpenAI's TTS API:

### Models

- `tts-1`: Standard TTS model
- `tts-1-hd`: High-definition TTS model

### Voices

- `alloy`: Neutral voice
- `echo`: Soft and gentle voice
- `fable`: Expressive and dynamic voice
- `onyx`: Deep and authoritative voice
- `nova`: Warm and friendly voice
- `shimmer`: Clear and energetic voice

To use a specific model and voice, specify them in the command:

```bash
gptspeak "Hello, world!" -o hello.mp3 -m tts-1-hd -v nova
```

## Examples

### Converting Direct Text Input with Custom Voice

```bash
gptspeak "Welcome to GPTSpeak!" -o welcome.mp3 -v fable
```

This command will convert the text "Welcome to GPTSpeak!" into an audio file named `welcome.mp3` using the "fable" voice.

### Converting a Text File with Custom Voice

```bash
gptspeak convert story.txt -o narration.mp3 -v echo
```

This command will convert the content of `story.txt` into an audio file named `narration.mp3` using the "echo" voice.

### Converting a Long Text File

```bash
gptspeak convert long_story.txt -o long_narration.mp3 -v nova
```

This command will convert the content of `long_story.txt` into an audio file named `long_narration.mp3` using the "nova" voice. If the text is longer than the API's character limit, GPTSpeak will automatically split it into chunks, process each chunk separately, and combine the results into a single audio file.

### Concatenating Multiple Audio Files

```bash
gptspeak concat -o full_audiobook.mp3 chapter1.mp3 chapter2.mp3 chapter3.mp3
```

This command will combine `chapter1.mp3`, `chapter2.mp3`, and `chapter3.mp3` into a single audio file named `full_audiobook.mp3`.

### Playing an Audio File

```bash
gptspeak play narration.mp3
```

This command will play the `narration.mp3` file.

## Contributing

Contributions to GPTSpeak are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository on GitHub.
2. Create a new branch for your feature or bugfix.
3. Make your changes and ensure tests pass.
4. Submit a pull request with a clear description of your changes.

Please ensure that your code adheres to the existing style conventions and passes all tests.

## License

GPTSpeak is licensed under the Apache-2.0 License. See [LICENSE](LICENSE) for more information.
