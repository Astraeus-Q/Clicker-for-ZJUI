import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
#import qdarkstyle
import base64
import configparser

# Windows
from login_UI import Ui_Form
import course_section_UI as cs

import hashlib

class logindialog(QDialog,Ui_Form):

    is_admin_signal = pyqtSignal()
    is_student_signal = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        super(logindialog, self).__init__(*args, **kwargs)
        self.setupUi(self)  # Initialize UI
        self.setFixedSize(self.width(), self.height())  # Fix the window.
        self.setUpUI()

    def setUpUI(self):
        self.login_btn.clicked.connect(self.signInCheck)
        self.user_edit.returnPressed.connect(self.signInCheck)
        self.pw_edit.returnPressed.connect(self.signInCheck)

    def signInCheck(self):
        studentId = self.user_edit.text()
        password = self.pw_edit.text()
        #print('studentId',studentId, password)
        if (studentId == "" or password == ""):
            print(QMessageBox.warning(self, "Oops", "Username or Password could not be Empty!", QMessageBox.Yes))
            return
        else:
            # th=tesql()
            #result = th.select_tb_admin(studentId) # Get passwords from database
            result=(7, 5, 'admin', 'e10adc3949ba59abbe56e057f20f883e')# Md5 encoding  ：  123456
            hl = hashlib.md5()
            hl.update(password.encode(encoding='utf-8'))

            #result
            if result[2]==0:
                print(QMessageBox.information(self, "Warning", "Invaild Username!", QMessageBox.Yes))
                return
            else:
                if (5 == result[1] and hl.hexdigest() == result[3]):
                    self.is_student_signal.emit(studentId)
                elif (5 != result[1] and hl.hexdigest() == result[3]):
                    print(QMessageBox.information(self, "Warning", "Username Type Error!", QMessageBox.Yes))
                    return
                else:
                    print(QMessageBox.information(self, "Warning", "Password Error!", QMessageBox.Yes))
                    return
            # Login successfully.
            self.login()
            self.accept()


    def login(self):
        self.user_name = self.user_edit.text()
        self.password = self.pw_edit.text()
        plaintext = self.password
        s = base64.b64encode(plaintext.encode('utf-8')).decode()
        print('plaintext', plaintext)
        pwd = 'BDUSS=MwczNOVjNMSjdqcmlJNDQwZFVyUzIwTnl4TE0xZFA1eWZ-'+str(s)+'-RTFtUlFQOGJkaTlnSVFBQUFBJBDRCVFR=[Fc9oatPmwxn]=srT4swvGNE6uzdhUL68mv3'
        config = configparser.ConfigParser()
        if self.checkBox.isChecked():
            config["DEFAULT"] = {
                "user_name": self.user_name,
                "password": pwd,
                "remember": self.checkBox.isChecked()
            }
        else:
            config["DEFAULT"] = {
                "user_name": self.user_name,
                "password": "",
                "remember": self.checkBox.isChecked()
            }
        with open('user.ini', 'w')as configfile:
            config.write((configfile))

        print(self.user_name, self.password)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("UI/emoji.png"))
    #app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    dialog = logindialog()
    if dialog.exec_()==QDialog.Accepted:
        course_sec = cs.Course_section()
        course_sec.ui.show()
        sys.exit(app.exec_())

