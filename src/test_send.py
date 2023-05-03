import serial
import time
ser = serial.Serial('COM5',9600,timeout=1)
while 1:
    ser.write("Poll|1".encode("utf-8"))
    time.sleep(0.5)
    #val2 = ser.readline()
    #print(val2)