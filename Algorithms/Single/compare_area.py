# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                                                     #
#   ___    ___    _ __ ___    _ __     __ _   _ __    ___            __ _   _ __    ___    __ _       _ __    _   _   #
#  / __|  / _ \  | '_ ` _ \  | '_ \   / _` | | '__|  / _ \  _____   / _` | | '__|  / _ \  / _` |     | '_ \  | | | |  #
# | (__  | (_) | | | | | | | | |_) | | (_| | | |    |  __/ |_____| | (_| | | |    |  __/ | (_| |  _  | |_) | | |_| |  #
#  \___|  \___/  |_| |_| |_| | .__/   \__,_| |_|     \___|          \__,_| |_|     \___|  \__,_| (_) | .__/   \__, |  #
#                            |_|                                                                     |_|      |___/   #
#                                                                                                                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
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

from preprocessing_methods import preprocess
from segmentation_methods import segment

def compare_area(image_directory):
    strain_image = image_directory + "strain.jpg"
    bmode_image = image_directory + "bmode.jpg"

    # Pre-process Images @ preprocess.py
    strain_image_processed = preprocess(strain_image)
    bmode_image_processed = preprocess(bmode_image)

    plt.subplot(221), plt.imshow(cv2.imread(strain_image), cmap='gray')
    plt.subplot(222), plt.imshow(strain_image_processed, cmap='gray')
    plt.subplot(223), plt.imshow(cv2.imread(bmode_image), cmap='gray')
    plt.subplot(224), plt.imshow(bmode_image_processed, cmap='gray')
    plt.show()

    # Segment Images @ segment.py
    strain_area, strain_segmented,_ = segment(strain_image_processed, 'strain', 84)
    bmode_area, bmode_segmented,_ = segment(bmode_image_processed, 'b-mode', 212)

    print("Strain Area: " + str(strain_area))
    print("B-Mode Area: " + str(bmode_area))

    plt.subplot(221), plt.imshow(cv2.imread(strain_image), cmap='gray')
    plt.subplot(222), plt.imshow(strain_segmented, cmap='gray')
    plt.subplot(223), plt.imshow(cv2.imread(bmode_image), cmap='gray')
    plt.subplot(224), plt.imshow(bmode_segmented, cmap='gray')
    plt.show()

    # # Compute the area ratio from the images
    # strain_area = sum(strain_segmented)
    # bmode_area = sum(bmode_segmented)
    # area_ratio = strain_area / bmode_area
    #
    # return area_ratio

# 10/58/09 | 234th Frame
compare_area("../../Data/Frames/Malignant/10-58-09/235/")
