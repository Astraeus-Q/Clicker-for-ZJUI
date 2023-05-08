from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

import sys 

class Course_history(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('UI/Course_hist.ui')

        self.ui.setWindowTitle("Course History")
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Course_history()
    window.ui.show()
    sys.exit(app.exec_())