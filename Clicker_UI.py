import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
#import qdarkstyle
import base64
import configparser

import hashlib

# Windows
from login_UI import Ui_Form
import course_section_UI as cs
import Clicker_DB_manager as dbm
import remote_db

# Global Variable
login_user = "Tester"
REMEMBER_ME = "*" # For Remember Me function.
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

        db.sync_local_account()
        self.dict_a = dbm.read_DB("JSON_Base/account.json") # Accounts    
        self.remembered = 0 # Remember me
        if self.dict_a[REMEMBER_ME] != REMEMBER_ME:
            print("Remember me")
            self.remembered = 1
        if self.remembered:
            # Remember me
            self.user_edit.setText(self.dict_a[REMEMBER_ME])
            self.pw_edit.setText("1234567890")
            self.checkBox.setChecked(True)

    def signInCheck(self):
        username = self.user_edit.text()
        password = self.pw_edit.text()
        #print('username',username, password)
        succeed = 0
        if (username == "" or password == ""):
            print(QMessageBox.warning(self, "Oops", "Username or Password could not be Empty!", QMessageBox.Yes))
            return
        else:
            # th=tesql()
            #result = th.select_tb_admin(username) # Get passwords from database
            hl = hashlib.md5()
            hl.update(password.encode(encoding='utf-8'))


            if username not in self.dict_a:
                print(QMessageBox.information(self, "Warning", "Username does not exist!", QMessageBox.Yes))
                return
            elif username == REMEMBER_ME:
                QMessageBox.information(self, "Warning", "Username cannot be %s!"% REMEMBER_ME, QMessageBox.Yes)
                return
            
            else:
                if hl.hexdigest() == self.dict_a[username]:
                    succeed = 1
                elif self.remembered and username == self.dict_a[REMEMBER_ME]:
                    succeed = 1
                else:
                    print(QMessageBox.information(self, "Warning", "Password Error!", QMessageBox.Yes))
                    return
            if succeed == 1:
                if self.checkBox.isChecked():
                    self.dict_a[REMEMBER_ME] = username
                else:
                    self.dict_a[REMEMBER_ME] = REMEMBER_ME
                dbm.write_DB("JSON_Base/account.json", self.dict_a)
                self.is_student_signal.emit(username)
                global login_user
                login_user = username
                global course_sec
                course_sec = cs.Course_section(login_user)
                course_sec.ui.show()
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

db = remote_db.remote_db()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("UI/emoji.png"))
    #app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    
    dialog = logindialog()
    if dialog.exec_()==QDialog.Accepted:
        sys.exit(app.exec_())

