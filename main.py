#######################
# This is a simple script to perform OCR (Optical Character Recognition)
# It is still a work in progress
# be careful when using it with a very large image, it will freeze your pc, 800x600 recomended
#######################

import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
img = cv2.imread("ticket2.jpg")

height, width, _ = img.shape
max_width, min_width = 1200, 800

print(f"Image dimensions: {width}x{height}")

if width > max_width:
    scale = (max_width / width)
    new_width, new_height = int(width * scale), int(height * scale)
    img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
    print(f"image reduced: {(max_width / width)}")
    reescaled = True
elif width > min_width:
    scale = (min_width / width)
    new_width, new_height = int(width * scale), int(height * scale)
    img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
    print(f"image reduced: {(max_width / width)}")
    reescaled = True
else:
    print("the image doesnt need to reescale")
    reescaled = False

if reescaled:
    cv2.imwrite("ocr_ready.png", img)

selection = cv2.selectROI("Select the part to proccess", img, fromCenter = False, showCrosshair = True)
x, y, w, h = selection
roi_selection = img[int(y):int(y+h), int(x):int(x+w)]

gray = cv2.cvtColor(roi_selection, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3,3), 0)
thresh = cv2.adaptiveThreshold(
    blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2
)

cv2.imshow("Ticket", thresh)
cv2.waitKey(0)

text = pytesseract.image_to_string(thresh, lang="spa")
print(text)
