#######################
# This is a simple script to perform OCR (Optical Character Recognition)
# It is still a work in progress
# be careful when using it with a very large image, it will freeze your pc, 800x600 recomended
# SciKit work with float, uint8 and bool / RGB and float64 [0,1]
# openCV work with uint8, float32 / BGR and uint8 [0,255]
########################

import cv2, sys
import pytesseract
from skimage import data, filters, color
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Calling the image and it`s metadata
img = cv2.imread("ticket2.jpg")

height, width, _ = img.shape
max_width, min_width = 3000, 800
config_tess = r"--oem 1 --psm 6"


print(f"Image dimensions: {width}x{height}")

# Scaling for better dettection for tesseract

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
    print(f"image rescaled: {(max_width / width)}")
    reescaled = True
else:
    print("the image doesnt need to reescale")
    reescaled = False

if reescaled:
    cv2.imwrite("ocr_ready.png", img)

# Scale again the originall to ROI selection

scale = 20
w_esc = int(img.shape[1] * scale / 100)
h_esc = int(img.shape[0] * scale / 100)
dim = (w_esc, h_esc)
img_smal_for_ROI = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

selection = cv2.selectROI("Select the part to proccess", img_smal_for_ROI, fromCenter = False, showCrosshair = True)
x, y, w, h = selection
x = int(x * 100 / scale)
y = int(y * 100 / scale)
w = int(w * 100 / scale)
h = int(h * 100 / scale)
roi_selection = img[int(y):int(y+h), int(x):int(x+w)]

cv2.destroyAllWindows()

# Filters for tesseract

img_rgb = cv2.cvtColor(roi_selection, cv2.COLOR_BGR2RGB)
img_gray = color.rgb2gray(img_rgb)

image_gauss = filters.gaussian(img_gray, sigma = 0)
umbral = filters.threshold_otsu(image_gauss)
mask = image_gauss > umbral

mask_uint8 = (mask * 255).astype(np.uint8)

# Showing the ressult, tesseract computing and printing

cv2.imshow("Ticket", mask_uint8)
cv2.imwrite("otsu_thresh.png", mask_uint8)

while True:
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

text = pytesseract.image_to_string(mask_uint8, config=config_tess, lang="spa")
print(text)
