from PyQt6.QtWidgets import (
    QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QWidget, QComboBox, QDoubleSpinBox, QLabel, QMessageBox,
)
from worker import SpeakWorker
import testKokoro
from theme import LIGHT_STYLE, DARK_STYLE


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = None

        self.setWindowTitle("READ4ME")
        self.setMinimumSize(800, 600)

        self.text_input = QTextEdit(self)
        self.text_input.setPlaceholderText("Paste your text here...")

        # --- Voice picker ---
        self.voice_combo = QComboBox()
        self.voice_combo.addItems(testKokoro.VOICES.keys())

        voice_row = QHBoxLayout()
        voice_row.addWidget(QLabel("Voice:"))
        voice_row.addWidget(self.voice_combo)

        # --- Speed control ---
        self.speed_spin = QDoubleSpinBox()
        self.speed_spin.setRange(0.5, 2.0)
        self.speed_spin.setSingleStep(0.1)
        self.speed_spin.setValue(1.0)

        speed_row = QHBoxLayout()
        speed_row.addWidget(QLabel("Speed:"))
        speed_row.addWidget(self.speed_spin)

        controls = QHBoxLayout()
        controls.addLayout(voice_row)
        controls.addLayout(speed_row)
        controls.addStretch()  # push the theme toggle to the right edge

        # --- Buttons ---
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.on_play)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.on_stop)
        self.stop_button.setEnabled(False)

        button_row = QHBoxLayout()
        button_row.addWidget(self.play_button)
        button_row.addWidget(self.stop_button)

        # --- Light/Dark Mode toggle (same line as voice/speed, right-aligned) ---
        self.theme_button = QPushButton("🌙 Dark Mode")
        self.theme_button.clicked.connect(self.toggle_theme)
        controls.addWidget(self.theme_button)

        layout = QVBoxLayout()
        layout.addLayout(controls)
        layout.addWidget(self.text_input)
        layout.addLayout(button_row)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Apply the default (light) theme.
        self.dark_mode = False
        self.setStyleSheet(LIGHT_STYLE)

    def on_play(self):
        text = self.text_input.toPlainText()
        if not text.strip():
            return

        # Translate name into Kokoro voice id.
        voice_id = testKokoro.VOICES[self.voice_combo.currentText()]
        speed = self.speed_spin.value()

        self.set_playing(True)
        self.worker = SpeakWorker(text, voice=voice_id, speed=speed)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_stop(self):
        if self.worker is not None:
            self.worker.stop()

    def on_error(self, message):
        QMessageBox.critical(self, "Error", message)

    def on_finished(self):
        self.set_playing(False)

    def set_playing(self, playing):
        self.play_button.setEnabled(not playing)
        self.stop_button.setEnabled(playing)

    def toggle_theme(self):
        # Flip the flag, then apply the matching style + button label.
        self.dark_mode = not self.dark_mode
        self.setStyleSheet(DARK_STYLE if self.dark_mode else LIGHT_STYLE)
        self.theme_button.setText("☀️ Light Mode" if self.dark_mode else "🌙 Dark Mode")
