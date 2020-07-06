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
import os
from glob import glob

def get_contours(imgray):
    # First make the image 1-bit and get contours
    ret, thresh = cv2.threshold(imgray, 80, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, 1, 2)

    # filter contours that are too large or small
    size = get_size(imgray)
    contours = [cc for cc in contours if contourOK(cc, size)]
    return contours

def get_size(img):
    ih, iw = img.shape[:2]
    return iw * ih

def contourOK(cc, size):
    x, y, w, h = cv2.boundingRect(cc)
    if w < 50 or h < 50: return False # too narrow or wide is bad
    area = cv2.contourArea(cc)
    return area > 200

def find_boundaries(img, contours):
    # margin is the minimum distance from the edges of the image, as a fraction
    ih, iw = img.shape[:2]
    minx = iw
    miny = ih
    maxx = 0
    maxy = 0

    for cc in contours:
        x, y, w, h = cv2.boundingRect(cc)
        if x < minx: minx = x
        if y < miny: miny = y
        if x + w > maxx: maxx = x + w
        if y + h > maxy: maxy = y + h

    return (minx, miny, maxx, maxy)

def crop(img, boundaries):
    minx, miny, maxx, maxy = boundaries
    return miny, maxy, minx, maxx

def process_image(img):
    contours = get_contours(img)
    #cv2.drawContours(img, contours, -1, (0,255,0)) # draws contours, good for debugging
    bounds = find_boundaries(img, contours)
    return crop(img, bounds)

def split_frames_2():
    root_directory = '../../Data/AVI/'
    for path, subdirs, files in os.walk(root_directory):
        for file_name in files:
            if len(file_name) == 12:
                # For every AVI file
                file_path = os.path.join(path, file_name)
                print(file_path)
                avi_sequence = cv2.VideoCapture(file_path)
                success, frame = avi_sequence.read()

                count = 0
                y1 = y2 = x1 = x2 = 0
                image_size = 264

                while success:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    if cv2.countNonZero(frame) > 150000 and count > 4:

                        if count == 5:
                            image_size = 264 if len(frame) == 600 else 308

                        if len(frame) == 600:
                            strain = frame[100:600, 70:70+image_size]
                            bmode = frame[100:600, 390:390+image_size]
                        else:
                            strain = frame[100:600, 160:160+image_size]
                            bmode = frame[100:600, 480:480+image_size]

                        if count == 5:
                            y1, y2, x1, x2 = process_image(strain)

                        strain_cropped = cv2.resize(strain[y1:y1 + image_size, :], dsize=(264, 264))
                        bmode_cropped = cv2.resize(bmode[y1:y1 + image_size, :], dsize=(264, 264))

                        cv2.imshow('Strain', strain_cropped)
                        cv2.imshow('B-Mode', bmode_cropped)
                        cv2.waitKey()

                    success, frame = avi_sequence.read()
                    count += 1

split_frames_2()

# def split_frames(avi_directory):

    # Get from avi_directory
    # classification = 'Malignant' if avi_directory[15] == 'M' else 'Benign'
    # id = avi_directory[-8:]
    # directory_header = "../../Data/Frames/" + classification + "/" + id # "../../Data/AVI/Benign/07-48-22" --> "../../Data/Frames/Benign/07-48-22"
    # print(directory_header)
    #
    # # Split Strain --> Frames
    #
    # elastogram_sequence = cv2.VideoCapture(avi_directory + "/Strain.AVI")
    # success, frame = elastogram_sequence.read()
    # count = 0
    #
    # while success:
    #
    #     os.makedirs(directory_header + "/%d/" % count) # "../../Data/Frames/Benign/07-48-22/0/"
    #     if not cv2.imwrite(directory_header + "/%d/strain.jpg" % count, frame): # "../../Data/Frames/Benign/07-48-22/0/strain.jpg"
    #         raise Exception("Could not write image")
    #     success, frame = elastogram_sequence.read()
    #     print ('Read a new frame: ', success)
    #     count += 1
    #
    # bmode_sequence = cv2.VideoCapture(avi_directory + "/Bmode.AVI")
    # success, frame = bmode_sequence.read()
    # count = 0
    #
    # while success:
    #     if not cv2.imwrite(directory_header + "/%d/bmode.jpg" % count, frame):
    #         raise Exception("Could not write image")
    #     success, frame = bmode_sequence.read()
    #     print ('Read a new frame: ', success)
    #     count += 1

# # Benign
# split_frames("../../Data/AVI/Benign/07-48-22")
# split_frames("../../Data/AVI/Benign/07-53-53")
# split_frames("../../Data/AVI/Benign/09-11-35")
# split_frames("../../Data/AVI/Benign/09-12-46")
# split_frames("../../Data/AVI/Benign/09-13-35")
# split_frames("../../Data/AVI/Benign/10-44-27")
# split_frames("../../Data/AVI/Benign/10-51-35")
# split_frames("../../Data/AVI/Benign/13-53-47")
# split_frames("../../Data/AVI/Benign/13-56-04")
# split_frames("../../Data/AVI/Benign/14-13-31")
# split_frames("../../Data/AVI/Benign/14-37-20")
#
# #malignant
# split_frames("../../Data/AVI/Malignant/07-50-58")
# split_frames("../../Data/AVI/Malignant/08-28-57")
# split_frames("../../Data/AVI/Malignant/09-10-14")
# split_frames("../../Data/AVI/Malignant/09-16-04")
# split_frames("../../Data/AVI/Malignant/09-35-49")
# split_frames("../../Data/AVI/Malignant/10-22-11")
# split_frames("../../Data/AVI/Malignant/10-58-09")
# split_frames("../../Data/AVI/Malignant/13-43-30")
# split_frames("../../Data/AVI/Malignant/13-54-36")
# split_frames("../../Data/AVI/Malignant/14-07-13")
# split_frames("../../Data/AVI/Malignant/14-21-51")
