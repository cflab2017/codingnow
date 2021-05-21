import serial
import tkinter as tk
import time
import threading

# pip install serial
# pip install pyserial
# pip uninstall serial

seri = serial.Serial(port='COM9',
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS) 

ledState = 0x00
def sendToAruino(led):
    global ledState
    if ledState & led:
        ledState &= (~led)
    else:
        ledState |= led

    comm = "{:02x}".format(ledState)
    # comm = "{:02x}".format(led)#01
    comm = 'LED'+comm
    print('Send : ', comm)
    comm += '\n'
    seri.write(bytes(comm, encoding='ascii'))

####################################################
## GUI 생성하기
####################################################
class LedControl():
    commands = ['0', '1', '2','3','auto']

    def __init__(self):
        self.win = tk.Tk()
        self.win.title('[파이선] 아두이노 LED 제어')
        self.isAuto = False
        self.btn = [None for i in range(len(self.commands))]
        for i, comm in enumerate(self.commands):##버튼을 만든다.
            self.btn[i] = tk.Button(self.win,text=comm,
                width=10, height=5, 
                bg='gray', fg='black',
                command=lambda cmd=comm: self.button_click(cmd)
                )
            self.btn[i].grid(column=i, row=0)

    def button_click(self, value):
        if value == 'auto':
            self.isAuto = True
        else:
            self.isAuto = False
            led = 0x01<< int(value)
            print(led)
            sendToAruino(led)

#thread 1 함수
def TH_readSerial():
    global isT1Run
    while isT1Run:
        if seri.readable():
            res = seri.readline()
            res = res.decode()[:len(res)-1]
            print(' Response :', res,'\n')
            if res.find('Arduino LED') != -1:
                res = res.replace("Arduino LED : ", "")
                led = int(res, 16)
                for i in range(len(tool.btn)):
                    if led & (0x01 << i):
                        tool.btn[i].configure(bg="yellow")
                    else:
                        tool.btn[i].configure(bg="gray")
    print('stop1 thread')

# #thread 2  함수
def TH_sendCmdAuto():
    global isT2Run
    index = 0
    while isT2Run:
        if tool.isAuto:
            led = 0x01 << index
            sendToAruino(led)
            index = (index+1) % 4
        time.sleep(0.4)
    print('stop2 thread')

#GUI class 생성
tool = LedControl()

#쓰레드 생성
isT1Run = True
t1 = threading.Thread(target=TH_readSerial)
t1.start()

isT2Run = True
t2 = threading.Thread(target=TH_sendCmdAuto)
t2.start()

#GUI 실행
tool.win.mainloop()

#GUI 종료 후
seri.close()
isT1Run = False
isT2Run = False
time.sleep(0.5)
print('Finish')
