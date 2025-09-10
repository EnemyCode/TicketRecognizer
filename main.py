#######################
# This is a simple script to perform OCR (Optical Character Recognition)
# It is still a work in progress
# be careful when using it with a very large image, it will freeze your pc, 800x600 recomended
#######################

import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
img = cv2.imread("ticket.jpg")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3,3), 0)
thresh = cv2.adaptiveThreshold(
    blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2
)

cv2.imshow("Ticket", thresh)
cv2.waitKey(0)

text = pytesseract.image_to_string(thresh, lang="spa")
print(text)
