from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

import sys


class Ans_history(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('UI/Ans_hist.ui')


        self.ui.setWindowTitle("Question History")
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # The size of table will fix to the window.
        self.center_table()
        #self.ui.tableWidget.item().setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        # -----Buttons-----
        # Button: Start Course
        #self.ui.pushButton_4.clicked.connect(self.start_course)

    def center_table(self):
        for i in range(self.ui.tableWidget.rowCount()):
            for j in range(self.ui.tableWidget.columnCount()):
                self.ui.tableWidget.item(i,j).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    







if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ans_history()
    window.ui.show()
    sys.exit(app.exec_())