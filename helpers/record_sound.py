#!/usr/bin/env python3
"""Create a recording with arbitrary duration.

The soundfile module (https://python-soundfile.readthedocs.io/)
has to be installed!

"""
import argparse
import tempfile
import queue
import os
import sys
from pathlib import Path

import sounddevice as sd
import soundfile as sf
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)

q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

def parse_opt():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        '-l', '--list-devices', action='store_true',
        help='show list of audio devices and exit')
    args, remaining = parser.parse_known_args()
    if args.list_devices:
        print(sd.query_devices())
        parser.exit(0)
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[parser])
    parser.add_argument(
        '--filename', nargs='?', default='input_', metavar='FILENAME',
        help='filename to store recording')
    parser.add_argument(
        '--savedir', type=str, default=r'./input_sounds', help='file directory to save')
    parser.add_argument(
        '--format', type=str, default='.wav', help='file format to save')
    parser.add_argument(
        '-d', '--device', type=int_or_str,
        help='input device (numeric ID or substring)')
    parser.add_argument(
        '-r', '--samplerate', type=int, default=48000, help='sampling rate')
    parser.add_argument(
        '-c', '--channels', type=int, default=1, help='number of input channels')
    parser.add_argument(
        '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
    args = parser.parse_args(remaining)
    return args, parser

def preprocessing(args):

    savedir = args.savedir
    filename = args.filename
    file_format = args.format

    CHECK_FOLDER = os.path.isdir(savedir) 
    if not CHECK_FOLDER:
        os.makedirs(savedir)

    try:
        file_number = max([int(str(item.name[len(filename):-len(file_format)])) for item in list(Path(savedir).glob(f"**/*{file_format}"))]) # This function grabs "3" as integer if files have name like input_0.wav, input_1.wav, input_2.wav, input_3.wav
        file_number += 1
    except ValueError:
        file_number = 0

    filepath = savedir + '//' + filename + str(file_number) + file_format

    return filepath

def recording(args, parser, filepath):
    samplerate = args.samplerate
    device = args.device
    channels = args.channels
    subtype = args.subtype
    file_format = args.format
    
    try:
        if samplerate is None:
            device_info = sd.query_devices(device, 'input')
            # soundfile expects an int, sounddevice provides a float:
            samplerate = int(device_info['default_samplerate'])
        if filepath is None:
            filepath = tempfile.mktemp(prefix='delme_rec_unlimited_',
                                            suffix=file_format, dir='')
            # print(type(filepath))
            # print(filepath)

        # Make sure the file is opened before recording anything:
        with sf.SoundFile(filepath, mode='x', samplerate=samplerate,
                        channels=channels, subtype=subtype) as file:
            with sd.InputStream(samplerate=samplerate, device=device,
                                channels=channels, callback=callback):
                print('#' * 80)
                print('press Ctrl+C to stop the recording')
                print('#' * 80)
                while True:
                    file.write(q.get())
    except KeyboardInterrupt:
        print('\nRecording finished: ' + repr(filepath))
        parser.exit(0)
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))

if __name__ == "__main__":
    args, parser = parse_opt()
    filepath = preprocessing(args)
    recording(args, parser, filepath)