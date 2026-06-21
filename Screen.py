from PyQt6.QtWidgets import (
    QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QWidget, QComboBox, QDoubleSpinBox, QLabel, QMessageBox,
)
from worker import GenerateWorker
import testKokoro
from theme import LIGHT_STYLE, DARK_STYLE
from overlay import LoadingOverlay
from playback import AudioPlayer
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QFileDialog
import soundfile as sf


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gen_worker = None

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
        controls.addStretch()

        # --- Playback ---
        self.audio_player = AudioPlayer()
        self.audio_player.finished.connect(self.on_finished)

        # --- Buttons ---
        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.on_convert)

        ICON_SIZE = QSize(24, 24)
        BUTTON_SIZE = QSize(40, 40)

        self.play_pause_button = QPushButton()
        self.play_pause_button.setIcon(QIcon("icons/play.png"))
        self.play_pause_button.setIconSize(ICON_SIZE)
        self.play_pause_button.setFixedSize(BUTTON_SIZE)
        self.play_pause_button.clicked.connect(self.on_play_pause)

        self.stop_button = QPushButton()
        self.stop_button.setIcon(QIcon("icons/stop.png"))
        self.stop_button.setIconSize(ICON_SIZE)
        self.stop_button.setFixedSize(BUTTON_SIZE)
        self.stop_button.clicked.connect(self.on_stop)

        self.restart_button = QPushButton()
        self.restart_button.setIcon(QIcon("icons/restart.png"))
        self.restart_button.setIconSize(ICON_SIZE)
        self.restart_button.setFixedSize(BUTTON_SIZE)
        self.restart_button.clicked.connect(self.on_restart)

        # --- Download ---
        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.on_download)
        self.download_button.setEnabled(False)  # nothing to download yet

        session_row = QHBoxLayout()
        session_row.addWidget(self.convert_button, stretch=1)
        session_row.addWidget(self.download_button, stretch=1)

        # --- Playback Transport ---
        controls.addWidget(self.play_pause_button)
        controls.addWidget(self.stop_button)
        controls.addWidget(self.restart_button)
        controls.addStretch()

        # --- Light/Dark Mode toggle ---
        self.theme_button = QPushButton("🌙 Dark Mode")
        self.theme_button.clicked.connect(self.toggle_theme)
        controls.addWidget(self.theme_button)

        layout = QVBoxLayout()
        layout.addLayout(controls)
        layout.addWidget(self.text_input)
        layout.addLayout(session_row)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # --- Overlay ---
        self.loading_overlay = LoadingOverlay(self)
        self.loading_overlay.setGeometry(self.rect())

        # --- Default theme ---
        self.dark_mode = False
        self.setStyleSheet(LIGHT_STYLE)
        self.loading_overlay.set_dark_mode(self.dark_mode)

        # Default state IDLE (only Convert is usable)
        self.enter_idle_state()

    # --- State machine ---
    #   IDLE       -> nothing converted yet
    #   CONVERTING -> GenerateWorker running, overlay shown
    #   READY      -> audio generated, not playing
    #   PLAYING    -> audio playing
    #   PAUSED     -> audio paused, can resume

    def enter_idle_state(self):
        self.convert_button.setEnabled(True)
        self.download_button.setEnabled(False)
        self.play_pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.restart_button.setEnabled(False)
        self.play_pause_button.setIcon(QIcon("icons/play.png"))

    def enter_converting_state(self):
        self.convert_button.setEnabled(False)
        self.download_button.setEnabled(False)
        self.play_pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.restart_button.setEnabled(False)

    def enter_ready_state(self):
        self.convert_button.setEnabled(True)
        self.download_button.setEnabled(True)
        self.play_pause_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.restart_button.setEnabled(True)
        self.play_pause_button.setIcon(QIcon("icons/play.png"))

    def enter_playing_state(self):
        self.convert_button.setEnabled(False)
        self.download_button.setEnabled(True)
        self.play_pause_button.setEnabled(True)
        self.stop_button.setEnabled(True)
        self.restart_button.setEnabled(True)
        self.play_pause_button.setIcon(QIcon("icons/pause.png"))

    def enter_paused_state(self):
        self.convert_button.setEnabled(True)
        self.download_button.setEnabled(True)
        self.play_pause_button.setEnabled(True)
        self.stop_button.setEnabled(True)
        self.restart_button.setEnabled(True)
        self.play_pause_button.setIcon(QIcon("icons/play.png"))

    # --- Convert flow ---
    def on_convert(self):
        text = self.text_input.toPlainText()
        if not text.strip():
            return

        # Discard anything currently playing before regenerating.
        self.audio_player.stop()
        self.enter_converting_state()
        self.loading_overlay.start()

        voice_id = testKokoro.VOICES[self.voice_combo.currentText()]
        speed = self.speed_spin.value()

        self.gen_worker = GenerateWorker(text, voice=voice_id, speed=speed)
        self.gen_worker.finished.connect(self.on_generated)
        self.gen_worker.error.connect(self.on_error)
        self.gen_worker.start()

    def on_generated(self, samples, sample_rate):
        self.audio_player.load(samples, sample_rate)
        self.loading_overlay.stop()
        self.enter_ready_state()

    def on_error(self, message):
        self.loading_overlay.stop()
        self.enter_idle_state()
        QMessageBox.critical(self, "Error", message)

    # --- Transport ---
    def on_play_pause(self):
        if self.audio_player.is_playing():
            self.audio_player.pause()
            self.enter_paused_state()
        else:
            self.audio_player.play()
            self.enter_playing_state()

    def on_stop(self):
        self.audio_player.stop()
        self.enter_ready_state()

    def on_restart(self):
        self.audio_player.stop()
        self.audio_player.play()
        self.enter_playing_state()

    def on_download(self):
        if not self.audio_player.is_loaded():
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Audio",
            "output.wav",
            "WAV Files (*.wav)"
        )

        if not file_path:
            return

        try:
            sf.write(file_path, self.audio_player.samples, self.audio_player.sample_rate)
            QMessageBox.information(self, "Download", f"Saved to:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Download Failed", str(e))

    def on_finished(self):
        self.audio_player.reset()
        self.enter_ready_state()

    # --- Theme ---
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.setStyleSheet(DARK_STYLE if self.dark_mode else LIGHT_STYLE)
        self.theme_button.setText("☀️ Light Mode" if self.dark_mode else "🌙 Dark Mode")
        self.loading_overlay.set_dark_mode(self.dark_mode)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.loading_overlay.setGeometry(self.rect())
