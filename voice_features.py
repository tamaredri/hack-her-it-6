from typing import TYPE_CHECKING, Optional, Tuple, Union
import torch
import pyaudio
import wave
import winsound
from whisper import load_model
from whisper import transcribe
import pyttsx3
import time
if TYPE_CHECKING:
    from whisper.model import Whisper
model_name = "base"
device = "cuda" if torch.cuda.is_available() else "cpu"
model_dir = None
model = load_model(model_name, device=device, download_root=model_dir)


def record(path, durtion):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = durtion
    OUTPUT_FILE = path

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    winsound.Beep(1700,500)

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


def trascribeSTT(audio_path):
    temperature = (0.0, 0.2, 0.4, 0.6000000000000001, 0.8, 1.0)
    args = {'verbose': True, 'task': 'transcribe', 'language': 'English', 'best_of': 5, 'beam_size': 5,
            'patience': None,
            'length_penalty': None, 'suppress_tokens': '-1', 'initial_prompt': None, 'condition_on_previous_text': True,
            'fp16': True, 'compression_ratio_threshold': 2.4, 'logprob_threshold': -1.0, 'no_speech_threshold': 0.6,
            'word_timestamps': False, 'prepend_punctuations': '"\'“¿([{-', 'append_punctuations': '"\'.。,，!！?？:：”)]}、'}
    return transcribe(model, audio_path, temperature=temperature, **args)["text"]


def listen(DURATION=2):
    record("output.wav", DURATION)
    text = trascribeSTT("output.wav")
    return text




def speak(text):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 130)
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.1)
