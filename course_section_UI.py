from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QIcon
from PyQt5 import uic
import sys
from time import sleep

import answer_section_UI as aui
import Clicker_UI as cui

class Course_section(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('UI/Course_section.ui')
        # Add pictures
        p_bar = QPixmap("UI/Moon1.jpg")
        scared_bar = p_bar.scaled(810, 180)
        self.ui.label_5.setMaximumSize(8100, 1800)
        self.ui.label_5.setPixmap(scared_bar)
        p_icon = QPixmap("UI/Earth_wb.jpg")
        scared_icon = p_icon.scaled(100, 80)
        self.ui.label.setPixmap(scared_icon)

        self.ui.setWindowTitle("Select Course")
    
        # -----Buttons-----
        # Button: Start Course
        self.ui.pushButton_4.clicked.connect(self.start_course)
        # Button: Logout
        self.ui.pushButton_5.clicked.connect(self.log_out)


    
    def start_course(self):
        if self.ui.comboBox.currentIndex() == 0:
            # User have to select a course from the list in comboBox.
            QMessageBox.information(self, "Oops", "Please select your course ↖（￣︶￣)>　", QMessageBox.Ok)
        else:
            self.ans_section = aui.Answer_section(self.ui.comboBox.currentText() + " : " + str(self.ui.spinBox.value()))
            self.ans_section.ui.show()
            self.ui.hide()


    def log_out(self):
        self.ui.hide()
        dialog = cui.logindialog()
        if dialog.exec_()==QDialog.Accepted:
            self.ui.show()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Course_section()
    window.ui.show()
    sys.exit(app.exec_())
   