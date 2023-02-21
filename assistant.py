import whisper
import os
from pathlib import Path
from ChatGPT_API.build.lib.revChatGPT.V1 import Chatbot

from auth import auth_config

import warnings
warnings.filterwarnings("ignore")

recordings_savedir = r'./input_sounds'
recordings_format = '.wav'
model_size = "large" # Available Models: "tiny", "base", "small", "medium", "large"

print()
print("Recordings Directory:", recordings_savedir)
print("Recordings Format:", recordings_format)
print("Model Size:", model_size)
print()

print("Model is loading...")
model = whisper.load_model(model_size)
print("Model is loaded!\n")

def transcribe(file): # Transcribing audio files
    options = dict(task="transcribe", best_of=5)
    text = model.transcribe(file, **options)["text"]
    return text.strip()

def translate(file): # Translating audio files
    options = dict(task="translate", best_of=5)
    text = model.transcribe(file, **options)["text"]
    return text.strip()

def record_sound():
    print('Recording sound...')
    command_to_record_sound = f"python helpers/record_sound.py --savedir {recordings_savedir} --format {recordings_format}"

    try:
        os.system(command_to_record_sound)
    except KeyboardInterrupt:
        pass

    print()
    recording_path = sorted([str(item) for item in list(Path(recordings_savedir).glob(f"**/*{recordings_format}"))])[-1]

    return recording_path

def transcribe_and_translate(recording_path):

    print('Processing file:', recording_path)
    print("Transcribing the recording...")
    recording_transcription = transcribe(recording_path)
    print("Translating the recording...")
    recording_translation = translate(recording_path)
    print()

    print('Results:')
    print("Turkish:\n", recording_transcription, "\n")
    print("English:\n", recording_translation, "\n")

    return recording_transcription, recording_translation

def ChatGPT_Response(prompt):
    print('Getting ChatGPT Results...\n')
    chatbot = Chatbot(config=auth_config)
    response = ""

    for data in chatbot.ask(prompt):
        response = data["message"]
    
    return response

def base():
    recording_path = record_sound()
    recording_transcription, recording_translation = transcribe_and_translate(recording_path)
    response = ChatGPT_Response(recording_transcription)
    print("ChatGPT Answer:\n", response)


if __name__ == "__main__":
    base()