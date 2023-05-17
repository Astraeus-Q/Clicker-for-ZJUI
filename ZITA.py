'''
* ZITA: Teaching Analysis System

It could extract useful information and generate corresponding
strategy or comment.
So far, we just makeup the data and hardcode the course,
for the sack of the convenience of demostration.

'''

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QIcon
from PyQt5.QtCore import QTimer, QThread
from PyQt5 import uic

import sys
import matplotlib.pyplot as plt
import numpy as np
import random

class ZI_TA(QMainWindow):
    def __init__(self, course_name):
        super().__init__()
        self.ui = uic.loadUi('UI/ZITA.ui')
        self.ui.setWindowTitle("ZITA")
        self.plot_att()
        p_attendance = QPixmap("ZITA/attendance.png")
        self.ui.label_2.setPixmap(p_attendance)

        self.course_name = course_name
        self.att_remark()

    def plot_att(self):
        plt.figure()
        # Fluctuation
        # Stably High
        # Stably Medium
        # Stably Low
        # Rise
        # Drop
        att_list = [[70,75,85,55,90,80,75,65,75,65,50,30,45,60,60,65,70,50,60,70,60,80,85,65,70],
                    [85,75,80,70,70,75,70,65,50,75,85,90,75,70,65,55,70,65,60,80,75,70,65,75,70],
                    [60,55,65,70,50,40,35,45,50,55,65,50,60,40,35,55,50,65,40,50,55,45,65,60,50],
                    [20,15,35,40,50,30,35,25,10,45,45,35,25,40,30,15,20,35,45,20,25,35,40,30,25],
                    [50,45,40,45,30,40,45,40,35,60,50,35,45,50,60,65,70,60,55,65,70,80,75,70,80],
                    [90,85,80,90,85,80,75,70,75,60,65,70,75,60,50,60,55,45,55,35,40,20,15,20,20]]  
        
        y = np.array(random.choice(att_list)) #y
        #y = np.array([90,80,75,65,75,65,55,40,45])
        x = np.array([i for i in range(len(y))])
        plt.xticks(x) # Force the x-coordinate to be integer.
        plt.yticks(np.linspace(0, 100, 11))
        plt.ylim([0,100])
        plt.plot(x, y, 'b*--', alpha=0.5, linewidth=1, label='acc') # Plot dots.
        self.slope, intercept = np.polyfit(x, y, 1)
        plt.plot(x, self.slope * x + intercept, color='orange') # Plot line.
        self.var = y.var()
        self.avg = y.mean()

        coefs = np.polyfit(x, y, 6)
        poly = np.poly1d(coefs)
        new_x = np.linspace(min(x), max(x), 1000)

        plt.plot(new_x, poly(new_x), color='red') # Plot polynomial
        plt.savefig("ZITA/attendance.png")
    
    def att_remark(self):
        # Generate attendance remark.
        remark = "Average attendance rate: %d\n\n" % int(self.avg)

        print(self.slope, self.var)
        adv = ""
        if abs(self.slope) < 0.5:
            # Flat Slope
            if self.var > 120:
                # Fluctuation
                adv = "You are experiencing \"significant fluctuations\" in course attendance.\n\nStrategy: "
                f_adv = open("ZITA/advice_fluctuate.txt", "r")
                adv_list = f_adv.readlines()
                adv += random.choice(adv_list)  

            elif self.avg >= 70:
                # Stable High
                adv = "The attendance rate of your course is \"stably high\".\n\nComment: "
                f_adv = open("ZITA/comment_st_high.txt", "r")
                adv_list = f_adv.readlines()
                adv += random.choice(adv_list)  

            elif self.avg > 50:
                # Stable Medium
                adv = "You have a \"stable but average\" attendance rate in your course.\n\nStrategy: "
                f_adv = open("ZITA/advice_st_avg.txt", "r")
                adv_list = f_adv.readlines()
                adv += random.choice(adv_list)  

            else:
                # Stable Low
                adv = "You are facing \"consistently low\" attendance rates in your course.\n\nStrategy: "
                f_adv = open("ZITA/advice_st_low.txt", "r")
                adv_list = f_adv.readlines()
                adv += random.choice(adv_list)  

        elif self.slope >= 0.5:
            # Rising
            adv = "You are experiencing a \"rise\" in course attendance, congratulations!\n\nComment: "
            f_adv = open("ZITA/comment_rise.txt", "r")
            adv_list = f_adv.readlines()
            adv += random.choice(adv_list)       

        else:
            # Dropping
            adv = "You are experiencing a \"drop\" in course attendance.\n\nStrategy: "
            f_adv = open("ZITA/advice_drop.txt", "r")
            adv_list = f_adv.readlines()
            adv += random.choice(adv_list)

        f_adv.close()
        remark += "%s\n" % adv
            
        self.ui.plainTextEdit_2.setPlainText(remark)

    # def course_remark(self):
    #     # Generate course remark.
    #     if self.course_name == 
        

            
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ZI_TA()
    window.ui.show()
    sys.exit(app.exec_())