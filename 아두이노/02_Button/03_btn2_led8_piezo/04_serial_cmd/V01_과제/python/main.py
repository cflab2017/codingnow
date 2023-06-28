import serial
import keyboard as ky
import time

# pip install serial
# pip install pyserial
# pip uninstall serial

###########################################
seri = serial.Serial(port='COM27', baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS) 
###########################################
def sendOnLedRight():    
    for i in range(0,9):
        comm = 'on'
        for j in range(0,8):
            if i==j:
                comm += '1'
            else:
                comm += '0'

        print('Send : ', comm)
        comm += '\n'
        seri.write(bytes(comm, encoding='ascii'))
        time.sleep(0.05) 
###########################################
def sendOnLedLeft():    
    for i in range(8,0,-1):
        comm = 'on'
        for j in range(0,8):
            if i==j:
                comm += '1'
            else:
                comm += '0'

        print('Send : ', comm)
        comm += '\n'
        seri.write(bytes(comm, encoding='ascii'))
        time.sleep(0.05) 
###########################################
def eventProcess():
    while True:
        event = ky.read_key()
        try:
            if event == "right":
                sendOnLedRight()
            if event == "left":
                sendOnLedLeft()
            if event == "esc":  # 종료
                return
        except:
            pass  
###########################################
eventProcess()
seri.close()
print('Finish')
###########################################