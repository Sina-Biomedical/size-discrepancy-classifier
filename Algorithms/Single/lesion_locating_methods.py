import cv2
import numpy as np
from matplotlib import pyplot as plt
import copy

def find_lesion(image, hyperparameters):

    # THRESHOLD IMAGE
    bin_threshold = hyperparameters['bmode']['lesion_locating_methods']['bin_threshold']
    ret, binarized_image = cv2.threshold(image, bin_threshold, 255, 0)

    # FIND IMAGE CONTOURS
    contours, hierarchy = cv2.findContours(binarized_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # FIND LARGEST CONTOUR
    largest_area = sorted(contours, key=cv2.contourArea)[-1]
    mask = np.zeros(image.shape, np.uint8)

    # MASK IMAGE W/ LARGEST CONTOUR
    cv2.drawContours(mask, [largest_area], 0, (255,255,255,255), -1)
    dst = cv2.bitwise_and(image, mask)
    mask = 255 - mask
    roi = cv2.add(dst, mask)

    # plt.imshow(roi, cmap='gray')
    # plt.show()

    return roi
