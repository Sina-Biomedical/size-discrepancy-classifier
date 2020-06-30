import numpy as np
# OpenCV
import cv2
# To Read Folder of images
from os import listdir
# To Join the paths
from os.path import isfile, join
# To store DiceCoefficient of all images in Excel
import pandas as pd

def on_mouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print('Seed: ' + str(x) + ', ' + str(y))
    clicks.append((y, x))

# Region Growing Segmentation
def RegionGrowing(portion, epsilon):
     output = np.zeros(np.shape(orginalImg), dtype=np.uint8)
     output[x][y] = 255
     while len(portion) > 0:
          xcd = portion[0][0]
          ycd = portion[0][1]
          for i in range(-1, 2):
               for j in range(-1, 2):
                    absDiff = abs(int(cen_pix) - int(orginalImg[xcd + i][ycd + j]))
                    if (i != 0 or j != 0) and output[xcd + i][ycd + j] != 255 and absDiff < epsilon:
                         output[xcd + i][ycd + j] = 255
                         portion.append([xcd + i, ycd + j])
          portion.pop(0)
     return output

# Function to remove the smallest objects using cca and only show the biggest one
def RemoveUnwantedRegions(output):
    new_img = np.zeros_like(output)
    for val in np.unique(output)[1:]:
        mask = np.uint8(output == val)  # step 3
        labels, stats = cv2.connectedComponentsWithStats(mask, 5)[1:3]
        largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
        new_img[labels == largest_label] = val
    return new_img

image = "/Users/areeq_hasan/Documents/GitHub/size-discrepancy-classifier/Data/Frames/Malignant/10-58-09/234/strain.jpg"

clicks = []
orginalImg = cv2.imread(image, 0)
# cv2.imshow('Original Image', orginalImg)
kernel = np.ones((9, 9), np.uint8)
orginalImg = cv2.morphologyEx(orginalImg, cv2.MORPH_CLOSE, kernel, iterations=1)
orginalImg = cv2.medianBlur(orginalImg, 19)
cv2.namedWindow('Input')
cv2.setMouseCallback('Input', on_mouse, 0, )
cv2.imshow('Input', orginalImg)
cv2.waitKey()
seed = clicks[-1]
x = seed[0]
y = seed[1]
rows = orginalImg.shape[0]
cols = orginalImg.shape[1]
# Find the center
cen_pix = orginalImg[x][y]
# New matrix that will hold segmented image
epsilon = 60
# Matrix to hold all region pixels
portion = [[x, y]]
RG = RegionGrowing(portion, epsilon)
kernel = np.ones((19, 19), np.uint8)
RG = cv2.morphologyEx(RG, cv2.MORPH_CLOSE, kernel, iterations=2)
# Removing small regions that are not a part of lesion like corners
output = RemoveUnwantedRegions(RG)
cv2.imshow('Output', output)
cv2.waitKey()
