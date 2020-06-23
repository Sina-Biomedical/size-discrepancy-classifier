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

def preprocess(image_filepath):

    # Determine whether image is elastogram or B-Mode image
    type = 'strain' if image_filepath[-5:] == 'n.jpg' else 'bmode'

    if type == 'bmode':
        pass
    elif type == 'strain':
        image = cv2.imread(image_filepath, 0)
        blur = cv2.fastNlMeansDenoising(image, None,150,7,21)
        hist_eq = cv2.equalizeHist(blur)
        segmented, thresh = cv2.threshold(gray,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)

        # blur = cv2.GaussianBlur(image, (11, 11), 0)

        plt.subplot(221), plt.imshow(image, 'gray'), plt.title('Original')
        plt.xticks([]), plt.yticks([])
        plt.subplot(222), plt.imshow(blur, 'gray'), plt.title('Blurred')
        plt.xticks([]), plt.yticks([])
        plt.subplot(223), plt.imshow(hist_eq, 'gray'), plt.title('Hist EQ')
        plt.xticks([]), plt.yticks([])
        plt.subplot(224), plt.imshow(cv2.fastNlMeansDenoising(image, None, 10, 19, 21)), plt.title('Blurred')
        plt.xticks([]), plt.yticks([])
        # plt.subplot(125), plt.imshow(cv2.fastNlMeansDenoising(image, None,30,7,21)), plt.title('Blurred')
        # plt.xticks([]), plt.yticks([])
        # plt.subplot(126), plt.imshow(cv2.fastNlMeansDenoising(image, None,50,7,21)), plt.title('Blurred')
        # plt.xticks([]), plt.yticks([])
        plt.show()


preprocess("../../Data/Frames/Malignant/10-58-09/234/strain.jpg")
