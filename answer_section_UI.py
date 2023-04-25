from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QIcon
from PyQt5.QtCore import QTimer, QThread
from PyQt5 import uic

import sys
import threading
import time

import course_section_UI as cs
import Clicker_UI as cui
import Clicker_backend as cbd


class Answer_section(QMainWindow):
    def __init__(self, course_name: str):
        super().__init__()
        self.ui = uic.loadUi('UI/answer_section.ui')
        # Add pictures
        p_bar = QPixmap("UI/Galaxy1.png")
        scared_bar = p_bar.scaled(1080, 180)
        self.ui.label_7.setMaximumSize(8100, 1000)
        self.ui.label_7.setPixmap(scared_bar)
        self.ui.setWindowTitle(course_name)

        # -----Buttons-----
        # Button: Start
        self.ui.pushButton.clicked.connect(self.start_ans)
        # Button: End
        self.ui.pushButton_2.clicked.connect(self.end_ans)
         # Button: Extend
        self.ui.pushButton_9.clicked.connect(self.ext_ans)
        # Button: End Course
        self.ui.pushButton_5.clicked.connect(self.end_course)

        # Display
        self.timeLock = threading.Lock()
        self.ans_time = 0
        self.t_display = QTimer(self)
        self.t_display.setInterval(500)
        self.t_display.timeout.connect(self.refresh_and_collect)
        self.ui.lcdNumber.display("00:00")
        self.ui.progressBar.setValue(0)


    def start_ans(self):
        port = "COM4"
        cbd.USB_init(port)
        t_lim = self.ui.spinBox.value()*60 + self.ui.spinBox_2.value()
        self.ans_time = float(t_lim)
        cbd.ans_dict = {}
        self.t_display.start()

    def refresh_and_collect(self):
        # Update time display.
        self.timeLock.acquire()
        # Count down
        self.ui.lcdNumber.display(t2s(int(self.ans_time)))
        progress = int(0 if len(cbd.ans_dict) == 0 else len(cbd.ans_dict) / 4 * 100)
        self.ui.progressBar.setValue(progress)
        self.ans_time -= 0.5
        t = threading.Thread(target = cbd.USB_read)
        t.start()
        if self.ans_time < 10:
            self.ui.lcdNumber.setStyleSheet("color: red")
        if self.ans_time <= 0:
            self.ui.lcdNumber.setStyleSheet("color: black")
            cbd.running = 0
            self.plotting()
            self.t_display.stop()
        self.timeLock.release()
        return
    
    def plotting(self):
        correct = self.ui.lineEdit.text()
        cbd.plot_answer(cbd.ans_dict, correct)
        # cbd.plot_attendance()
        return
    
    def end_ans(self):
        self.ui.lcdNumber.setStyleSheet("color: black")
        self.ui.lcdNumber.display("00:00")
        cbd.running = 0
        self.t_display.stop()
        return

    def ext_ans(self):
        self.timeLock.acquire()
        t_add = self.ui.timeEdit_2.time().minute()*60 + self.ui.timeEdit_2.time().second()
        if t_add > 0:
            t_add += 1
        self.ans_time += t_add
        if self.ans_time >= 10:
            self.ui.lcdNumber.setStyleSheet("color: black")
        self.timeLock.release()
        return
        
    
    def end_course(self):
        # self.course_section = cs.Course_section()
        # self.course_section.ui.show()
        # self.ui.hide()
        return

        

def t2s(t: int):
    # Transfer the number of second to a formated string "mm:ss".
    if t > 99 * 60 + 999:
        # Maximum time
        print("Error: Time Overflow!!!")
        return "00:00"
    return (f"{int(t/60):0>2}:{int(t%60):0>2}")
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Answer_section("TEST")
    window.ui.show()
    sys.exit(app.exec_())