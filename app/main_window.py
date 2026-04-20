from PyQt6.QtCore import QSize, Qt, QThreadPool
from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QPushButton,
    QLineEdit,
    QTextEdit,
)
from PyQt6.QtGui import QFont

from services.file_service import process_directory
from app.worker import Worker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.threadpool = QThreadPool()

        self._setup_window()
        self._setup_ui()

    def _setup_window(self):
        self.setWindowTitle("Ingestls")
        self.setFixedSize(QSize(1024, 620))

    def _setup_ui(self):
        self.container = QWidget()
        self.setCentralWidget(self.container)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.container.setLayout(self.layout)

        self.top_layout = QHBoxLayout()

        font = QFont("Segoe UI", 12)

        # Input Diretório
        self.input_directory = QLineEdit()
        self.input_directory.setObjectName("inputDirectory")
        self.input_directory.setFixedHeight(60)
        self.input_directory.setFont(font)
        self.input_directory.setPlaceholderText("Diretório...")

        # Botão Ingest
        self.button = QPushButton("Ingest")
        self.button.setObjectName("ingestButton")
        self.button.setFont(font)
        self.button.setFixedHeight(60)
        self.button.setFixedWidth(106)
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)

        # Conexão do botão
        self.button.clicked.connect(self._handle_ingest)

        # Input Ignore
        self.input_ignore = QLineEdit()
        self.input_ignore.setObjectName("inputIgnore")
        self.input_ignore.setFixedHeight(60)
        self.input_ignore.setFont(font)
        self.input_ignore.setPlaceholderText(
            "Ignorar... (Ex: nome_modules, *.md, index.php)"
        )

        self.top_layout.addWidget(self.input_directory)
        self.top_layout.addWidget(self.button)

        # TextArea
        self.text_area = QTextEdit()
        self.text_area.setObjectName("textArea")
        self.text_area.setFont(font)
        self.text_area.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.text_area.setReadOnly(True)

        self.text_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded,
        )
        self.text_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded,
        )

        self.layout.addLayout(self.top_layout)
        self.layout.addWidget(self.input_ignore)
        self.layout.addWidget(self.text_area, stretch=1)

    def _handle_ingest(self):
        path = self.input_directory.text()
        ignore_raw = self.input_ignore.text()

        ignore_patterns = [p.strip() for p in ignore_raw.split(",") if p.strip()]

        if not path:
            self.text_area.setPlainText("Informe um diretório.")
            return

        # UI feedback
        self.text_area.setPlainText("Processando...")
        self.button.setEnabled(False)

        # Cria worker
        worker = Worker(process_directory, path, ignore_patterns)

        # Conecta sinais
        worker.signals.finished.connect(self._on_finished)
        worker.signals.error.connect(self._on_error)

        # Executar no background
        self.threadpool.start(worker)

    def _on_finished(self, result: str):
        self.text_area.setPlainText(result)
        self.button.setEnabled(True)

    def _on_error(self, error: str):
        self.text_area.setPlainText(f"Erro: {error}")
        self.button.setEnabled(True)
