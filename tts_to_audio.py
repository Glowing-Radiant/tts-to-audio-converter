import os
import re
from dotenv import load_dotenv
import uuid

from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

class TTSSkitCreator:
    def __init__(self, api_key):
        self.client = ElevenLabs(api_key=api_key)
        self.voices = {}
        self.load_voices()

    def load_voices(self):
        try:
            response = self.client.voices.get_all()
            for voice in response.voices:
                self.voices[voice.name.lower()] = voice.voice_id
        except Exception as e:
            raise ValueError(f"Failed to load voices. Error: {str(e)}")

    def save_voice_list(self, filename):
        with open(filename, 'w') as f:
            f.write("Available voices:\n")
            for voice_name in self.voices.keys():
                f.write(f"{voice_name}\n")
        print(f"Voice list saved to {filename}")

    def parse_script(self, script_path):
        with open(script_path, 'r', encoding='utf-8')  as file:
            content = file.read()

        characters_match = re.search(r'characters\s*{([^}]*)}', content, re.DOTALL)
        if not characters_match:
            raise ValueError("Characters section not found in the script.")

        characters = {}
        for line in characters_match.group(1).strip().split('\n'):
            if ':' in line:
                char, voice = map(str.strip, line.split(':', 1))
                characters[char.lower()] = voice.lower()

        dialogue = []
        for line in content.split('\n'):
            if ':' in line and not line.strip().startswith('//'):
                char, text = map(str.strip, line.split(':', 1))
                if char.lower() in characters:
                    dialogue.append((char.lower(), text.strip('"')))

        return characters, dialogue

    def create_audio(self, text, voice_name):
        voice_id = self.voices.get(voice_name)
        if not voice_id:
            raise ValueError(f"Voice '{voice_name}' not found. Please choose from available voices.")
        
        try:
            response = self.client.text_to_speech.convert(
                voice_id=voice_id,
                optimize_streaming_latency=0,
                output_format="mp3_44100_128",
                text=text,
                model_id="eleven_monolingual_v1",
                voice_settings=VoiceSettings(
                    stability=0.5,
                    similarity_boost=0.75,
                    style=0.25,
                    use_speaker_boost=True,
                ),
            )
            return response
        except Exception as e:
            raise ValueError(f"Failed to generate audio for '{voice_name}'. Error: {str(e)}")

    def create_simple_skit(self, script_path, output_dir):
        characters, dialogue = self.parse_script(script_path)
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, "skit_audio.mp3")
        with open(output_file, "wb") as f:
            for char, text in dialogue:
                voice = characters[char]
                audio = self.create_audio(text, voice)
                for chunk in audio:
                    if chunk:
                        f.write(chunk)
            
        print(f"Created audio file: {output_file}")

    def create_advanced_skit(self, script_path, output_dir):
        characters, dialogue = self.parse_script(script_path)
        for char in characters:
            os.makedirs(os.path.join(output_dir, char), exist_ok=True)

        char_counters = {char: 1 for char in characters}

        for char, text in dialogue:
            voice = characters[char]
            audio = self.create_audio(text, voice)
            file_name = f"{char}{char_counters[char]}.mp3"
            file_path = os.path.join(output_dir, char, file_name)
            
            with open(file_path, "wb") as f:
                for chunk in audio:
                    if chunk:
                        f.write(chunk)
            
            print(f"Created audio file: {file_path}")
            char_counters[char] += 1

def main():
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        api_key = input("Please enter your ElevenLabs API key: ")
        try:
            set_key(".env", "ELEVENLABS_API_KEY", api_key)
        except:
            print("sorry, couldn't save the key to the environment")
    try:
        creator = TTSSkitCreator(api_key)
    except ValueError as e:
        print(f"Error: {str(e)}")
        return

    # Save voice list to a file
    voice_list_file = "available_voices.txt"
    creator.save_voice_list(voice_list_file)
    print(f"Please check {voice_list_file} for available voices before creating your script.")

    while True:
        choice = input("Enter 1 to create a skit, or 2 to exit: ")
        if choice == '2':
            break
        elif choice == '1':
            script_path = input("Enter the path to your script file: ")
            mode = input("Choose mode (simple/advanced): ").lower()
            output_dir = input("Enter output directory for audio files: ")

            try:
                if mode == 'simple':
                    creator.create_simple_skit(script_path, output_dir)
                elif mode == 'advanced':
                    creator.create_advanced_skit(script_path, output_dir)
                else:
                    print("Invalid mode selected. Please choose 'simple' or 'advanced'.")
            except ValueError as e:
                print(f"Error: {str(e)}")
            except Exception as e:
                print(f"An unexpected error occurred: {str(e)}")
        else:
            print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()

