import serial

ser = serial.Serial()
ser.port = "COM8"
#ser.baudrate = 115200
ser.baudrate = 9600
ser.open()
print('run')
while(True):
    line = ser.readall()
    print(line)
    print(len(line))

    ser = serial.Serial()
ser.port = "COM9"
#ser.baudrate = 115200
ser.baudrate = 2400
ser.open()
print('run')
while(True):
    line = ser.readall()
    print(line)
    print(len(line))
        
    #print(line.decode('utf').rstrip('\n'))
    #print(line.decode('hex').rstrip('\n'))
    