import whisper
import os
from pathlib import Path

import warnings
warnings.filterwarnings("ignore")

recordings_savedir = r'./input_sounds'
recordings_format = '.wav'
model_size = "small" # Available Models: "tiny", "base", "small", "medium", "large"

print("Recordings Directory:", recordings_savedir)
print("Recordings Format:", recordings_format)
print("Model Size:", model_size)
print()

print("Model is loading...")
model = whisper.load_model(model_size)
print("Model is loaded!")

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

    last_recording = sorted([str(item) for item in list(Path(recordings_savedir).glob(f"**/*{recordings_format}"))])[-1]
    print('Saved file:', last_recording)
    print()

    return last_recording

def transcribe_and_translate(last_recording):

    print("Transcribing the recording...")
    last_recording_transcribe = transcribe(last_recording)
    print("Translating the recording...")
    last_recording_translate = translate(last_recording)
    print()

    print('Results:')
    print("Turkish:\n", last_recording_transcribe)
    print("English:\n", last_recording_translate)

def base():
    last_recording = record_sound()
    transcribe_and_translate(last_recording)


if __name__ == "__main__":
    base()