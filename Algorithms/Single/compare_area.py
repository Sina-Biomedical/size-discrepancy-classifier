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

# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#             PREPROCESSING METHODS [4](2/2)          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# HYPERPARAMETER  #        VALUE        # IMAGE TYPE  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# IMAGE CROPPING  # [0, 470] [100, 700] # STRAIN      #
# IMAGE RESIZING  # 0.4                 # STRAIN      #
# CLOSE SIZE      # 12                  # STRAIN      #
# CLOSE ITERS.    # 1                   # STRAIN      #
# MED. BLURRING   # 59                  # STRAIN      #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# IMAGE CROPPING  # [0, 470][100,700]   # B-MODE      #
# CLOSE SIZE      # 13                  # B-MODE      #
# CLOSE ITERS.    # 1                   # B-MODE      #
# BILAT. FILTER   # 13                  # B-MODE      #
# MED. BLURRING   # 25                  # B-MODE      #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#            LESION LOCATING METHODS [4](2/2)         #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# HYPERPARAMETER  #        VALUE        # IMAGE TYPE  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# THRESHOLD 1     # 193                 # STRAIN      #
# THRESHOLD 2     # 194                 # STRAIN      #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# THRESHOLD 1     # 193                 # B-MODE      #
# THRESHOLD 2     # 194                 # B-MODE      #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#            SEGMENTATION METHODS [12](6/6)           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# HYPERPARAMETER  #        VALUE        # IMAGE TYPE  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# BIN. THRESHOLD  # 84                   # STRAIN     #
# OPEN/DIL. SIZE  # 3                    # STRAIN     #
# OPEN ITERATIONS # 2                    # STRAIN     #
# DIL. ITERATIONS # 3                    # STRAIN     #
# DIST TRANSFORM  # 5                    # STRAIN     #
# FOREGR. THRESH. # 0.7                  # STRAIN     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# BIN. THRESHOLD  # 212                  # B-MODE     #
# OPEN/DIL. SIZE  # 3                    # B-MODE     #
# OPEN ITERATIONS # 2                    # B-MODE     #
# DIL. ITERATIONS # 3                    # B-MODE     #
# DIST TRANSFORM  # 5                    # B-MODE     #
# FOREGR. THRESH. # 0.7                  # B-MODE     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

import cv2
import numpy as np
from matplotlib import pyplot as plt

from preprocessing_methods import preprocess
from segmentation_methods import segment

def compare_area(image_directory):
    strain_image = image_directory + "strain.jpg"
    bmode_image = image_directory + "bmode.jpg"

    # Pre-Process Images @ preprocess.py
    strain_image_processed = preprocess(strain_image)
    bmode_image_processed = preprocess(bmode_image)

    # Show Pre-Processed Images
    plt.subplot(221), plt.imshow(cv2.imread(strain_image), cmap='gray')
    plt.subplot(222), plt.imshow(strain_image_processed, cmap='gray')
    plt.subplot(223), plt.imshow(cv2.imread(bmode_image), cmap='gray')
    plt.subplot(224), plt.imshow(bmode_image_processed, cmap='gray')
    plt.show()

    # Segment Images @ segment.py
    strain_area, strain_segmented,_ = segment(strain_image_processed, 'strain', 84)
    bmode_area, bmode_segmented,_ = segment(bmode_image_processed, 'b-mode', 212)

    # Show Segmented Images
    plt.subplot(221), plt.imshow(cv2.imread(strain_image), cmap='gray')
    plt.subplot(222), plt.imshow(strain_segmented, cmap='gray')
    plt.subplot(223), plt.imshow(cv2.imread(bmode_image), cmap='gray')
    plt.subplot(224), plt.imshow(bmode_segmented, cmap='gray')
    plt.show()

    print("Strain Area: " + str(strain_area))
    print("B-Mode Area: " + str(bmode_area))
    print("Area Ratio: "  + str(strain_area/bmode_area))

    return strain_area, bmode_area

# 10/58/09 | 234th Frame
compare_area("../../Data/Frames/Malignant/10-58-09/235/")
