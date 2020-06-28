# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                               #
#   _ __    _ __    ___   _ __    _ __    ___     ___    ___   ___   ___       _ __    _   _    #
#  | '_ \  | '__|  / _ \ | '_ \  | '__|  / _ \   / __|  / _ \ / __| / __|     | '_ \  | | | |   #
#  | |_) | | |    |  __/ | |_) | | |    | (_) | | (__  |  __/ \__ \ \__ \  _  | |_) | | |_| |   #
#  | .__/  |_|     \___| | .__/  |_|     \___/   \___|  \___| |___/ |___/ (_) | .__/   \__, |   #
#  |_|                   |_|                                                  |_|      |___/    #
#                                                                                               #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Est. June 20, 2020 (6/20/2020)  #
# # # # # # # # # # # # # # # # # #
# SINA BIOMEDICAL RESEARCH GROUP  #
#   +-- S. Kaisar Alam (PI)       #
#   +-- Areeq I. Hasan (Lead)     #
#   +-- Sarina M. Hasan           #
#   +-- Raiyah Z. Ahmed           #
#   +-- Wasi S. Ahmed             #
# # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# compare_area()                                                                              #
# Computes the ratio between the area of a lesion in a given b-mode and strain image pair.    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# @ params                                                                                    #
#   +-- image_directory: (string) | Path to the directory containing strain.png & b-mode.png  #
# @ output                                                                                    #
#   +-- area_ratio:      (double) | the area ratio between strain and b-mode masks.           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import cv2
import numpy as np
from matplotlib import pyplot as plt

mouse_clicks = []

def on_mouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print('Seed: ' + str(x) + ', ' + str(y))
    mouse_clicks.append((y, x))

# Best Image --> As close to a completely black lesion and completely white and uniform surrounding as possible.
# *NOTE* More important than retaining the shape of the lesion is retaining the size of the lesion.

def preprocess(image_filepath):

    image = cv2.imread(image_filepath, 0)
    image_type = "strain" if image_filepath[-5:] == "n.jpg" else "bmode"

    if image_type == "strain":
        # IMAGE CROPPING // Height: 0 --> 470, Width: 100 --> 700
        processed_image = image[0:470, 100:700]

        # IMAGE RESIZING // 0.4
        processed_image = cv2.resize(processed_image, (0,0), fx=0.4, fy=0.4)

        # MORPHOLOGICAL CLOSING // 11
        kernel = np.ones((11, 11), np.uint8)
        processed_image = cv2.morphologyEx(processed_image, cv2.MORPH_CLOSE, kernel, iterations=1)

        # BILATERIAL FILTER // 79
        # image = cv2.bilateralFilter(image,79,75,75)

        # NLM DENOISING // 10
        processed_image = cv2.fastNlMeansDenoising(processed_image, None, 10, 7, 1)

        # MEDIAN BLURRING // 59
        processed_image = cv2.medianBlur(processed_image, 59)

        # ADAPTIVE HISTOGRAM EQUALIZATION // 2.0
        # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        # image = clahe.apply(image)
    else:

        # IMAGE CROPPING // Height: 0 --> 470, Width: 100 --> 700
        processed_image = image[0:595, 100:700]

        # IMAGE RESIZING // 0.4
        # processed_image = cv2.resize(processed_image, (0,0), fx=0.4, fy=0.4)

        # MORPHOLOGICAL CLOSING // 11
        kernel = np.ones((13, 13), np.uint8)
        processed_image = cv2.morphologyEx(processed_image, cv2.MORPH_CLOSE, kernel, iterations=1)

        # BILATERAL FILTER // 79 -- Edge-Preserving Denoise
        processed_image = cv2.bilateralFilter(processed_image,13,75,75)

        # NLM DENOISING // 10 -- Denoise
        # processed_image = cv2.fastNlMeansDenoising(processed_image, None, 10, 7, 1)

        # MEDIAN BLURRING // 59 -- Denoise
        # processed_image = cv2.medianBlur(processed_image, 59)

        # HISTOGRAM EQUALIZATION -- Intensifies/Increases Contrast
        # processed_image = cv2.equalizeHist(processed_image)



    plt.subplot(121), plt.imshow(image, cmap='gray'), plt.title('Original Image')
    plt.subplot(122), plt.imshow(processed_image, cmap='gray'), plt.title('Processed Image')
    plt.show()

    cv2.namedWindow('Input')
    cv2.setMouseCallback('Input', on_mouse, 0, )
    cv2.imshow('Input', processed_image)
    cv2.waitKey()
    seed = mouse_clicks[-1]
    seed_x = seed[0]
    seed_y = seed[1]
    rows = processed_image.shape[0]
    cols = processed_image.shape[1]
    # Find the center
    cen_pix = processed_image[seed_x][seed_y]
    # New matrix that will hold segmented image
    # Matrix to hold all region pixels
    portion = [[seed_x, seed_y]]

    return(processed_image, portion)

preprocess("../../Data/Frames/Malignant/10-58-09/234/bmode.jpg")
