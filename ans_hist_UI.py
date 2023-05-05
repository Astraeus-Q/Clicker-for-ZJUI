from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

import sys
import json


class Ans_history(QMainWindow):

    def __init__(self, db_path, class_idx):
        super().__init__()
        self.ui = uic.loadUi('UI/Ans_hist.ui')

        self.ui.setWindowTitle("Question History")

        self.create_table(db_path, class_idx)

        # -----Buttons-----
        # Button: Select All
        self.ui.pushButton.clicked.connect(self.select_all)

        # Button: Unselect All
        self.ui.pushButton_4.clicked.connect(self.unselect_all)


    
    def create_table(self, db_path, class_idx):
        table = self.ui.tableWidget
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # The size of table will fix to the window.
        jf_a = open(db_path, "r") # Open JSON database.
        dict_a = json.load(jf_a)
        print(dict_a)
        dict_std_c = dict_a["Standard"][class_idx]
        q_list = sorted(dict_std_c.keys())
        q_num = len(q_list) # Get the number of question in this class.
        table.setRowCount(q_num)

        def fill_table(table):
            for i in range(q_num):
                qi = q_list[i]
                for j in range(table.columnCount()):
                    if j == 0:
                        newItem = QTableWidgetItem(qi) # Fill question index.
                        newItem.setCheckState(Qt.Unchecked)
                    else:
                        print(dict_std_c[qi][j-1])
                        newItem = QTableWidgetItem(str(dict_std_c[qi][j-1])) # Fill question information.

                    table.setItem(i, j, newItem)
                    if table.item(i,j) != None:
                        table.item(i,j).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter) # Centralize

        fill_table(table)


    def select_all(self):
        table = self.ui.tableWidget
        for i in range(table.rowCount()):
            table.item(i,0).setCheckState(Qt.Checked)

    def unselect_all(self):
        table = self.ui.tableWidget
        for i in range(table.rowCount()):
            table.item(i,0).setCheckState(Qt.Unchecked)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ans_history("JSON_Base/admin/ECE_110.json", "1")
    window.ui.show()
    sys.exit(app.exec_())