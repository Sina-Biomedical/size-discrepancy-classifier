# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #                                                                                                             #
#                  _   _   _              __                                                                #
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
# Splits an *.avi file into B-Mode & Elastogram frames placed in the Data > Frames directory. #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# @ params                                                                                    #
#   +-- avi_file:       (string) | Path to the *.avi file to split into frames.               #
#   +-- classification: (string) | Whether the lesion framed is B9/CA.                        #
#   +-- layout:         (int)    | Whether the *.avi has the Start Bar at the bottom.         #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import cv2
print(cv2.__version__)

def split_frames(avi_directory):

    # Get  from avi_directory
    classification = 'Malignant' if avi_directory[15] == 'M' else 'Benign'
    id = avi_directory[-8:]
    directory_header = "../../Data/Frames/" + classification + "/" + id + "/"
    print(directory_header)

    # Split Strain --> Frames

    elastogram_sequence = cv2.VideoCapture(avi_directory + "/Strain.mp4")
    success, frame = elastogram_sequence.read()
    count = 0

    while success:

        # cv2.imshow('img', frame)
        # cv2.waitKey(0)

        os.makedirs(directory_header + "/%d/" % count)
        if not cv2.imwrite(directory_header + "/%d/strain.jpg" % count, frame):
            raise Exception("Could not write image")
        success, frame = elastogram_sequence.read()
        print ('Read a new frame: ', success)
        count += 1

    # Split Bmode --> Frames

    bmode_sequence = cv2.VideoCapture(avi_directory + "/Bmode.mp4")
    success, frame = bmode_sequence.read()
    count = 0

    while success:

        # cv2.imshow('img', frame)
        # cv2.waitKey(0)

        if not cv2.imwrite(directory_header + "/%d/bmode.jpg" % count, frame):
            raise Exception("Could not write image")
        success, frame = bmode_sequence.read()
        print ('Read a new frame: ', success)
        count += 1

#benign
split_frames("../../Data/AVI/Benign/07-48-22")
split_frames("../../Data/AVI/Benign/07-53-53")
split_frames("../../Data/AVI/Benign/09-11-35")
split_frames("../../Data/AVI/Benign/09-12-46")
split_frames("../../Data/AVI/Benign/09-13-35")
split_frames("../../Data/AVI/Benign/10-44-27")
split_frames("../../Data/AVI/Benign/10-51-35")
split_frames("../../Data/AVI/Benign/13-53-47")
split_frames("../../Data/AVI/Benign/13-56-04")
split_frames("../../Data/AVI/Benign/14-13-31")
split_frames("../../Data/AVI/Benign/14-37-20")

#malignant
split_frames("../../Data/AVI/Malignant/07-50-58")
split_frames("../../Data/AVI/Malignant/08-28-57")
split_frames("../../Data/AVI/Malignant/09-10-14")
split_frames("../../Data/AVI/Malignant/09-16-04")
split_frames("../../Data/AVI/Malignant/09-35-49")
split_frames("../../Data/AVI/Malignant/10-22-11")
# split_frames("../../Data/AVI/Malignant/10-58-09")
split_frames("../../Data/AVI/Malignant/13-43-30")
split_frames("../../Data/AVI/Malignant/13-54-36")
split_frames("../../Data/AVI/Malignant/14-07-13")
split_frames("../../Data/AVI/Malignant/14-21-51")
