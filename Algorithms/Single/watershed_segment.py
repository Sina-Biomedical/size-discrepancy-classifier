import numpy as np
import cv2
from matplotlib import pyplot as plt

from preprocessing_methods import preprocess

img_filepath = "../../Data/Frames/Malignant/10-58-09/234/strain.jpg"
original_image = cv2.imread(img_filepath, 0)

img,_ = preprocess(img_filepath)
ret, thresh = cv2.threshold(img,84,255,cv2.THRESH_BINARY_INV)

plt.subplot(121), plt.imshow(original_image, cmap='gray'), plt.title('Original Image')
plt.subplot(122), plt.imshow(thresh, cmap='gray'), plt.title('Binarized Image')
plt.show()

kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

plt.subplot(121), plt.imshow(thresh, cmap='gray'), plt.title('Binarized Image')
plt.subplot(122), plt.imshow(opening, cmap='gray'), plt.title('MORPH_OPEN Image')
plt.show()

# sure background area
sure_bg = cv2.dilate(opening,kernel,iterations=3)

# Finding sure foreground area
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

plt.subplot(121), plt.imshow(sure_bg, cmap='gray'), plt.title('Background')
plt.subplot(122), plt.imshow(sure_fg, cmap='gray'), plt.title('Foreground')
plt.show()

# Finding unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)

plt.subplot(121), plt.imshow(original_image, cmap='gray'), plt.title('Background')
plt.subplot(122), plt.imshow(unknown, cmap='gray'), plt.title('Foreground')
plt.show()

# Marker labelling
ret, markers = cv2.connectedComponents(sure_fg)

# Add one to all labels so that sure background is not 0, but 1
markers = markers+1

# Now, mark the region of unknown with zero
markers[unknown == 255] = 0

plt.subplot(121), plt.imshow(original_image, cmap='gray'), plt.title('Background')
plt.subplot(122), plt.imshow(markers, cmap='jet'), plt.title('Foreground')
plt.show()

markers = cv2.watershed(cv2.cvtColor(img, cv2.COLOR_GRAY2RGB), markers)
img[markers == -1] = 255

plt.subplot(121), plt.imshow(original_image, cmap='gray'), plt.title('Original Image')
plt.subplot(122), plt.imshow(img, cmap='gray'), plt.title('Processed Image')
plt.show()
