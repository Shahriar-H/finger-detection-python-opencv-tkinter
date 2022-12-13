import serial

ser = serial.Serial("COM27", 9600, timeout = 1) #Change your port name COM... and your baudrate

def getDataFromArduino():
    ser.write(b'1')
    data = ser.readline().decode('ascii')
    return data
def receiveFingerData(fingerNum):
    while(True):
        uInput = fingerNum
        ser.write(fingerNum)
        print(getDataFromArduino())
        # if uInput == '1':
        #     print(retrieveData())
        # else:
        #     ser.write(b'0')