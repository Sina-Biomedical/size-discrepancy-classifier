import cv2
import numpy as np
from matplotlib import pyplot as plt
import copy

def find_lesion(image_src, hyperparameters):
    gray = image_src

    bin_threshold = hyperparameters['bmode']['lesion_locating_methods']['bin_threshold']
    ret, gray = cv2.threshold(gray, bin_threshold, 255, 0)

    contours, hierarchy = cv2.findContours(gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    largest_area = sorted(contours, key=cv2.contourArea)[-1]
    mask = np.zeros(image_src.shape, np.uint8)
    cv2.drawContours(mask, [largest_area], 0, (255,255,255,255), -1)
    dst = cv2.bitwise_and(image_src, mask)
    mask = 255 - mask
    roi = cv2.add(dst, mask)

    # plt.imshow(roi, cmap='gray')
    # plt.show()

    return roi
