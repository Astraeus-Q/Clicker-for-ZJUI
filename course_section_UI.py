from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QIcon
from PyQt5 import uic
import sys
from time import sleep
from datetime import date

import answer_section_UI as aui
import Clicker_UI as cui
import Clicker_DB_manager as dbm
import course_hist as ch

class Course_section(QMainWindow):

    def __init__(self, user="admin"):
        super().__init__()
        self.ui = uic.loadUi('UI/Course_section.ui')
        # Add pictures
        p_bar = QPixmap("UI/Moon1.jpg")
        scared_bar = p_bar.scaled(810, 180)
        self.ui.label_5.setMaximumSize(8100, 1800)
        self.ui.label_5.setPixmap(scared_bar)
        p_icon = QPixmap("UI/Earth_wb.jpg")
        scaled_icon = p_icon.scaled(100, 80)
        self.ui.label.setPixmap(scaled_icon)
        self.user = user
        self.ui.setWindowTitle("%s: Select Course" % self.user)

        self.user_path = "JSON_Base/%s/" % self.user
        self.c_db_path = self.user_path + "course.json"

        # Remote db
        #cui.db.change_user(self.user)
        #cui.db.local_update_course()
        dict_c = dbm.read_DB(self.c_db_path)
        self.ui.comboBox.clear()
        self.ui.comboBox.addItems(["Please Select a course"] + list(dict_c.keys())) # Add course selections.
    
        # -----Buttons-----
        # Button: Start Course
        self.ui.pushButton_4.clicked.connect(self.start_course)
        # Button: Logout
        self.ui.pushButton_5.clicked.connect(self.log_out)
        # Select a course.
        self.ui.comboBox.activated.connect(self.update_course_idx)
        # Course NO. Changes.
        self.ui.spinBox.textChanged.connect(self.update_topic)
        # Button: Course History
        self.ui.pushButton_3.clicked.connect(self.course_history)
        


    
    def start_course(self):
        if self.ui.comboBox.currentIndex() == 0:
            # User have to select a course from the list in comboBox.
            QMessageBox.information(self, "Oops", "Please select your course ↖（￣︶￣)>　", QMessageBox.Ok)
        else:
            global ans_ui
            state = self.update_JSONDB_course()
            if state == 0:
                # Cancel
                return
            course_name = self.ui.comboBox.currentText()

            # Remote db
            #cui.db.change_course(course_name)
            #cui.db.local_student_update()
            ans_ui = aui.Answer_section(course_name, str(self.ui.spinBox.value()), self.user)
            ans_ui.ui.show()
            self.ui.hide()


    def log_out(self):
        self.ui.hide()
        dialog = cui.logindialog()
        if dialog.exec_()==QDialog.Accepted:
            #self.ui.show()
            pass

    def update_course_idx(self):
        if self.ui.comboBox.currentIndex() == 0:
            # Course has not been selected.
            return
        course_name = self.ui.comboBox.currentText()
        self.dict_c = dbm.read_DB(self.c_db_path)
        course_idx = 1
        for i in self.dict_c[course_name]:
            course_idx = max(course_idx, int(i)+1)
        self.ui.spinBox.setValue(course_idx)

    def update_topic(self):
        if self.ui.comboBox.currentIndex() == 0:
            # Course has not been selected.
            self.ui.lineEdit.setText("Default Topic") # Set default topic.
            return
        self.dict_c = dbm.read_DB(self.c_db_path)
        course_name = self.ui.comboBox.currentText()
        course_idx = str(self.ui.spinBox.value())
        if course_idx in self.dict_c[course_name]:
            self.ui.lineEdit.setText(self.dict_c[course_name][course_idx][1]) # Set specific topic.
        else:
            self.ui.lineEdit.setText("Default Topic") # Set default topic.



    def update_JSONDB_course(self):
        dict_c = dbm.read_DB(self.c_db_path)
        course_name = self.ui.comboBox.currentText()
        course_idx = str(self.ui.spinBox.value())
        if course_idx in dict_c[course_name]:
            if QMessageBox.Yes != QMessageBox.information(self, "Confirmation", "This course exists. Continue to start?\n(Records might be covered!)", QMessageBox.Yes, QMessageBox.Cancel):
                return 0
        else:
            # Initialize answer JSON database for new class.
            dict_new_a = {"Question":{}, "Student":{}}
            db_stu_path = "%s%s/student.json" % (self.user_path, course_name)
            dict_s = dbm.read_DB(db_stu_path)
            for si in dict_s.values():
                dict_new_a["Student"][si] = {}
            db_path = "%s%s/%s.json" % (self.user_path, course_name, course_idx)
            dbm.write_DB(db_path, dict_new_a)

        today = "%s-%s-%s" % (date.today().year, date.today().month, date.today().day)
        dict_c[course_name][course_idx] = [today, self.ui.lineEdit.text()]
        dbm.write_DB(self.c_db_path, dict_c)
        return 1
    
    def course_history(self):
        global hist_u
        user_path = "JSON_Base/%s/" % self.user
        if self.ui.comboBox.currentIndex() == 0:
            # User have to select a course from the list in comboBox.
            QMessageBox.information(self, "Oops", "Please select your course ↖（￣︶￣)>　", QMessageBox.Ok)
            return  
        #if self.
        course_name = self.ui.comboBox.currentText()

        # Remote db
        #cui.db.change_course(course_name)
        #cui.db.local_student_update()

        hist_u = ch.Course_history(user_path, course_name)
        hist_u.ui.show()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Course_section()
    window.ui.show()
    sys.exit(app.exec_())
   