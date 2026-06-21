from PyQt6.QtCore import QThread, pyqtSignal
import testKokoro


class SpeakWorker(QThread):
    ready = pyqtSignal()    # fires once audio is generated, BEFORE playback
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, text, voice=testKokoro.DEFAULT_VOICE, speed=1.0):
        super().__init__()
        self.text = text
        self.voice = voice
        self.speed = speed

    def run(self):
        try:
            # Phase 1: convert text -> audio (slow). Tell the UI to hide the overlay.
            samples, sample_rate = testKokoro.generate(
                self.text, voice=self.voice, speed=self.speed
            )
            self.ready.emit()

            # Phase 2: play the audio. Only emit finished after playback ends
            # (or the user hits Stop).
            testKokoro.play(samples, sample_rate)
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.finished.emit()

    def stop(self):
        testKokoro.stop()
