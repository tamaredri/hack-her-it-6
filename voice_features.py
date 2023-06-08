import argparse
import os
import warnings
from typing import TYPE_CHECKING, Optional, Tuple, Union
import vlc

import numpy as np
import torch
import tqdm
import pyaudio
import wave
from whisper import load_model

from whisper.audio import (
    FRAMES_PER_SECOND,
    HOP_LENGTH,
    N_FRAMES,
    N_SAMPLES,
    SAMPLE_RATE,
    log_mel_spectrogram,
    pad_or_trim,
)
from whisper.decoding import DecodingOptions, DecodingResult
from whisper.timing import add_word_timestamps
from whisper.tokenizer import LANGUAGES, TO_LANGUAGE_CODE, get_tokenizer
from whisper.utils import (
    exact_div,
    format_timestamp,
    get_writer,
    make_safe,
    optional_float,
    optional_int,
    str2bool,
)

if TYPE_CHECKING:
    from whisper.model import Whisper
model_name = "base"
device ="cuda" if torch.cuda.is_available() else "cpu"
model_dir = None
model = load_model(model_name, device=device, download_root=model_dir)

def record(path):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 2
    OUTPUT_FILE = path

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Recording started...")
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording stopped...")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(OUTPUT_FILE, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
from whisper import transcribe
def trascribeSTT(audio_path):
    temperature = (0.0, 0.2, 0.4, 0.6000000000000001, 0.8, 1.0)
    args = {'verbose': True, 'task': 'transcribe', 'language': 'English', 'best_of': 5, 'beam_size': 5, 'patience': None,
     'length_penalty': None, 'suppress_tokens': '-1', 'initial_prompt': None, 'condition_on_previous_text': True,
     'fp16': True, 'compression_ratio_threshold': 2.4, 'logprob_threshold': -1.0, 'no_speech_threshold': 0.6,
     'word_timestamps': False, 'prepend_punctuations': '"\'“¿([{-', 'append_punctuations': '"\'.。,，!！?？:：”)]}、'}
    return transcribe(model, audio_path, temperature=temperature, **args)["text"]
def get_speech_(DURATION = 3):
    record("output.wav")
    text = trascribeSTT("output.wav")
    return text

import pyttsx3
def speak(text):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 180)
    engine.say(text)
    engine.runAndWait()

