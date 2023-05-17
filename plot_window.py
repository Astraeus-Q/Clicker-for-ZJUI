from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QIcon
from PyQt5.QtCore import QTimer, QThread
from PyQt5 import uic


class Plot_win(QMainWindow):
    def __init__(self, picture_name, picture_path):
        super().__init__()
        self.ui = uic.loadUi('UI/plot.ui')
        #self.ui.setFixedSize(self.ui.width(), self.ui.height()) # Fixed
        self.ui.setWindowTitle(picture_name)
        picture = QPixmap(picture_path)
        self.ui.label.setPixmap(picture)
