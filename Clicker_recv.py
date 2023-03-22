'''
    Senior Project: Clicker for ZJUI Undergraduate
    Date: 3-11-2023
    Version: 1.1
'''

import serial
import time
import matplotlib.pyplot as plt
import numpy as np
import random

ID_LEN = 4 # ID of Clicker is a 4-digit number. Like"1234".
ANS_LEN = 1 # 'A', 'B', 'C', 'D', 'E', 'F'
MSG_LEN = ID_LEN + ANS_LEN + 2 # "ID[Ans]\r\n"

class Clicker_resp:
    # Include the ID of Clicker and answer.
    id = 0
    ans = 0

    def __init__(self, message):
      self.id = int(message[:ID_LEN])
      self.ans = message[ID_LEN]
   


def USB_read(port:str, timelim)->Clicker_resp:
    '''
        Input:  The port of USB.
                Time limit (second) of answering.

        Output: A generator of the message infomation sent by Clickers.

        Side Effect: 
    '''

    
    # Set port value.
    serialPosrt = port
    # Set baudRate value.
    baudRate = 9600
    # Set timeout, and the unit is second.
    timeout = 0.5
    # Receive serial port data.
    ser = serial.Serial(serialPosrt, baudRate, timeout=timeout)
    

    # Initial time
    t0 = time.time()

    def msg_filter(msg:str)->str:
        print(msg)
        if len(msg) ==  MSG_LEN:
            return 1, msg[:(ID_LEN + ANS_LEN)]
        else:
            return 0, msg[:(ID_LEN + ANS_LEN)]
        
    # Get message continuously within time limit.
    while time.time() - t0 < timelim:
        '''
        str = ser.readline()
        print(str)
        '''
        status, msg = msg_filter(ser.readline())
        #msg = msg_filter(ser.readline())
        
        if status:
            yield Clicker_resp(msg)
    
    print("Section End (^v^)/")


def plot_answer(stu_ans:dict, correct):
    plt.title("Student Answers")
    plt.xlabel("Options")
    plt.ylabel("Number")

    options = ['A', 'B', 'C', 'D', 'E']
    ans = list(stu_ans.values())
    num = [ans.count(x) for x in options]

    r_g = ["green" if op == correct else "red" for op in options]

    print(r_g)

    plt.bar(options, num, color = r_g)

    for x,y in zip(options, num):   
        plt.text(x, y, '%d'%y, ha='center', va='bottom', fontsize=7)
    plt.show()
    return

def plot_attendance():
    y = [72, 28]
    plt.pie(y, labels = ["Present", "Absent"], autopct='%d')
    plt.title("Attendance: %.2f%%" % (100*y[0]/sum(y)))
    plt.show()
    return

def main():
    timelim = 15
    stu_ans = {}

    '''
    port = "COM6"
    for c in USB_read(port, timelim):
        print("ID: %d, Ans: %c" % (c.id, c.ans))
        stu_ans[c.id] = c.ans
    '''

    # Random Ans Test
    for i in range(100):
        stu_ans[i] = random.choice(['A', 'B', 'B', 'C', 'D', 'E'])
    print("Response:")
    correct = 'B'
    plot_answer(stu_ans, correct)
    plot_attendance()
    return

if __name__ == '__main__':
    main()

        



