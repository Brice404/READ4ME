from PyQt6.QtCore import QThread, pyqtSignal
import testKokoro

class GenerateWorker(QThread):
    finished = pyqtSignal(object, object)  # samples, sample_rate
    error = pyqtSignal(str)

    def __init__(self, text, voice=testKokoro.DEFAULT_VOICE, speed=1.0):
        super().__init__()
        self.text = text
        self.voice = voice
        self.speed = speed

    def run(self):
        try:
            samples, sample_rate = testKokoro.generate(
                self.text, voice=self.voice, speed=self.speed
            )
            self.finished.emit(samples, sample_rate)
        except Exception as e:
            self.error.emit(str(e))