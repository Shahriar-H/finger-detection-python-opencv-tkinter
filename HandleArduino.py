import serial.tools.list_ports


ports = serial.tools.list_ports.comports();
serialInst = serial.Serial()

portList=[];

for onePort in ports:
    portList.append(str(onePort));
    print(str(onePort));

val = input("Select Port: COM");

for x in range(0,len(portList)):
    if portList[x].startswith("COM" + str(val)):
        portVar = "COM"+str(val);
        print(portVar+1)

serialInst.baudrate = 9600;
serialInst.port = 'COM4';
serialInst.open();

while True:
    command = input("Arduino Command: ")
    serialInst.write(command.encode('utf-8'))

    if command=='exit':
        exit();
