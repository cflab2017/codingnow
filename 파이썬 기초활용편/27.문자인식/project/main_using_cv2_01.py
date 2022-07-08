import cv2
import numpy as np
import pytesseract

#pip install opencv-python
class find_text():
    path = {
        'tesseract': r'C:\\Program Files\\Tesseract-OCR\\tesseract',
        'output': './result/receipt_output_01.jpg'
    }
    margin = 5
###############################################################################
    def __init__(self):
        self.img = cv2.imread("./image/image.png")

###############################################################################
    def get_hulls(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        # cv2.imshow('gray', gray)
        # cv2.waitKey(0)
        mser = cv2.MSER_create()
        regions, _ = mser.detectRegions(gray)
        hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions]
        # print(hulls)
        # self.setRectangle(gray, hulls, (0, 255, 0), 1)
        # cv2.imshow('hulls_area', gray)
        # cv2.waitKey(0)
        return hulls

    def setRectangle(self, img, hulls, color, thickness):
        margin = self.margin
        for j, cnt in enumerate(hulls):
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(img,
                          (x-margin, y-margin),
                          (x + w + margin, y + h + margin),
                          color, thickness)
###############################################################################
    def leave_text_area(self, img):
        hulls = self.get_hulls(img)
        out_path = self.path['output']
        #검정색
        mask = np.zeros((img.shape[0], img.shape[1], 1), dtype=np.uint8)
        self.setRectangle(mask, hulls, (255, 255, 255), -1)
        # cv2.imshow("mask", mask)
        # cv2.waitKey(0)

        img_text = cv2.bitwise_and(img, img, mask=mask)
        # cv2.imshow("text area", img_text)
        cv2.imwrite(out_path, img_text)
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
# ocr_text.get_hulls(ocr_text.img)
ocr_text.leave_text_area(ocr_text.img)  # hulls 영역 찾기
ocr_text.get_text()#최종 이미지에서 문자 찾기