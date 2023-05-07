from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

import sys
import json
import matplotlib.pyplot as plt
import re



class Detail_history(QMainWindow):
    def __init__(self, course_path, class_idx, ques_list:list):
        super().__init__()
        self.ui = uic.loadUi('UI/Ans_detail_hist.ui')

        self.ui.setWindowTitle("Question Detail")
        table = self.ui.tableWidget

        # Load answer section Json database.
        self.course_path = course_path
        self.class_idx = class_idx
        db_path = self.course_path + ("%d.json" % self.class_idx)
        jf_a = open(db_path, "r+") # Open JSON database.
        dict_a = json.load(jf_a)

        dict_ques = dict_a["Question"] # Question Record
        dict_stud = dict_a["Student"] # Student Record
        q_list = sorted(ques_list)
        q_num = len(q_list)
        s_list = sorted(dict_stud.keys())
        s_num = len(s_list)
        table.setRowCount(s_num) # Row header is student name.
        table.setColumnCount(q_num + 1) # Column header is question+answer. +1 is for total points.

        width_fit = (800 + 80 * q_num) % 1600
        heigh_fit = (400 + 20 * s_num) % 1000
        self.ui.resize(width_fit, heigh_fit) # The size of the table is fit to the amount of data.

        for ri in range(table.rowCount()):
            rhead_item = QTableWidgetItem(s_list[ri]) # Student name.
            table.setVerticalHeaderItem(ri, rhead_item)
            for ci in range(table.columnCount()):
                if ci != table.columnCount() - 1:
                    chead_item = QTableWidgetItem("Question%s [%s]" % (q_list[ci], dict_ques[q_list[ci]][0])) # e.g. Question [A]
                else:
                    # Last Column
                    chead_item = QTableWidgetItem("Total Points")

                table.setHorizontalHeaderItem(ci, chead_item)
        
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # The size of table will fix to the window.
        
        # -----Table DoubleClick-----
        self.ui.tableWidget.itemDoubleClicked.connect(self.show_picture)

    def show_picture(self, Item=None):
        table = self.ui.tableWidget
        if Item == None or Item.column() == table.columnCount() - 1:
            print("None")
            return
        chead = table.horizontalHeaderItem(Item.column()).text()
        ques_idx = re.search("\d+\.?\d*", chead).group(0)
        img = plt.imread(self.course_path + "%s-%s.png" % (self.class_idx, ques_idx))
        plt.imshow(img)
        plt.axis('off')
        plt.show()


            


        
        
        
        

class Ans_history(QMainWindow):

    def __init__(self, course_path, class_idx):
        super().__init__()
        self.ui = uic.loadUi('UI/Ans_hist.ui')

        self.ui.setWindowTitle("Question History")

        self.course_path = course_path
        self.class_idx = class_idx
        self.db_path = course_path + ("%d.json" % self.class_idx)
        self.open_JSONDB()
        self.create_table()

        # -----Buttons-----
        # Button: Select All
        self.ui.pushButton.clicked.connect(self.select_all)
        # Button: Unselect All
        self.ui.pushButton_4.clicked.connect(self.unselect_all)
        # Button: Remove
        self.ui.pushButton_3.clicked.connect(self.remove)
        # Button: Remove Selected
        self.ui.pushButton_5.clicked.connect(self.remove_selected)
        # Button: Detail
        self.ui.pushButton_2.clicked.connect(self.detail)
        # -----Table DoubleClick-----
        self.ui.tableWidget.itemDoubleClicked.connect(self.detail_clicked)


    def open_JSONDB(self):
        self.modified = 0 # Whether the database is modified.
        self.jf_a = open(self.db_path, "r+") # Open JSON database.
        self.dict_a = json.load(self.jf_a)
        self.dict_ques = self.dict_a["Question"] # Question Record
        self.dict_stud = self.dict_a["Student"] # Student Record
        self.jf_a.close()
        return
        

    def create_table(self):
        table = self.ui.tableWidget
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # The size of table will fix to the window.
        self.fill_table()
        return


    def fill_table(self):
        # Use self.dict_ques to fill the table.
        table = self.ui.tableWidget
        q_list = sorted(self.dict_ques.keys())
        q_num = len(q_list) # Get the number of question in this class.
        table.setRowCount(q_num)
        for i in range(q_num):
            qi = q_list[i]
            for j in range(table.columnCount()):
                if j == 0:
                    newItem = QTableWidgetItem(qi) # Fill question index.
                    newItem.setCheckState(Qt.Unchecked)
                else:
                    newItem = QTableWidgetItem(str(self.dict_ques[qi][j-1])) # Fill question information.
                table.setItem(i, j, newItem)
                if table.item(i,j) != None:
                    table.item(i,j).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter) # Centralize
        return

    def select_all(self):
        table = self.ui.tableWidget
        for i in range(table.rowCount()):
            table.item(i,0).setCheckState(Qt.Checked)
        return

    def unselect_all(self):
        table = self.ui.tableWidget
        for i in range(table.rowCount()):
            table.item(i,0).setCheckState(Qt.Unchecked)
        return

    def remove_one_record(self, question_idx):
        # Remove the quesion in question record.
        state = self.dict_ques.pop(question_idx, -1)
        if state == -1:
            print(QMessageBox.warning(self, "Oops", "No such question", QMessageBox.Yes))
            return
        self.dict_a["Question"] = self.dict_ques

        # Remove the question in student record.
        for di in self.dict_stud.values():
            di.pop(question_idx, -1)
        return
    
    def remove(self):
        ques_idx = str(self.ui.spinBox.value())
        self.remove_one_record(ques_idx)
        self.update_jf_a()
        self.fill_table()
        return

    def remove_selected(self):
        table = self.ui.tableWidget
        modified = 0
        for i in range(table.rowCount()):
            if table.item(i,0).checkState() == Qt.Checked:
                ques_idx = table.item(i,0).text()
                modified = 1
                self.remove_one_record(ques_idx)
        
        if modified == 1:
            self.dict_a["Question"] = self.dict_ques
            self.update_jf_a()
            self.fill_table()
        return


    def update_jf_a(self):
        self.jf_a = open(self.db_path, "w+")
        json.dump(self.dict_a, self.jf_a, indent=4)
        self.jf_a.close()
        return


    def detail(self):
        global detail
        ques_list = [str(self.ui.spinBox.value())]
        detail = Detail_history(self.course_path, self.class_idx, ques_list)
        detail.ui.show()
        return
    
    def detail_clicked(self, Item=None):
        if Item == None:
            print("None")
            return
        global detail
        ques_list = [self.ui.tableWidget.item(Item.row(),0).text()]
        detail = Detail_history(self.course_path, self.class_idx, ques_list)
        detail.ui.show()

    def __del__(self):
        pass






if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ans_history("JSON_Base/admin/ECE_110/", 1)
    window.ui.show()
    sys.exit(app.exec_())