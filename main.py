#######################
# This is a simple script to perform OCR (Optical Character Recognition)
# It is still a work in progress
# be careful when using it with a very large image, it will freeze your pc, 800x600 recomended
# SciKit work with float, uint8 and bool / RGB and float64 [0,1]
# openCV work with uint8, float32 / BGR and uint8 [0,255]
########################

import os
os.environ["QT_LOGGIN_RULES"] = "qt.qpa.*=False"

import utils

import cv2, sys, re, json
import pytesseract
from pytesseract import Output
from skimage import data, filters, color
import numpy as np

#Uncoment this line if you are in windows.
#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#This part is for linux
pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

# Calling the image and it`s metadata
img = cv2.imread("resources/ticket.jpg")

height, width, _ = img.shape
max_width, min_width = 1500, 900 #The resolution of our new image, important to process.
config_tess = r""" --oem 1 --psm 6 """

reescaled = True

print(f"Image dimensions: {width}x{height}")


if width > max_width:
    utils.rescaling(max_width, width, height, img)
elif width > min_width:
    utils.rescaling(min_width, width, height, img)
else:
    print("the image doesnt need to reescale")
    reescaled = False

if reescaled:
    cv2.imwrite("resources/ocr_ready.png", img)

# Scale again the originall to ROI selection

img = utils.Region_Of_Interest_window(img)

# Filters for tesseract

mask_uint8 = utils.rgb_to_uint8Mask(img)

# Showing the ressult, tesseract computing and printing

cv2.imshow("tick2", mask_uint8)
cv2.imwrite("resources/otsu_thresh.png", mask_uint8)

while True:
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

#----------------------------------------------------------------------

# TODO resolve this thing failing on the "warpAffine" function of cv2

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5,5), 0)

_, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,5))
th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel)

contours, _ = cv2.findContours(
    th,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)



contour = max(contours, key=cv2.contourArea)

rect = cv2.minAreaRect(contour)
angle = rect[2]

print(angle)

if rect[1][0] < rect[1][1]:
    angle = angle + 90

box = cv2.boxPoints(rect)
box = np.intp(box)

cv2.drawContours(img, [box], 0, (0,255,0), 1)



cv2.imwrite("resources/ocr_rotated.png", img)
cv2.imwrite("resources/ocr_rotated2.png", th)

#------------------------------------------------------------------------

ticket_on_text = pytesseract.image_to_string(mask_uint8, config=config_tess, lang="spa")
ticket_on_dict = pytesseract.image_to_data(mask_uint8, config=config_tess,output_type=Output.DICT, lang="spa")

#showing rectangles on detected words

debug = mask_uint8.copy()

utils.rect_word_detection(ticket_on_dict, debug)


with open("resources/output.txt", "w") as file_tess:
    file_tess.write(ticket_on_text)

with open("resources/output2.json", "w") as file_tess:
    json.dump(ticket_on_dict,file_tess, indent=4)
