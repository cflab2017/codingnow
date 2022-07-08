import cv2
import numpy as np
import pytesseract

#pip install opencv-python
class find_text():
    path = {
        'tesseract': r'C:\\Program Files\\Tesseract-OCR\\tesseract',
        'output': './result/receipt_output_02.jpg'
    }
###############################################################################
    def __init__(self):
        self.img = cv2.imread("./image/image.png")
###############################################################################
    def showOnlyOneColor(self,rgb_key):
        out_path = self.path['output']
        img = self.img
        # cv2.imshow("OneColor clone", img)
        r = int(rgb_key[0])
        g = int(rgb_key[1])
        b = int(rgb_key[2])
        rgb_low = np.array([r-1, g-1, b-1])
        rgb_high = np.array([r, g, b])
        mask = cv2.inRange(img, rgb_low, rgb_high)
        # cv2.imshow("OneColor mask", mask)
        cv2.imwrite(out_path, mask)
        # cv2.waitKey(0)
###############################################################################
    def get_text(self):
        path_img = self.path['output']
        pytesseract.pytesseract.tesseract_cmd = self.path['tesseract']
        config = ('-l kor+eng --oem 3 --psm 11')
        text = pytesseract.image_to_string(path_img, config=config)
        print('==========텍스트 인식 결과==========')
        print(text)

ocr_text = find_text()
ocr_text.showOnlyOneColor([242, 242, 242])  # 배경을 제외한 영역 검정으로
ocr_text.get_text()#최종 이미지에서 문자 찾기