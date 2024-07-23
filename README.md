# TTS to audio converter.

This Python script leverages the ElevenLabs API to create voice dialogues using script parsing. It allows users to generate audio files for skits or dialogues based on a structured script input.

## Features

- Parses custom script format to extract character information and dialogue
- Supports multiple voices using ElevenLabs' text-to-speech API
- Offers two modes of operation:
  - Simple: Creates a single audio file containing the entire skit
  - Advanced: Generates individual audio files for each line of dialogue, organized by character

## Prerequisites

- Python 3.6 or higher
- ElevenLabs API key

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/glowing-radiant/tts to audio converter.git
   cd "tts to audio converter"
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your ElevenLabs API key:
   - Create a `.env` file in the project root
   - Add your API key: `ELEVENLABS_API_KEY=your_api_key_here`

## Usage

1. Run the script:
   ```
   python tts_to_audio.py
   ```

2. Follow the prompts to:
   - generate a txt file with available voices in the working directory.
   - Create a skit
   - Choose between simple and advanced modes
   - Specify the input script file and output directory

### Script Format

Your input script should follow this format:

```
characters {
character1: voice_name1
character2: voice_name2
}

character1: "Dialogue line 1"
character2: "Dialogue line 2"
character1: "Dialogue line 3"
```
the script will ignore the rest of the lines except the ones structured in this format   so you could make additional notes in your script  freely.

## Available Voices

The script will generate a list of available voices from ElevenLabs and save them to `available_voices.txt`. Refer to this file when choosing voices for your characters.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
