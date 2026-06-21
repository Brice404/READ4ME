from kokoro_onnx import Kokoro
import sounddevice as sd

kokoro = None

# Map of names -> voice ids used by Kokoro.
VOICES = {
    "American Male - Adam": "am_adam",
    "American Male - Michael": "am_michael",
    "American Female - Bella": "af_bella",
    "American Female - Sarah": "af_sarah",
    "British Male - George": "bm_george",
    "British Male - Lewis": "bm_lewis",
    "British Female - Emma": "bf_emma",
    "British Female - Isabella": "bf_isabella",
}

DEFAULT_VOICE = "am_adam"


def load_model():
    global kokoro
    kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")


def speak(text, voice=DEFAULT_VOICE, speed=1.0):
    # Guard against speak() being called before load_model().
    if kokoro is None:
        raise RuntimeError("Model not loaded. Call load_model() first.")

    samples, sample_rate = kokoro.create(text, voice=voice, speed=speed, lang="en-us")
    sd.play(samples, sample_rate)
    sd.wait()


def stop():
    # Interrupts whatever sounddevice is currently playing.
    sd.stop()
