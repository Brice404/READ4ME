from PyQt6.QtWidgets import (
    QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QWidget, QComboBox, QDoubleSpinBox, QLabel, QMessageBox,
)
from worker import SpeakWorker
import testKokoro
from theme import LIGHT_STYLE, DARK_STYLE
from PyQt6.QtWidgets import QProgressBar
from overlay import LoadingOverlay


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = None

        self.setWindowTitle("READ4ME")
        self.setMinimumSize(800, 600)

        self.text_input = QTextEdit(self)
        self.text_input.setPlaceholderText("Paste your text here...")

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)

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
        controls.addStretch()

        # --- Buttons ---
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.on_play)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.on_stop)
        self.stop_button.setEnabled(False)

        button_row = QHBoxLayout()
        button_row.addWidget(self.play_button)
        button_row.addWidget(self.stop_button)

        # --- Light/Dark Mode toggle ---
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

        #--- Overlay ---
        self.loading_overlay = LoadingOverlay(self)
        self.loading_overlay.setGeometry(self.rect())

        # --- Default theme ---
        self.dark_mode = False
        self.setStyleSheet(LIGHT_STYLE)
        self.loading_overlay.set_dark_mode(self.dark_mode)

        # --- Loading bar --- 
        layout.addWidget(self.progress_bar)

    def on_play(self):
        text = self.text_input.toPlainText()
        if not text.strip():
            return

        # Translates name into Kokoro voice id.
        voice_id = testKokoro.VOICES[self.voice_combo.currentText()]
        speed = self.speed_spin.value()

        self.set_playing(True)
        self.worker = SpeakWorker(text, voice=voice_id, speed=speed)
        self.worker.ready.connect(self.on_ready)
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

    def on_ready(self):
        self.loading_overlay.stop()

    def set_playing(self, playing):
        self.play_button.setEnabled(not playing)
        self.stop_button.setEnabled(playing)
        if playing:
            self.loading_overlay.start()
        else:
            self.loading_overlay.stop()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.setStyleSheet(DARK_STYLE if self.dark_mode else LIGHT_STYLE)
        self.theme_button.setText("☀️ Light Mode" if self.dark_mode else "🌙 Dark Mode")
        self.loading_overlay.set_dark_mode(self.dark_mode)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.loading_overlay.setGeometry(self.rect())
