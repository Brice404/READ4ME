import sys
from PyQt6.QtWidgets import QApplication
from screen import MainWindow
import kokoro

app = QApplication(sys.argv)
kokoro.load_model()
window = MainWindow()
window.show()
sys.exit(app.exec())