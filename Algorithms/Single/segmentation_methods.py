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

def fill_contours(arr):
    return np.maximum.accumulate(arr,1) & \
           np.maximum.accumulate(arr[:,::-1],1)[:,::-1]

def segment(image, image_type, binarize_threshold):

    if image_type == 'strain':

        # BINARIZE STRAIN IMAGE // binarize_threshold
        _, binarized_image = cv2.threshold(image, binarize_threshold, 255, cv2.THRESH_BINARY_INV)

        # MORPHOLOGICAL OPENING/DILATION // ITERATION = 3
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(binarized_image, cv2.MORPH_OPEN, kernel, iterations = 2)

        #
        sure_bg = cv2.dilate(opening, kernel, iterations=3)

        # DIST TRANSFORM // 5
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)

        _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
        sure_fg = np.uint8(sure_fg)

        unknown = cv2.subtract(sure_bg, sure_fg)

        _, markers = cv2.connectedComponents(sure_fg)
        markers = markers + 1
        markers[unknown == 255] = 0

        output_image = image

        markers = cv2.watershed(cv2.cvtColor(image, cv2.COLOR_GRAY2RGB), markers)
        binarized_image = fill_contours(markers)
        output_image[markers == -1] = 255

        strain_area = np.sum(binarized_image == 2) * 6.25

        plt.imshow(binarized_image, cmap='gray')
        plt.show()

        return strain_area, np.pad(cv2.resize(output_image, (0,0), fx=2.5, fy=2.5), [(0, 130), (100, 100)], mode='constant', constant_values=0), np.pad(np.resize(binarized_image, (tuple(int(float(i) * 2.5) for i in binarized_image.shape))), [(0, 130), (100, 100)], mode='constant', constant_values=0)
    else:
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
        binarized_image = fill_contours(markers)
        output_image[markers == -1] = 255

        plt.imshow(binarized_image, cmap='gray')
        plt.show()

        bmode_area = np.sum(binarized_image == 2)

        return bmode_area, output_image, np.pad(binarized_image, [(0, 0), (130, 130)], mode='constant', constant_values=0)
