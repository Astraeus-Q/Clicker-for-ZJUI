from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

import sys 
import os

import Clicker_DB_manager as dbm
import answer_hist_UI as ah
import ZITA

class Course_history(QMainWindow):

    def __init__(self, user_path: str, course_name):
        super().__init__()
        self.ui = uic.loadUi('UI/Course_hist.ui')
        self.ui.setWindowTitle("Course History")
        
        self.user_path = user_path
        self.course_name = course_name
        self.course_path = user_path + ("/%s/" % self.course_name)

        self.dict_c = (dbm.read_DB(self.user_path+"course.json"))[self.course_name] # Load the course database.
        self.create_table()

        # -----Buttons-----
        # Button: Select All
        self.ui.pushButton.clicked.connect(self.select_all)
        # Button: Unselect All
        self.ui.pushButton_4.clicked.connect(self.unselect_all)        
        # Button: Detail
        self.ui.pushButton_2.clicked.connect(self.detail)
        # Button: Remove
        self.ui.pushButton_3.clicked.connect(self.remove)
        # Button: Remove Selected
        self.ui.pushButton_5.clicked.connect(self.remove_selected)
        # Button: ZITA
        self.ui.pushButton_6.clicked.connect(self.TA)
        # -----Table DoubleClick-----
        self.ui.tableWidget.itemDoubleClicked.connect(self.detail_clicked)



    def create_table(self):
        table = self.ui.tableWidget
        #table.setColumnWidth(4, 400)
        #table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # The size of table will fix to the window.
        self.fill_table()
        return
    
    def fill_table(self):
        # Use self.dict_c and data in each course (to calculate attendance) to fill the table.
        table = self.ui.tableWidget
        c_list = sorted(self.dict_c.keys())
        c_num = len(c_list) # Get the number of class.
        table.setRowCount(c_num)

        for i in range(c_num):
            ci = c_list[i] # Class NO.
            dict_a = (dbm.read_DB(self.course_path + ("%s.json"%ci))) # Answer data in this class.
            no_ques = 0
            dict_s = dict_a["Student"] # Data for each student.
            if not dict_a["Question"]:
                no_ques = 1
            
            for j in range(table.columnCount()):
                if j == 0:
                    # Class index.
                    newItem = QTableWidgetItem(ci)
                    newItem.setCheckState(Qt.Unchecked)

                elif j == 1:
                    # Date
                    newItem = QTableWidgetItem(self.dict_c[ci][0])
                    
                elif j == 2:
                    # Total Student
                    if no_ques:
                        newItem = QTableWidgetItem("N.A.")
                    else:
                        stu_tot = len(dict_s.keys())
                    newItem = QTableWidgetItem(str(stu_tot))

                elif j == 3:
                    # Student attend
                    if no_ques:
                        newItem = QTableWidgetItem("N.A.")
                    else:
                        stu_att = 0
                        for si in dict_s:
                            if dict_s[si]:
                                # The student has once answered a question.
                                stu_att += 1
                    newItem = QTableWidgetItem(str(stu_att))

                elif j == 4:
                    # Attandance Rate
                    if no_ques:
                        newItem = QTableWidgetItem("N.A.")
                    else:
                        att_rate = str(int(stu_att/stu_tot*100)) + "%"
                    newItem = QTableWidgetItem(att_rate)

                elif j == 5:
                    # Topic
                    newItem = QTableWidgetItem(self.dict_c[ci][1])
                
                table.setItem(i, j, newItem)
                if table.item(i,j) != None:
                    table.item(i,j).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter) # Centralize


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
        
    def detail(self):
        global detail
        class_idx = self.ui.spinBox.value()
        if str(class_idx) not in self.dict_c:
             QMessageBox.information(self, "Oops", "Class%s does not exist!" % class_idx, QMessageBox.Ok)
             return
        detail = ah.Ans_history(self.course_path, class_idx)
        detail.ui.show()
        return
    
    def detail_clicked(self, Item=None):
        if Item == None:
            print("None")
            return
        global detail
        class_idx = int(self.ui.tableWidget.item(Item.row(),0).text())
        detail = ah.Ans_history(self.course_path, class_idx)
        detail.ui.show()
    
    def update_jf_c(self):
        dict_all_c = (dbm.read_DB(self.user_path+"course.json")) # All course data under the user.
        dict_all_c[self.course_name] = self.dict_c
        dbm.write_DB(self.user_path+"course.json", dict_all_c)

    def remove_one_record(self, class_idx: str):
        # Remove the class in class record.
        state = self.dict_c.pop(class_idx, -1)
        if state == -1:
            print(QMessageBox.warning(self, "Oops", "No such class.", QMessageBox.Yes))
            return

        # Remove the answer data of the class.
        f_path = self.course_path + "%s.json" % class_idx
        if os.path.isfile(f_path):
            os.remove(f_path)
        else:
            print("ERROR!!! No such file.")


    def remove(self):
        class_idx = str(self.ui.spinBox.value())
        if QMessageBox.Yes == QMessageBox.warning(self, "Confirmation", "Are you sure about removing class%s?" % class_idx, QMessageBox.Yes, QMessageBox.No):
            self.remove_one_record(class_idx)
            self.update_jf_c()
            self.fill_table()

    def remove_selected(self):
        table = self.ui.tableWidget
        modified = 0
        if QMessageBox.Yes == QMessageBox.warning(self, "Confirmation", "Are you sure about removing classes selected?", QMessageBox.Yes, QMessageBox.No):
            for i in range(table.rowCount()):
                if table.item(i,0).checkState() == Qt.Checked:
                    class_idx = table.item(i,0).text()
                    modified = 1
                    self.remove_one_record(class_idx)
            
            if modified == 1:
                self.update_jf_c()
                self.fill_table()
        return        

    def TA(self):
        global zi_ta
        zi_ta = ZITA.ZI_TA(self.course_name)
        zi_ta.ui.show()

    
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Course_history("JSON_Base/admin/", "ECE_110")
    window.ui.show()
    sys.exit(app.exec_())