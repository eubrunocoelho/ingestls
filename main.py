import sys
from PyQt6.QtWidgets import QApplication

from app.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    # Estilos
    app.setStyleSheet(open("styles/styles.qss").read())

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
