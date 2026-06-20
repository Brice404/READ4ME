from kokoro_onnx import Kokoro
import sounddevice as sd

kokoro = None

def load_model():
    global kokoro
    kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")

def speak(text, voice="am_adam", speed=1.0):
    samples, sample_rate = kokoro.create(text, voice=voice, speed=speed,lang="en-us")
    sd.play(samples, sample_rate)
    sd.wait()