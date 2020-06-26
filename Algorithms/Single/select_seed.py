# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #                                                                                                             #
#                 _                 _                                     _                         #
#    ___    ___  | |   ___    ___  | |_           ___    ___    ___    __| |      _ __    _   _     #
#   / __|  / _ \ | |  / _ \  / __| | __|         / __|  / _ \  / _ \  / _` |     | '_ \  | | | |    #
#   \__ \ |  __/ | | |  __/ | (__  | |_          \__ \ |  __/ |  __/ | (_| |  _  | |_) | | |_| |    #
#   |___/  \___| |_|  \___|  \___|  \__|  _____  |___/  \___|  \___|  \__,_| (_) | .__/   \__, |    #
#                                        |_____|                                 |_|      |___/     #
#                                                                                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Est. June 26, 2020 (6/26/2020)  #
# # # # # # # # # # # # # # # # # #
# SINA BIOMEDICAL RESEARCH GROUP  #
#   +-- S. Kaisar Alam (PI)       #
#   +-- Areeq I. Hasan (Lead)     #
#   +-- Sarina M. Hasan (Assgn.)  #
#   +-- Raiyah Z. Ahmed           #
#   +-- Wasi S. Ahmed             #
# # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# select_seed()                                                                               #
# Computes the ratio between the area of a lesion in a given b-mode and strain image pair.    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# @ params                                                                                    #
#   +-- image_directory: (string) | Path to the directory containing strain.png & b-mode.png  #
# @ output                                                                                    #
#   +-- area_ratio:      (double) | the area ratio between strain and b-mode masks.           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# % Steps:
# 1. Pre-processing (@ preprocess.py)
# 2. Segment via Otsu Thresholding
# 3. Seed Generation
# 4. Ranking
# 5. Seed Point Geneneration
# 6. Refining Seed Point
# 7. Seed Point Display/Return

from preprocessing_methods import preprocess
import cv2

def select_seed(image_filepath):

    image_type = "strain" if image_filepath[-5:] == "n.jpg" else "bmode"
    print(image_filepath[-5:])

    processed_image, _ = preprocess(image_filepath)

    if image_type == "strain":
        _, binarized_image = cv2.threshold(processed_image, 120, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        cv2.imshow('Otsu Threshold', binarized_image)

    else:
        pass

    # return seed_x, seed_y

select_seed("../../Data/Frames/Malignant/10-58-09/234/strain.jpg")
