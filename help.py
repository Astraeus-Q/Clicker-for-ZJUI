from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QIcon
from PyQt5.QtCore import QTimer, QThread
from PyQt5 import uic

import sys

class Help(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('UI/help.ui')
        self.ui.setWindowTitle("Help")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Help()
    window.ui.show()
    sys.exit(app.exec_())