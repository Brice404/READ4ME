from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMovie
from resource_path import resource_path


class LoadingOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 150);")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.spinner_label = QLabel()
        self.movie = QMovie(resource_path("icons/loading.gif"))
        self.spinner_label.setMovie(self.movie)
        self.spinner_label.setStyleSheet("background: transparent;")
        layout.addWidget(self.spinner_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.text_label = QLabel("Converting text to speech.\nThis may take a few minutes.")
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label.setStyleSheet("color: white; font-size: 14px; background: transparent;")
        layout.addWidget(self.text_label)

        self.setLayout(layout)
        self.hide()

    def set_dark_mode(self, is_dark):
        color = "white" if is_dark else "black"
        self.text_label.setStyleSheet(f"color: {color}; background: transparent; font-size: 14px;")

    def start(self):
        self.movie.start()
        self.show()
        self.raise_()

    def stop(self):
        self.movie.stop()
        self.hide()