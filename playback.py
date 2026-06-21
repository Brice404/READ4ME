from PyQt6.QtCore import QObject, pyqtSignal
import sounddevice as sd
import numpy as np


class AudioPlayer(QObject):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.stream = None
        self.samples = None
        self.sample_rate = None
        self.position = 0
        self._explicit_stop = False

    # --- Queries ---
    def is_loaded(self):
        return self.samples is not None

    def is_playing(self):
        return self.stream is not None and self.stream.active

    # --- Loading ---
    def load(self, samples, sample_rate):
        self._teardown_stream()
        self.samples = np.asarray(samples, dtype=np.float32)
        self.sample_rate = sample_rate
        self.position = 0

    # --- Stream Cycle ---
    def _make_stream(self):
        return sd.OutputStream(
            samplerate=self.sample_rate,
            channels=1,
            callback=self._callback,
            finished_callback=self._on_stream_finished,
        )

    def _teardown_stream(self):
        if self.stream is not None:
            self._explicit_stop = True
            try:
                self.stream.stop()
                self.stream.close()
            except Exception:
                pass
            self.stream = None

    def _callback(self, outdata, frames, time_info, status):
        remaining = len(self.samples) - self.position
        if remaining <= 0:
            outdata.fill(0)
            raise sd.CallbackStop()
        chunk = min(frames, remaining)
        outdata[:chunk, 0] = self.samples[self.position:self.position + chunk]
        if chunk < frames:
            outdata[chunk:, 0] = 0
        self.position += chunk

    def _on_stream_finished(self):
        if self._explicit_stop:
            self._explicit_stop = False
            return 

        self.stream = None
        self.finished.emit()

    # --- Transport ---
    def play(self):
        if not self.is_loaded():
            return
        if self.position >= len(self.samples):
            self.position = 0
        if self.stream is None:
            self.stream = self._make_stream()
        self._explicit_stop = False
        self.stream.start()

    def pause(self):
        if self.is_playing():
            self._explicit_stop = True
            self.stream.stop()
            # NOTE: stream stays open so play() can resume from position.

    def stop(self):
        # Fully halt and rewind to the start.
        self._teardown_stream()
        self.position = 0

    def reset(self):
        self._teardown_stream()
        self.position = 0
