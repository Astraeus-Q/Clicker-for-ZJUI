from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

import sys
import os
import json
import matplotlib.pyplot as plt
import re

import Clicker_DB_manager as dbm
import plot_window as pw

#import Clicker_UI as cui # For remote db


class Detail_history(QMainWindow):
    def __init__(self, course_path, class_idx: str, ques_list: list):
        super().__init__()
        self.ui = uic.loadUi('UI/Answer_detail_hist.ui')

        self.ui.setWindowTitle("Question Detail")
        table = self.ui.tableWidget

        # Load answer section Json database.
        self.course_path = course_path
        self.class_idx = class_idx
        db_path = self.course_path + ("%s.json" % self.class_idx)
        dict_a = dbm.read_DB(db_path) # Open JSON database.

        self.dict_ques = dict_a["Question"] # Question Record
        self.dict_stud = dict_a["Student"] # Student Record
        q_list = sorted(ques_list)
        q_num = len(q_list)
        s_list = sorted(self.dict_stud.keys())
        s_num = len(s_list)
        table.setRowCount(s_num) # Row header is student name.
        table.setColumnCount(q_num + 1) # Column header is question+answer. +1 is for total points.

        width_fit = (800 + 80 * q_num) % 1600
        heigh_fit = (400 + 20 * s_num) % 1000
        self.ui.resize(width_fit, heigh_fit) # The size of the table is fit to the amount of data.

        for ri in range(table.rowCount()):
            stud_name = s_list[ri] # Student name.
            rhead_item = QTableWidgetItem(stud_name) 
            table.setVerticalHeaderItem(ri, rhead_item)
            total_point = 0 # The sum of the points that the student got in this class.
            for ci in range(table.columnCount()):
                if ci == table.columnCount() - 1:
                    # Last Column
                    chead_item = QTableWidgetItem("Total Points")
                    newItem = QTableWidgetItem(str(total_point))
                    table.setItem(ri, ci, newItem)
                    table.item(ri,ci).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter) # Centralize
                else:
                    ques_idx = q_list[ci]
                    chead_item = QTableWidgetItem("Question%s [%s]" % (ques_idx, self.dict_ques[q_list[ci]][0])) # e.g. Question [A]
                    if ques_idx in self.dict_stud[stud_name]:
                        # This student has answered the question.
                        stud_ans = self.dict_stud[stud_name][ques_idx]
                        if self.dict_ques[ques_idx][0] == "V":
                            point = self.dict_ques[ques_idx][3]
                        else:
                            point = self.dict_ques[ques_idx][3] if stud_ans == self.dict_ques[ques_idx][0] else str(0)
                        newItem = QTableWidgetItem("%s  [%s]" % (point, stud_ans))
                        total_point += int(point)
                        table.setItem(ri, ci, newItem)
                        table.item(ri,ci).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter) # Centralize
                    else:
                        newItem = QTableWidgetItem("")
                        table.setItem(ri, ci, newItem)
                        


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
        # Just two ways to apply regular expression.
        ques_idx = re.search("\d+\.?\d*", chead).group(0)
        correct = re.findall("[\[](.*?)[\]]", chead)[0]

        plt.figure()
        plt.xlabel("%s-%s" % (self.class_idx, ques_idx))
        plt.ylabel("Number")

        options = ['A', 'B', 'C', 'D', 'E']
        ans = []
        for studi in self.dict_stud:
            if ques_idx in self.dict_stud[studi]:
                ans.append(self.dict_stud[studi][ques_idx])

        num = [ans.count(x) for x in options]

        if correct == 'V':
            plt.title("Vote")
            r_g = ["green" for op in options]
        else:
            plt.title("Correct Answers: " + correct)
            r_g = ["green" if op == correct else "red" for op in options] # Right answer is "green" and wrong answer is "red".


        plt.bar(options, num, color = r_g)

        for x,y in zip(options, num):   
            plt.text(x, y, '%d'%y, ha='center', va='bottom', fontsize=7)
        
        pic_path = self.course_path+"ans.png"
        plt.savefig(pic_path)
        global plot
        plot = pw.Plot_win("Answer Distribution", pic_path)
        plot.ui.show()

        # try:
        #     img = plt.imread(self.course_path + "%s-%s.png" % (self.class_idx, ques_idx))
        #     plt.imshow(img)
        #     plt.axis('off')
        #     plt.show()
        # except:
        #     print(QMessageBox.warning(self, "Oops", "The chart has been deleted!", QMessageBox.Yes))
            


        
        
        
        

class Ans_history(QMainWindow):

    def __init__(self, course_path, class_idx: str):
        super().__init__()
        self.ui = uic.loadUi('UI/Answer_hist.ui')

        self.ui.setWindowTitle("Question History")

        self.course_path = course_path
        self.class_idx = class_idx

        # Remote db.
        #cui.db.history_update()
        
        self.db_path = course_path + ("%s.json" % self.class_idx)
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
        # Button: Detail Selected
        self.ui.pushButton_6.clicked.connect(self.detail_selected)
        # -----Table DoubleClick-----
        self.ui.tableWidget.itemDoubleClicked.connect(self.detail_clicked)


    def open_JSONDB(self):
        self.modified = 0 # Whether the database is modified.
        self.dict_a = dbm.read_DB(self.db_path) # Open JSON database.
        if self.dict_a:
            self.dict_ques = self.dict_a["Question"] # Question Record
            self.dict_stud = self.dict_a["Student"] # Student Record
        return
        

    def create_table(self):
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # The size of table will fix to the window.
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

    def remove_one_record(self, ques_idx: str):
        # Remove the quesion in question record.
        state = self.dict_ques.pop(ques_idx, -1)
        if state == -1:
            print(QMessageBox.warning(self, "Oops", "No such question.", QMessageBox.Yes))
            return
        self.dict_a["Question"] = self.dict_ques

        # Remove the question in student record.
        for di in self.dict_stud.values():
            di.pop(ques_idx, -1)

        # Delete the statistics chart
        # pic_path = self.course_path + "%s-%s.png" % (self.class_idx, ques_idx)
        # if os.path.isfile(pic_path):
        #     os.remove(pic_path)
        # else:
        #     print("ERROR!!! No such file.")
        return
    
    def remove(self):
        ques_idx = str(self.ui.spinBox.value())
        if QMessageBox.Yes == QMessageBox.warning(self, "Confirmation", "Are you sure about removing question%s?" % ques_idx, QMessageBox.Yes, QMessageBox.No):
            self.remove_one_record(ques_idx)
            self.update_jf_a()
            self.fill_table()
        return

    def remove_selected(self):
        table = self.ui.tableWidget
        modified = 0
        if QMessageBox.Yes == QMessageBox.warning(self, "Confirmation", "Are you sure about removing questions selected?", QMessageBox.Yes, QMessageBox.No):
            for i in range(table.rowCount()):
                if table.item(i,0).checkState() == Qt.Checked:
                    ques_idx = table.item(i,0).text()
                    modified = 1
                    self.remove_one_record(ques_idx)
            
            if modified == 1:
                self.update_jf_a()
                self.fill_table()
        return


    def update_jf_a(self):
        dbm.write_DB(self.db_path, self.dict_a)
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

    def detail_selected(self):
        table = self.ui.tableWidget
        ques_list = []
        for i in range(table.rowCount()):
            if table.item(i,0).checkState() == Qt.Checked:
                ques_idx = table.item(i,0).text()
                ques_list.append(ques_idx)
                global detail
        global detail
        detail = Detail_history(self.course_path, self.class_idx, ques_list)
        detail.ui.show()

    def __del__(self):
        pass






if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ans_history("JSON_Base/Rigel/ECE_110/", 1)
    window.ui.show()
    sys.exit(app.exec_())