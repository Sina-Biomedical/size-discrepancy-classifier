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

# Best Image --> As close to a completely black lesion and completely white and uniform surrounding as possible.
# *NOTE* More important than retaining the   shape of the lesion is retaining the size of the lesion.

def preprocess(image, image_type, hyperparameters):
    if image_type == "strain":

        # MORPHOLOGICAL CLOSING // 11
        closing_size = hyperparameters['strain']['preprocessing_methods']['closing_size']
        closing_iters = hyperparameters['strain']['preprocessing_methods']['closing_iters']
        kernel = np.ones((closing_size, closing_size), np.uint8)
        processed_image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=closing_iters)

        # MEDIAN BLURRING // 59
        med_blurring = hyperparameters['strain']['preprocessing_methods']['med_blurring']
        processed_image = cv2.medianBlur(processed_image, med_blurring)

        processed_image = cv2.equalizeHist(processed_image)

        med_blurring = hyperparameters['strain']['preprocessing_methods']['med_blurring']
        processed_image = cv2.medianBlur(processed_image, med_blurring)

    else:

        # MORPHOLOGICAL CLOSING // 11
        closing_size = hyperparameters['bmode']['preprocessing_methods']['closing_size']
        closing_iters = hyperparameters['bmode']['preprocessing_methods']['closing_iters']
        kernel = np.ones((closing_size, closing_size), np.uint8)
        processed_image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=closing_iters)

        # BILATERAL FILTER // 79 -- Edge-Preserving Denoise
        bilat_filter = hyperparameters['bmode']['preprocessing_methods']['bilat_filter']
        processed_image = cv2.bilateralFilter(processed_image, bilat_filter, 75, 75)

        # HISTOGRAM EQUALIZATION -- Intensifies/Increases Contrast
        processed_image = cv2.equalizeHist(processed_image)

        # # MEDIAN BLURRING // 59 -- Denoise
        med_blurring = hyperparameters['bmode']['preprocessing_methods']['med_blurring']
        processed_image = cv2.medianBlur(processed_image, med_blurring)

        # HISTOGRAM EQUALIZATION -- Intensifies/Increases Contrast
        processed_image = cv2.equalizeHist(processed_image)

    return processed_image
