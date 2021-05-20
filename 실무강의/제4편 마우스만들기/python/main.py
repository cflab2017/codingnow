import serial
import time
import threading
import pyautogui
import tkinter as tk
# pip install serial
# pip install pyserial
# pip uninstall serial
#https://www.devicemart.co.kr/goods/view?no=1279487

seri = serial.Serial(port='COM9',
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS) 
###########################################
keybuffer = 0
def readSerial():
    global isT1Run
    global keybuffer
    while isT1Run:
        pass
        try:
            if seri.readable():
                res = seri.readline()
                res = res.decode()[:len(res)-1]
                print(res)
                if res.find('key') != -1:
                    res = res.replace("key=","")
                    key = int(res,16)
                    keybuffer = key
        except:
            pass
    print('stop thread1')

def mouseProcess():
    global isT2Run
    global keybuffer
    keybufferPre = 0
    key = 0
    moveOffset = 1
    while isT2Run:
        pass
        try:
            if keybuffer != keybufferPre:
                key = keybuffer
                keybufferPre = keybuffer
                print(key)
    #move
            x, y = 0, 0
            if key & 0x01:
                x -= moveOffset
            if key & 0x02:
                x += moveOffset
            if key & 0x04:
                y -= moveOffset
            if key & 0x08:
                y += moveOffset
            pyautogui.move(x,y)

            if x or y:
                if moveOffset < 100:
                    moveOffset *= 2
            else:
                moveOffset = 1
    #click   
            if key&0x10:
                pyautogui.leftClick()
            if key&0x20:
                pyautogui.rightClick()
            if key&0x40:
                pyautogui.scroll(200)
            if key&0x80:
                pyautogui.scroll(-200)
            key &= (~0x30);#0xCF#bnt은 한번만 동작하도록 삭제
        except:
            pass
        time.sleep(0.01)
    print('stop thread2')

###########################################
isT1Run = True
t1 = threading.Thread(target=readSerial)
t1.start()

isT2Run = True
t2 = threading.Thread(target=mouseProcess)
t2.start()
###########################################
win = tk.Tk()
win.title('[파이선] 아두이노 제어')
win.mainloop()
###########################################
#GUI 종료 후
seri.close()
isT1Run = False
isT2Run = False
time.sleep(0.5)
print('Finish')
