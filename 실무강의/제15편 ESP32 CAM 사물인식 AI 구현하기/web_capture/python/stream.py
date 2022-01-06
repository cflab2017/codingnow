import cv2
import PIL.Image, PIL.ImageTk
from tkinter import *
import numpy as np
from urllib.request import urlopen

class App:
    def __init__(self, window):
        #화면 생성
        self.width, self.height = 320, 320
        self.window = window
        self.window.geometry("320x320")
        self.window.title("Read ESP32-CAM")
        self.window.bind('<Key>', self.keyPressed)
        self.buffer = b''
        #esp-cap stream
        url = "http://192.168.0.2:81/stream" #Your url
        self.stream = urlopen(url)

        self.canvas = Canvas(window, width = self.width, height = self.height)
        self.canvas.pack()
        self.delay = 1
        self.isCaputure = 0
        self.update()
        self.window.mainloop()

    def keyPressed(self, event):
        print(event.char)
        if event.char == 'a':#현재 화면을 사진으로 저장
            self.isCaputure = 1
            
        if event.char == 'q':#종료하기
            self.window.destroy()

    def update(self):
        while True:
            #촬영 데이타 받아오기
            self.buffer += self.stream.read(2560)
            head = self.buffer.find(b'\xff\xd8')
            end = self.buffer.find(b'\xff\xd9')
            try:
                if head > -1 and end > -1:
                    #촬영 데이타를 jpg로 변환하기
                    jpg = self.buffer[head:end+2]
                    self.buffer = self.buffer[end+2:]
                    img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    img = cv2.resize(img, (320, 320))
                    # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)  # vertical
                    #사진 파일로 저장하기
                    if self.isCaputure:
                        cv2.imwrite('capture' + ".jpg", img)
                        self.isCaputure = 0
                    self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(img))
                    self.canvas.create_image(0, 0, image = self.photo, anchor = NW)
                    break
            except:
                pass
        self.window.after(ms=self.delay, func=self.update)

App(Tk())
