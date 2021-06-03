import serial

import tkinter as tk
import time
import threading

# pip install serial
# pip install pyserial
# pip uninstall serial
images = ['0042A5000000423C',
          '0042A5420000423C',
          '0042A50000003C42',
          '0066998181422418']

seri = serial.Serial(port='COM8',
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS) 

def sendToAruino(img):
    comm = 'LED'+images[img]
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
        self.win.title('[파이선] 아두이노 Matrix LED 제어')
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
            sendToAruino(int(value))

# #thread 2  함수
def TH_sendCmdAuto():
    global isT1Run
    index = 0
    while isT1Run:
        if tool.isAuto:            
            sendToAruino(index)
            index = (index+1) % len(images)
        time.sleep(0.5)
    print('stop2 thread')

#GUI class 생성
tool = LedControl()

isT1Run = True
t2 = threading.Thread(target=TH_sendCmdAuto)
t2.start()

#GUI 실행
tool.win.mainloop()

#GUI 종료 후
isT1Run = False
time.sleep(0.5)
seri.close()
print('Finish')
