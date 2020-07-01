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

# hyperparameters = {
#     'strain': {
#         'preprocessing_methods': {
#             'image_cropping': [0, 470, 100, 700],
#             'image_resizing':  0.4,
#             'closing_size'  :  12,
#             'closing_iters' :  1,
#             'med_blurring'  :  59
#         },
#         'lesion_locating_methods': {
#             'threshold_1'   :  193,
#             'threshold_2'   :  194,
#         },
#         'segmentation_methods': {
#             'bin_threshold' :  84,
#             'open/dil_size' :  3,
#             'open_iters'    :  2,
#             'dil_iters'     :  3,
#             'dist_transform':  5,
#             'fg_thresh'     :  0.7
#         },
#     },
#     'bmode': {
#         'preprocessing_methods': {
#             'image_cropping': [0, 600, 100, 700],
#             'image_resizing': 0.4,
#             'closing_size'  : 13,
#             'closing_iters' : 1,
#             'bilat_filter'  : 13,
#             'med_blurring'  : 25
#         },
#         'lesion_locating_methods': {
#             'threshold_1'   : 193,
#             'threshold_2'   : 194
#         },
#         'segmentation_methods': {
#             'bin_threshold' : 212,
#             'open/dil_size' : 3,
#             'open_iters'    : 2,
#             'dil_iters'     : 3,
#             'dist_transform': 5,
#             'fg_thresh'     : 0.7
#         }
#     }
# }

def segment(image, image_type, hyperparameters):

    if image_type == 'strain':

        # IMAGE THRESHOLDING
        binarize_threshold = hyperparameters['strain']['segmentation_methods']['bin_threshold']
        _, binarized_image = cv2.threshold(image, binarize_threshold, 255, cv2.THRESH_BINARY_INV)

        # MORPHOLOGICAL OPENING/DILATION
        open_dil_size = hyperparameters['strain']['segmentation_methods']['open/dil_size']
        open_iters = hyperparameters['strain']['segmentation_methods']['open_iters']
        dil_iters = hyperparameters['strain']['segmentation_methods']['dil_iters']

        # DETERMINE SURROUNDING TISSUE
        kernel = np.ones((open_dil_size, open_dil_size), np.uint8)
        opening = cv2.morphologyEx(binarized_image, cv2.MORPH_OPEN, kernel, open_iters)
        sure_bg = cv2.dilate(opening, kernel, dil_iters)

        # DISTANCE TRANSFORM
        dist_transform_param = hyperparameters['strain']['segmentation_methods']['dist_transform']
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, dist_transform_param)

        fg_threshold = hyperparameters['strain']['segmentation_methods']['fg_thresh']
        _, sure_fg = cv2.threshold(dist_transform, fg_threshold * dist_transform.max(), 255, 0)
        sure_fg = np.uint8(sure_fg)

        unknown = cv2.subtract(sure_bg, sure_fg)

        _, markers = cv2.connectedComponents(sure_fg)
        markers = markers + 1
        markers[unknown == 255] = 0

        output_image = image

        markers = cv2.watershed(cv2.cvtColor(image, cv2.COLOR_GRAY2RGB), markers)
        binarized_image = fill_contours(markers)
        output_image[markers == -1] = 255

        image_resizing = hyperparameters['strain']['preprocessing_methods']['image_resizing']
        strain_area = np.sum(binarized_image == 2) * ((1/image_resizing) ** 2)

        plt.imshow(binarized_image, cmap='gray')
        plt.show()

        original_dims = [0, 600, 0,   800]
        image_cropping = hyperparameters['strain']['preprocessing_methods']['image_cropping']
        padding = [ (abs(original_dims[0] - image_cropping[0]), abs(original_dims[1] - image_cropping[1])), (abs(original_dims[2] - image_cropping[2]), abs(original_dims[3] - image_cropping[3]))]

        return strain_area, np.pad(cv2.resize(output_image, (0,0), fx = 1/image_resizing, fy = 1/image_resizing), padding, mode='constant', constant_values=0)
    else:

        bin_threshold = hyperparameters['bmode']['segmentation_methods']['bin_threshold']
        _, binarized_image = cv2.threshold(image, bin_threshold, 255, cv2.THRESH_BINARY_INV)

        open_dil_size = hyperparameters['bmode']['segmentation_methods']['open/dil_size']
        open_iters = hyperparameters['bmode']['segmentation_methods']['open_iters']
        kernel = np.ones((open_dil_size, open_dil_size), np.uint8)
        opening = cv2.morphologyEx(binarized_image, cv2.MORPH_OPEN, kernel, iterations = open_iters)

        dil_iters = hyperparameters['bmode']['segmentation_methods']['dil_iters']
        sure_bg = cv2.dilate(opening, kernel, iterations = dil_iters)

        dist_transform = hyperparameters['bmode']['segmentation_methods']['dist_transform']
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, dist_transform)

        fg_thresh = hyperparameters['bmode']['segmentation_methods']['fg_thresh']
        _, sure_fg = cv2.threshold(dist_transform, fg_thresh * dist_transform.max(), 255, 0)

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

        return bmode_area, output_image
