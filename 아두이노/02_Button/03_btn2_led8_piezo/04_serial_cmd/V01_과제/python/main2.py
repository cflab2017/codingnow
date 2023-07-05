import serial
import keyboard as ky
import time

# pip install keyboard
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
    comm = "on00000000"  
    comm += '\n'
    seri.write(bytes(comm, encoding='ascii'))
    print(comm)
    time.sleep(0.05) 
###########################################
def sendOnLedLeft():  
    comm = "on11111111"  
    comm += '\n'
    seri.write(bytes(comm, encoding='ascii'))    
    print(comm)
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
###########################################