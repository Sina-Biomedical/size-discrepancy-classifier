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

clicks = []

def on_mouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print('Seed: ' + str(x) + ', ' + str(y))
    clicks.append((y, x))

def preprocess(image_filepath, image_type):
    image = cv2.imread(image_filepath, 0)
    image = cv2.resize(image, (0,0), fx=0.5, fy=0.5) 
    # cv2.imshow('Original Image', orginalImg)
    kernel = np.ones((9, 9), np.uint8)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=1)
    image = cv2.medianBlur(image, 19)
    cv2.namedWindow('Input')
    cv2.setMouseCallback('Input', on_mouse, 0, )
    cv2.imshow('Input', image)
    cv2.waitKey()
    seed = clicks[-1]
    x = seed[0]
    y = seed[1]
    rows = image.shape[0]
    cols = image.shape[1]
    # Find the center
    cen_pix = image[x][y]
    # New matrix that will hold segmented image
    # Matrix to hold all region pixels
    portion = [[x, y]]

    return(image, portion)
