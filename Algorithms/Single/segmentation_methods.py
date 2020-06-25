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

def RegionGrowing(image, portion, epsilon):
    x = portion[0][0]
    y = portion[0][1]
    cen_pix = image[x][y]

    output = np.zeros(np.shape(image), dtype=np.uint8)
    output[x][y] = 255
    while len(portion) > 0:
         xcd = portion[0][0]
         ycd = portion[0][1]
         for i in range(-1, 2):
              for j in range(-1, 2):
                absDiff = abs(int(cen_pix) - int(image[xcd + i][ycd + j]))
                if (i != 0 or j != 0) and output[xcd + i][ycd + j] != 255 and absDiff < epsilon:
                    output[xcd + i][ycd + j] = 255
                    portion.append([xcd + i, ycd + j])
         portion.pop(0)
    return output

def segment(image, portion, type, epsilon):
    RG = RegionGrowing(image, portion, epsilon)
    kernel = np.ones((19, 19), np.uint8)
    RG = cv2.morphologyEx(RG, cv2.MORPH_CLOSE, kernel, iterations=2)
    # Removing small regions that are not a part of lesion like corners
    segmented_image = RemoveUnwantedRegions(RG)
    cv2.imshow('Output', output)
    cv2.waitKey()

    return segmented_image
