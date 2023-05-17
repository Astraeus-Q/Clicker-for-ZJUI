'''
    Senior Project: Clicker for ZJUI Undergraduate
    Date: 3-11-2023
    Version: 1.2
'''

import serial
import serial.tools.list_ports
import time
import matplotlib.pyplot as plt
import numpy as np
import random
import threading

import Clicker_DB_manager as dbm

ID_LEN = 7 # ID of Clicker is a 7-digit number. Like"0123456".
ANS_LEN = 1 # 'A', 'B', 'C', 'D' or 'E'
MSG_LEN = ANS_LEN + ID_LEN + 2 # "[Ans][ID]\r\n"

# Gloabl Variable
ans_dict = {}
running = 1
class Clicker_resp:
    # Include the ID of Clicker and answer.
    def __init__(self, message):
      self.id = "%07d" % int(message[ANS_LEN: ANS_LEN + ID_LEN]) # 7-digit number. 0 is added on the left if needed.
      self.ans = message[0]

def msg_filter(msg:str)->str:
    print(msg)
    if len(msg) ==  MSG_LEN:
        return 1, msg[:(ID_LEN + ANS_LEN)]
    else:
        return 0, msg[:(ID_LEN + ANS_LEN)]  


def USB_init():
    # Get the port of Arduino automatically.
    for pi in list(serial.tools.list_ports.comports()):
        if pi[2].startswith('USB VID:PID=2341:0043'):
            # Set port value.
            serialPosrt = pi[0] 
            print(serialPosrt)
            break

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
        print("ID: %s, Ans: %c" % (c.id, c.ans))
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


def plot_answer(stu_ans:dict, correct, pic_path):
    plt.figure()
    plt.title("Correct Answers: " + correct)
    plt.xlabel("Options")
    plt.ylabel("Number")

    options = ['A', 'B', 'C', 'D', 'E']
    ans = list(stu_ans.values())
    num = [ans.count(ord(x)) for x in options] # ord() returns ASCII value.

    if correct == 'V':
        plt.title("Vote")
        r_g = ["green" for op in options]
    else:
        plt.title("Correct Answers: " + correct)
        r_g = ["green" if op == correct else "red" for op in options] # Right answer is "green" and wrong answer is "red".


    plt.bar(options, num, color = r_g)

    for x,y in zip(options, num):   
        plt.text(x, y, '%d'%y, ha='center', va='bottom', fontsize=7)
    plt.savefig(pic_path)
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

def update_JSONDB_ans(course_path, class_idx: str, ques_idx: str, correct_ans, point: str, ans_time):
    c_db_path = course_path + ("%s.json" % class_idx)
    dict_a = dbm.read_DB(c_db_path)
    s_db_path = course_path + "student.json"
    dict_s = dbm.read_DB(s_db_path)

    global ans_dict
    num_total_ans = 0
    num_correct_ans = 0
    for id in ans_dict:
        if id in dict_s:
            # Student belongs to this course.
            stu_name = dict_s[id]
            dict_a["Student"][stu_name][ques_idx] = chr(ans_dict[id])
            num_total_ans += 1
            if chr(ans_dict[id]) == correct_ans or correct_ans == "V":
                num_correct_ans += 1
    dict_a["Question"][ques_idx] = [correct_ans, num_total_ans, num_correct_ans, point, ans_time]
    dbm.write_DB(c_db_path, dict_a)
    return


if __name__ == '__main__':
    stu_ans = collect_ans(20)
    correct = 'A'
    plot_answer(stu_ans, correct)
    plot_attendance()

        



