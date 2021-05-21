import serial
import tkinter as tk

# pip install pyserial
# pip install serial
seri = serial.Serial(port='COM9',
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS) 

# while True:
#     if seri.readable():
#         res = seri.readline()
#         print(res.decode()[:len(res)-1])
#         break
# seri.write(bytes('on\n', encoding='ascii'))

####################################################
## GUI 생성하기
####################################################
class LedControl():
    commads = ['ON', 'OFF', 'BLINKING']

    def __init__(self, seri):
        self.win = tk.Tk()
        self.win.title('[파이선] 아두이노 LED 제어')
        self.seri = seri
        for i, comm in enumerate(self.commads):##버튼을 만든다.
            bt = tk.Button(self.win,text=comm,
                width=40, height=10, 
                bg='gray', fg='black',
                command=lambda cmd=comm: self.button_click(cmd)
                )
            bt.grid(column=i, row=0)

    def button_click(self, value):
        print(value)
        comm = value+'\n'
        self.seri.write(bytes(comm, encoding='ascii'))
        # ser.write(comm.encode())

#class 를 생성하면서 GUI를 나타낸다.
btn = LedControl(seri)
btn.win.mainloop()
