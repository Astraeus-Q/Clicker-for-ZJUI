import serial.tools.list_ports

for port in list(serial.tools.list_ports.comports()):
    print(port[0])
    print(port[2])
    if port[2].startswith('USB VID:PID=2341:0043'):
        print("yes")