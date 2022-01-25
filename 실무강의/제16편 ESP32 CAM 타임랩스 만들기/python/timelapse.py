import cv2
import os

#pip install opencv-python

image_folder = 'images'
video_name = 'video.avi'

#1. 모든 이미지 파일의 파일명을 리스트로 변환
images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
# print(images)

#2. 첫번째 이미지의 프레임크기 정보를 가져온다.
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape
# print(width, height, layers)

#3. 비디오 생성
# *은 'D', 'I', 'V', 'X' 이렇게 문자열을 문자로
video = cv2.VideoWriter(video_name, 
                        cv2.VideoWriter_fourcc(*'DIVX'), 
                        100, 
                        (width, height))

#4. 이미지 파일을 하나씩 가져와서 비디오에 추가
for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

#5. 종료
cv2.destroyAllWindows()
video.release()
