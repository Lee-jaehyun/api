import base64
import time, datetime
import re
import cv2
import numpy as np
import pytesseract
import json
from collections import OrderedDict
from deskew import determine_skew
from mser import mser_process
from angle4 import rotate

from PIL import Image
from io import BytesIO


def ocr_prsc(base64_data): #base64_data
    start = time.time()

    data = BytesIO(base64.b64decode(base64_data))

    img = Image.open(data)
   # img = cv2.imread("../../Desktop/image3.jpeg")
   # img = cv2.resize(img, dsize=(960, 1280), interpolation=cv2.INTER_AREA)
    image = np.array(img)
    image = cv2.resize(image, dsize=(960, 1280), interpolation=cv2.INTER_AREA)

   # w, h = image.shape[:2]
   # print(h)
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


#angle = determine_skew(grayscale)
    angle = determine_skew(grayscale)
    print("[INFO]==>", angle)

    if (angle < -59) or (angle > 80):
        rotated = image
    else:
        rotated = rotate(image, angle, (0, 0, 0))

  #  cv2.imshow('rotated', rotated)
  #  cv2.waitKey(0)

    end_angle = time.time()
    sec = (end_angle - start)
    print('[INFO] ==> process_angle :', datetime.timedelta(seconds=sec))

    grayscale1 = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
 #   src_bin = cv2.adaptiveThreshold(grayscale, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 55, 5)

 #   contours, hierarchy = cv2.findContours(src_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

#    mask = np.zeros(src_bin.shape, dtype=np.uint8)

    output = []


    grayscale1 = cv2.resize(grayscale1, None, fx=2.5, fy=2.5, interpolation=cv2.INTER_CUBIC)
  #  thr = cv2.threshold(grayscale1, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    start_ocr = time.time()

    custom_config = r'--oem 1 --psm 6'  # -c tessedit_char_whitelist=.0123456789
    text = pytesseract.image_to_string(grayscale1, lang=None, config=custom_config)

    text = re.findall(r'\d+', text)
    output.append(text)
    end_ocr = time.time()
    sec2 = (end_ocr - start_ocr)
    print('[INFO] ==> OCR_process :', datetime.timedelta(seconds=sec2))
    sec3 = (end_ocr - start)
    print('[INFO] ==> Total_process :', datetime.timedelta(seconds=sec3))

    return output



if __name__=="__main__":
    text = ocr_prsc()
    print(text)


#    file_data = OrderedDict()
#    file_data['text'] = output







