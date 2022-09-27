import sys
from pathlib import Path

from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QIcon

from lib import Converter


class MainMenuWindow(QMainWindow, Converter):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(str(Path('media/icon.png').resolve())))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MainMenuWindow()
    myapp.show()
    sys.exit(app.exec())
