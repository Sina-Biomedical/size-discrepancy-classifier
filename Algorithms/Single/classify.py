# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#         _                       _    __                               #
#   ___  | |   __ _   ___   ___  (_)  / _|  _   _       _ __    _   _   #
#  / __| | |  / _` | / __| / __| | | | |_  | | | |     | '_ \  | | | |  #
# | (__  | | | (_| | \__ \ \__ \ | | |  _| | |_| |  _  | |_) | | |_| |  #
#  \___| |_|  \__,_| |___/ |___/ |_| |_|    \__, | (_) | .__/   \__, |  #
#                                           |___/      |_|      |___/   #
#                                                                       #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
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
# classify_lesion()                                                                           #
# Determines whether the depicted lesion is benign or malignant using size discrepancy.       #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# @ params                                                                                    #
#   +-- image_directory: (string) | Path to the directory containing strain.png & b-mode.png  #
# @ output                                                                                    #
#   +-- is_malignant:    (bool)   | Whether the lesion is malignant or benign.                #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def classify_lesion(image_directory):

    # Define threshold, to be determined using an SVM trained on the area ratios of the entire dataset.
    threshold = 2.5

    # Compute the ratio between the area of a lesion in the b-mode and strain image pair @ compare_area.py
    area_ratio = compare_area(image_directory)

    # Determine if the lesion is malignant or benign using the ML-determined threshold
    is_malignant = area_ratio > threshold

    return is_malignant
