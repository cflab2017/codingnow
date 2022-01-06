import cv2 #opencv
import urllib.request #para abrir y leer URL
import numpy as np

# python -m pip install opencv-python
#참고
#https://github.com/JhoelRN/ESP32-CAM-wireless-computer-vision-objects-detection
#https://pysource.com/2019/06/27/yolo-object-detection-using-opencv-with-python/
#weights download
#https://pjreddie.com/darknet/yolo/

url = 'http://192.168.0.2/cam-hi.jpg'
winName = 'ESP32 CAMERA'
infoPath = './infor/'

classNames = []
classFile = infoPath+'coco.names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

configPath = infoPath+'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt' #YOLO 환경설정파일
weightsPath = infoPath+'frozen_inference_graph.pb'#사전 훈련된 가중치들

cv2.namedWindow(winName,cv2.WINDOW_AUTOSIZE)
net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
#net.setInputSize(480,480)
# net.setInputSize(608, 608)
net.setInputScale(1.0/127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

while(1):
    try:
        #이미지 가져오기
        imgResponse = urllib.request.urlopen (url) #abrimos el URL
        imgNp = np.array(bytearray(imgResponse.read()),dtype=np.uint8)
        img = cv2.imdecode (imgNp,-1) #decodificamos
        # img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE) # vertical
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #black and white    

        #사물인식
        classIds, confs, bbox = net.detect(img,confThreshold=0.5)
        print(classIds,bbox)

        #사물인식된 경우 박스 및 테스트 입력
        if len(classIds) != 0:
            for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
                cv2.rectangle(img,box,color=(0,255,0),thickness = 3) #mostramos en rectangulo lo que se encuentra
                cv2.putText(img, classNames[classId-1], (box[0]+10,box[1]+30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0),2)
        cv2.imshow(winName,img) # mostramos la imagen
    except:
        pass

    #ESC key 입력
    tecla = cv2.waitKey(5) & 0xFF
    if tecla == 27:
        break
cv2.destroyAllWindows()
