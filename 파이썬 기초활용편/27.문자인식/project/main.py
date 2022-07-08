import pytesseract
import os
# pip install pillow
# pip install pytesseract
# pip install opencv-python

# 설치파일 다운로드 경로
# https://github.com/UB-Mannheim/tesseract/wiki

# 언어 학습 데이타 다운로드 경로
# https://github.com/tesseract-ocr/tessdata/

path_tesseract = r'C:\\Program Files\\Tesseract-OCR\\tesseract'

path_img = "./image/image.png"
# path_img = "./image/image_eng.png"

pytesseract.pytesseract.tesseract_cmd = path_tesseract
config = ('-l kor+eng --oem 3 --psm 11')
text = pytesseract.image_to_string(path_img, config=config)
print(text)
