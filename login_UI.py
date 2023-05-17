# -*- coding: utf-8 -*-
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QLabel, QDesktopWidget, QHBoxLayout, QFormLayout, \
    QPushButton, QLineEdit
from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 610)

        # Set font
        font_12 = QtGui.QFont()
        font_12.setFamily("Times New Roman")
        font_12.setPointSize(12)
        font_14 = QtGui.QFont()
        font_14.setFamily("Times New Roman")
        font_14.setPointSize(14)
        font_16 = QtGui.QFont()
        font_16.setFamily("Times New Roman")
        font_16.setPointSize(16)

        # Parameters
        L = 300 # length of edit line
        H = 50 # Width/height of edit line and login botton.

        # Input username
        self.user_edit = QtWidgets.QLineEdit(Form)
        self.user_edit.setGeometry(QtCore.QRect(250, 270, L, H)) # R_off, D_off, L, H 
        self.user_edit.setFont(font_14)
        self.user_edit.setObjectName("user_edit")

    
        # Input password
        self.pw_edit = QtWidgets.QLineEdit(Form)
        self.pw_edit.setGeometry(QtCore.QRect(250, 380, L, H))
        self.pw_edit.setMaxLength(32) # The length limitation of password is 32 chars.
        pw_font = QFont()
        pw_font.setPixelSize(24)
        self.pw_edit.setFont(pw_font)
        self.pw_edit.setEchoMode(QLineEdit.Password) # Hide the password digit.
        self.pw_edit.setObjectName("pw_edit")

        # Login botton
        self.login_btn = QtWidgets.QPushButton(Form)
        self.login_btn.setGeometry(QtCore.QRect(300, 510, 200, H))
        self.login_btn.setFont(font_16)
        self.login_btn.setText("Login")
        self.login_btn.setObjectName("login_btn")
        self.login_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.login_btn.setStyleSheet("#login_btn{background-color:#2c7adf;color:#fff;border:none;border-radius:4px;}")

        # User label
        self.user_label = QtWidgets.QLabel(Form)
        self.user_label.setGeometry(QtCore.QRect(130, 280, 80, 30))
        self.user_label.setFont(font_16)
        self.user_label.setText("User:")
        self.user_label.setObjectName("user_label")

        # Password label
        self.pw_label = QtWidgets.QLabel(Form)
        self.pw_label.setGeometry(QtCore.QRect(66, 390, 160, 30))
        self.pw_label.setFont(font_16)
        self.pw_label.setText("Password:")
        self.pw_label.setObjectName("pw_label")

        # Top picture
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(0, 0, 800, 200))
        pixmap = QPixmap("UI/Interface2.png")
        scaredPixmap = pixmap.scaled(800, 200)
        self.label_4.setPixmap(scaredPixmap)

        # Remember me checkbox
        self.checkBox = QtWidgets.QCheckBox(Form)      # Remember me.
        self.checkBox.setGeometry(QtCore.QRect(580, 400, 180, 30))
        self.checkBox.setObjectName("checkBox")
        self.checkBox.setText("Remember Me")
        self.checkBox.setFont(font_12)

        # Title
        Form.setWindowTitle("Welcome to ZIC")

        #self.retranslateUi(Form) # Chinese version
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        # 中文版本。
        # For Chinese version, but it is not mandatory.
        _translate = QtCore.QCoreApplication.translate
        self.login_btn.setText(_translate("Form", "登录"))
        self.user_label.setText(_translate("Form", "用户:"))
        self.pw_label.setGeometry(QtCore.QRect(130, 390, 80, 30))
        self.pw_label.setText(_translate("Form", "密码:"))
        self.checkBox.setText(_translate("Form", "记住我"))





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    form = QtWidgets.QWidget()
    w = Ui_Form()
    w.setupUi(form)
    form.show()
    sys.exit(app.exec_())
