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

from preprocessing_methods import preprocess
from segmentation_methods import segment

def compare_area(image_directory):
    strain_image = image_directory + "strain.jpg"
    bmode_image = image_directory + "bmode.jpg"

    # Pre-process images @ preprocess.py
    strain_image, strain_region = preprocess(strain_image, 'strain')
    bmode_image, bmode_region = preprocess(bmode_image, 'b-mode')

    # Segment images @ segment.py
    strain_segmented = segment(strain_image, strain_region, 'strain', 60)
    bmode_segmented = segment(bmode_image, bmode_region, 'b-mode', 60)

    # # Compute the area ratio from the images
    # strain_area = sum(strain_segmented)
    # bmode_area = sum(bmode_segmented)
    # area_ratio = strain_area / bmode_area
    #
    # return area_ratio

# 10/58/09 | 234th Frame
compare_area("../../Data/Frames/Malignant/10-58-09/234/")
