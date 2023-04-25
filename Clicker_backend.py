'''
    Senior Project: Clicker for ZJUI Undergraduate
    Date: 3-11-2023
    Version: 1.2
'''

import serial
import time
import matplotlib.pyplot as plt
import numpy as np
import random
import threading

ID_LEN = 7 # ID of Clicker is a 4-digit number. Like"1234".
ANS_LEN = 1 # 'A', 'B', 'C', 'D', 'E'
DIV_LEN = 3 
MSG_LEN = ANS_LEN + DIV_LEN + ID_LEN + 2 # "[Ans][3 spaces][ID]\r\n"

class Clicker_resp:
    # Include the ID of Clicker and answer.
    id = 0
    ans = ''

    def __init__(self, message):
      self.id = int(message[ANS_LEN + DIV_LEN : ANS_LEN + DIV_LEN + ID_LEN])
      self.ans = message[0]

def msg_filter(msg:str)->str:
    print(msg)
    if len(msg) ==  MSG_LEN:
        return 1, msg[:(ID_LEN + ANS_LEN + 3)]
    else:
        return 0, msg[:(ID_LEN + ANS_LEN)]  

ans_dict = {}
running = 1
def USB_init(port):
    # Set port value.
    serialPosrt = port
    # Set baudRate value.
    baudRate = 9600
    # Set timeout, and the unit is second.
    timeout = 0.5
    # Receive serial port data.
    global ser
    global serLock
    global ans_dict
    global running
    running = 1
    ans_dict = {}
    serLock = threading.Lock()
    ser = serial.Serial(serialPosrt, baudRate, timeout=timeout)

def USB_read():
    global ser
    global serLock
    global ans_dict
    global running

    serLock.acquire()
    if running != 1:
        serLock.release()
        return -1
    status, msg = msg_filter(ser.readline())
    if status:
        c = Clicker_resp(msg)
        print("ID: %d, Ans: %c" % (c.id, c.ans))
        ans_dict[c.id] = c.ans

        serLock.release()
        return 0
    else:
        serLock.release()
        return -1


def USB_read_cont(port:str, timelim)->Clicker_resp:
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
    plt.figure()
    plt.title("Correct Answers: " + correct)
    plt.xlabel("Options")
    plt.ylabel("Number")

    options = ['A', 'B', 'C', 'D', 'E']
    ans = list(stu_ans.values())
    num = [ans.count(ord(x)) for x in options]

    r_g = ["green" if op == correct else "red" for op in options] # Right answer is "green" and wrong answer is "red".


    plt.bar(options, num, color = r_g)

    for x,y in zip(options, num):   
        plt.text(x, y, '%d'%y, ha='center', va='bottom', fontsize=7)
    plt.show()
    return

def plot_attendance():
    plt.figure()
    global ans_dict
    y = [len(ans_dict), 4]
    plt.pie(y, labels = ["Present", "Absent"], autopct='%d')
    plt.title("Attendance: %.2f%%" % (100*y[0]/y[1]))
    plt.show()
    return

def collect_ans(timelim):
    global stu_ans
    stu_ans = {}

    
    port = "COM5"
    for c in USB_read_cont(port, timelim):
        print("ID: %d, Ans: %c" % (c.id, c.ans))
        stu_ans[c.id] = c.ans
    
    '''
    # Random Ans Test
    for i in range(100):
        stu_ans[i] = random.choice(['A', 'B', 'B', 'C', 'D', 'E'])
    '''
    print("Response:")

    return stu_ans

if __name__ == '__main__':
    stu_ans = collect_ans(20)
    correct = 'A'
    plot_answer(stu_ans, correct)
    plot_attendance()

        



