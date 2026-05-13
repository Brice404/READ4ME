import sys 
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget
import testKokoro

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Default settings
        self.setWindowTitle("READ4ME")
        self.setMinimumSize(800, 600)

        #Text field
        self.text_input = QTextEdit(self)
        self.text_input.setPlaceholderText("Paste your text here...")

        #Buttons
        self.play_button = QPushButton("play")
        self.play_button.clicked.connect(self.on_play)

        #Layout
        layout = QVBoxLayout()
        layout.addWidget(self.text_input)
        layout.addWidget(self.play_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def on_play(self):
        text = self.text_input.toPlainText()
        if text.strip():
            testKokoro.speak(text)