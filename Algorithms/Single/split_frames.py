# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #                                                                                                             #
#                 _   _   _              __                                                                 #
#    ___   _ __   | | (_) | |_           / _|  _ __    __ _   _ __ ___     ___   ___       _ __    _   _    #
#   / __| | '_ \  | | | | | __|         | |_  | '__|  / _` | | '_ ` _ \   / _ \ / __|     | '_ \  | | | |   #
#   \__ \ | |_) | | | | | | |_          |  _| | |    | (_| | | | | | | | |  __/ \__ \  _  | |_) | | |_| |   #
#   |___/ | .__/  |_| |_|  \__|  _____  |_|   |_|     \__,_| |_| |_| |_|  \___| |___/ (_) | .__/   \__, |   #
#         |_|                   |_____|                                                   |_|      |___/    #
#                                                                                                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Est. June 20, 2020 (6/20/2020)  #
# # # # # # # # # # # # # # # # # #
# SINA BIOMEDICAL RESEARCH GROUP  #
#   +-- S. Kaisar Alam (PI)       #
#   +-- Areeq I. Hasan (Lead)     #
#   +-- Sarina M. Hasan (Assign.) #
#   +-- Raiyah Z. Ahmed           #
#   +-- Wasi S. Ahmed             #
# # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# split_frames()                                                                              #
# Splits an *.avi file into B-Mode & Elastogram images placed in the Data > Frames directory. #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# @ params                                                                                    #
#   +-- avi_file:       (string) | Path to the *.avi file to split into frames.               #
#   +-- classification: (string) | Whether the lesion imaged is B9/CA.                        #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def split_frames(avi_file, classification):
    # Getting B-Modes & Elastograms
    # Origin: Bottom-Right Corner
    # AVI Dimensions --> 800 x 600
    # Strain Image
    #   +-- Bottom-Left Corner @ (70, 230)
    #   +-- Dimensions: 265 x 205
    # B-Mode Image
    #   +-- Bottom-Left Corner @ (390, 155)
    #   +-- Dimensions: 265 x 280

    # For a given *.avi,
    # +-- Iterate through each frame
    # +-- Get the B-Mode & Strain from each frame using the above guidelines
    # +-- Save the images as strain.png/bmode.png in Data > Frames > Benign/Malignant > AVI Name > Frame # > strain.png/bmode.png
    #   +-- Use classification to determine whether to put it in Benign or Malignant
    #   +-- The AVI Name comes from everything before the .avi in avi_file
    #   +-- You can get Frame # from the iterator.

split_frames("../../Data/AVI/Malignant/10-58-09.avi", "Malignant")
