from PyQt6.QtCore import QThread, pyqtSignal
import testKokoro


class SpeakWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, text, voice=testKokoro.DEFAULT_VOICE, speed=1.0):
        super().__init__()
        self.text = text
        self.voice = voice
        self.speed = speed

    def run(self):
        try:
            testKokoro.speak(self.text, voice=self.voice, speed=self.speed)
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.finished.emit()

    def stop(self):
        testKokoro.stop()
