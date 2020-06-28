# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #                                                                                                  #
#                                                   _                           #
#    ___    ___    __ _   _ __ ___     ___   _ __   | |_       _ __    _   _    #
#   / __|  / _ \  / _` | | '_ ` _ \   / _ \ | '_ \  | __|     | '_ \  | | | |   #
#   \__ \ |  __/ | (_| | | | | | | | |  __/ | | | | | |_   _  | |_) | | |_| |   #
#   |___/  \___|  \__, | |_| |_| |_|  \___| |_| |_|  \__| (_) | .__/   \__, |   #
#                 |___/                                       |_|      |___/    #
#                                                                               #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
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

def segment(image, type, binarize_threshold):

    _, binarized_image = cv2.threshold(image, binarize_threshold, 255, cv2.THRESH_BINARY_INV)

    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(binarized_image, cv2.MORPH_OPEN, kernel, iterations = 2)

    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0

    output_image = image

    markers = cv2.watershed(cv2.cvtColor(image, cv2.COLOR_GRAY2RGB), markers)
    output_image[markers == -1] = 255

    return output_image
