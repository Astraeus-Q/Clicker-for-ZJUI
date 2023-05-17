from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QIcon
from PyQt5.QtCore import QTimer, QThread
from PyQt5 import uic

import sys
import threading
import time
import matplotlib.pyplot as plt

import course_section_UI as cs
import answer_hist_UI as ah
import Clicker_backend as cbd
import Clicker_DB_manager as dbm
import help


class Answer_section(QMainWindow):
    def __init__(self, course_name: str, course_idx: str, user = "admin"):
        super().__init__()
        self.ui = uic.loadUi('UI/answer_section.ui')
        # Add pictures
        p_bar = QPixmap("UI/Galaxy1.png")
        scared_bar = p_bar.scaled(1080, 180)
        self.ui.label_7.setMaximumSize(8100, 1000)
        self.ui.label_7.setPixmap(scared_bar)

        self.course_name = course_name
        self.course_idx = course_idx
        self.user = user
        
        self.ui.setWindowTitle("%s: %s" % (self.user,course_name))
        self.ui.lineEdit.setEchoMode(QLineEdit.Password) # Hide the password digit.
        self.first = 0 # Avoid Repeat USB Initialization

        self.course_path = "JSON_Base/%s/%s/" % (self.user, self.course_name)
        self.a_db_path = self.course_path + ("%s.json" % self.course_idx)
        self.update_question_idx()

        # -----Buttons-----
        # Button: Start
        self.ui.pushButton.clicked.connect(self.start_ans)
        # Button: Interrupt
        self.ui.pushButton_2.clicked.connect(self.end_ans)
        # Button: Extend
        self.ui.pushButton_9.clicked.connect(self.ext_ans)
        # Button: Result
        self.ui.pushButton_4.clicked.connect(self.detail)
        # Button: History
        self.ui.pushButton_3.clicked.connect(self.history)
        # Button: Attandance
        self.ui.pushButton_6.clicked.connect(self.attendance)
        # Button: Help
        self.ui.pushButton_8.clicked.connect(self.help)
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

    def update_question_idx(self):
        self.dict_a = dbm.read_DB(self.a_db_path)
        course_idx = 1
        for i in self.dict_a["Question"]:
            course_idx = max(course_idx, int(i)+1)
        self.ui.spinBox_4.setValue(course_idx)

    def start_ans(self):
        if self.first == 0:
            #port = "COM4"
            try:
                cbd.USB_init()
                self.first = 1
            except:
                print(QMessageBox.warning(self, "Oops", "Please insert the Clicker Receiver.", QMessageBox.Yes))
                self.first = 0
                return
        self.t_lim = self.ui.spinBox.value()*60 + self.ui.spinBox_2.value()
        if self.t_lim > 99 * 60 + 59:
            # Maximum time
            print(QMessageBox.warning(self, "Oops", "Error: Time Overflow!!!", QMessageBox.Yes))
            return
        self.ans_time = float(self.t_lim)
        cbd.ans_dict = {}
        cbd.running = 1
        self.correct = self.ui.lineEdit.text()
        self.ques_idx = str(self.ui.spinBox_4.value())
        self.point = str(self.ui.spinBox_3.value())
        
        self.dict_a = dbm.read_DB(self.a_db_path)
        if self.ques_idx in self.dict_a["Question"]:
            # Question exists.
            if QMessageBox.Yes != QMessageBox.information(self, "Confirmation", "This question exists. Continue to start?\n(Record will be covered!)", QMessageBox.Yes, QMessageBox.Cancel):
                return
            

        if self.correct in ['A', 'B', 'C', 'D']:
            self.t_display.start()
        else:
            print(QMessageBox.warning(self, "Oops", "Please Choose a Correct Answer form A, B, C or D.", QMessageBox.Yes))

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
            cbd.update_JSONDB_ans(self.course_path, self.course_idx, self.ques_idx, self.correct, self.point, self.t_lim) # TODO
            self.update_question_idx()
            self.t_display.stop()
        self.timeLock.release()
        return
    
    def plotting(self):
        cbd.plot_answer(cbd.ans_dict, self.correct)
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
        self.t_lim += t_add
        if t_add > 0:
            t_add += 1 # For correct LCDnumber display.
        self.ans_time += t_add
        if self.ans_time >= 10:
            self.ui.lcdNumber.setStyleSheet("color: black")
        self.timeLock.release()
        return
        
    def attendance(self):
        dict_s = dbm.read_DB(self.course_path+"%s.json"%self.course_idx)["Student"]
        tot_stu = 0
        att_stu = 0
        for si in dict_s:
            tot_stu += 1
            if dict_s[si]:
                att_stu += 1
        plt.figure()
        y = [att_stu, tot_stu-att_stu]
        plt.pie(y, labels = ["Present", "Absent"], autopct='%d')
        plt.title("Attendance: %.2f%%" % (100*y[0]/(y[1]+y[0])))
        plt.show()
        

    
    def detail(self):
        global detail
        dict_q = dbm.read_DB(self.a_db_path)["Question"]
        ques_idx = str(self.ui.spinBox_4.value())
        if ques_idx in dict_q:
            detail = ah.Detail_history(self.course_path, self.course_idx, [ques_idx])
            detail.ui.show()
        else:
            print(QMessageBox.information(self, "Oops", "The question has not been answered.", QMessageBox.Yes))
        return
    
    def history(self):
        global hist_ui
        hist_ui = ah.Ans_history("JSON_Base/%s/%s/" % (self.user, self.course_name), self.course_idx)
        hist_ui.ui.show()
        return

    def help(self):
        global help_ui
        help_ui = help.Help()
        help_ui.ui.show()

    def end_course(self):
        global course_ui
        course_ui = cs.Course_section(self.user)
        course_ui.ui.show()
        self.ui.hide()
        return

def t2s(t: int):
    # Transfer the number of second to a formated string "mm:ss".
    return (f"{int(t/60):0>2}:{int(t%60):0>2}")
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Answer_section("ME_200", 1)
    window.ui.show()
    sys.exit(app.exec_())