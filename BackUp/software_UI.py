from PyQt5.QtWidgets import *
import sys

# -*- coding: utf-8 -*-
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QLabel, QDesktopWidget, QHBoxLayout, QFormLayout, \
    QPushButton, QLineEdit
from PyQt5 import QtCore, QtGui, QtWidgets

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MainWindow")
        button = QPushButton("New Window", self)
        button.clicked.connect(self.show_child)
        self.user_label = QtWidgets.QLabel(self)
        self.user_label.setGeometry(QtCore.QRect(40, 40, 80, 30))
        # t = threading.Thread(target = self.dynamic_label, args=())
        # t.start()
        self.user_label.setText("User:")
        self.user_label.setObjectName("user_label")

    def dynamic_label(self):
        i = 0
        while True: 
            i += 1
            if i % 10000 == 0:
                self.user_label.setText("%d" % (i/10000))

    def show_child(self):
        self.child_window = Child()
        self.child_window.show()


class Child(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SubWindow")


# MainWindow
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
