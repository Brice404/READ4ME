import sys
from PyQt6.QtWidgets import QApplication
from screen import MainWindow
import testKokoro

app = QApplication(sys.argv)
testKokoro.load_model()
window = MainWindow()
window.show()
sys.exit(app.exec())