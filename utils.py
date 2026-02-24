import json, cv2
from skimage import data, filters, color
import numpy as np


def json_to_ordered_data_txt(raw_json_data):
# TODO Please add docstring.

    try:
        with open("resources/output2.json") as json_raw:
            raw_json_data = json.loads(json_raw.read())
    except:
        print("Exception ocurred trying to load")
        raise Exception

    try:
        json_keys = raw_json_data.keys()
        #print(json_keys)

        with open("better_data.txt", "w") as file:
            for i in range(len(raw_json_data["level"])):
                line = ""
                for key in json_keys:
                    word = f"{key}: {raw_json_data[key][i]} "
                    line += word

                file.write(line)
                file.write("\n")
    except:
        print("Exception ocurred trying to interpreting json/wtitting on txt")
        raise Exception
    
    
def rescaling(new_width, original_width, original_height, img):
# TODO Please add docstring

    print(f"Image dimensions: {original_width}x{original_height}")

    scale = (new_width / original_width) # Scale number
    new_width, new_height = int(original_width * scale), int(original_height * scale) # New resolution calc
    img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA) # Resize by OpenCV
    
    print(f"image rescaled: {(new_width / original_width)}")


def Region_Of_Interest_window(img, scale=50):
# TODO Please add docstring

    w_esc = int(img.shape[1] * scale / 100)
    h_esc = int(img.shape[0] * scale / 100)
    dim = (w_esc, h_esc)
    img_small_for_ROI = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    selection = cv2.selectROI("Select the part to proccess", img_small_for_ROI, fromCenter = False, showCrosshair = True)
    x, y, w, h = selection
    x = int(x * 100 / scale)
    y = int(y * 100 / scale)
    w = int(w * 100 / scale)
    h = int(h * 100 / scale)
    roi_selection = img[int(y):int(y+h), int(x):int(x+w)]

    cv2.destroyAllWindows()

    return roi_selection

def rgb_to_uint8Mask(img):
# TODO Please add docstring

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_gray = color.rgb2gray(img_rgb)

    image_gauss = filters.gaussian(img_gray, sigma = 1)
    umbral = filters.threshold_otsu(image_gauss)
    mask = image_gauss > umbral

    mask_uint8 = (mask * 255).astype(np.uint8)

    return mask_uint8

def rect_word_detection(string,img):
# TODO Please add docstring

    try:
        for i in range(len(string["text"])):
            if string["level"][i] != 5:
                continue

            x = string["left"][i]
            y = string["top"][i]
            w = string["width"][i]
            h = string["height"][i]

            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 1)

        cv2.imwrite("debug_boxes.png", img)
    except:
        print("something wrong ocurred interpreting json results")
        raise Exception