import os
import cv2
import h5py
import imageio
import numpy as np
from tqdm import tqdm
from PIL import Image, ImageEnhance
from matplotlib import pyplot as plt

source_directory = '../../Data/Frames/'
destination_directory = '../../Data/CompareNET/Raw/'

def get_contours(image):
    _, binarized_image = cv2.threshold(image, 80, 255, 0)
    contours, _ = cv2.findContours(binarized_image, 1, 2)
    contours = [contour for contour in contours if valid_contour(contour)]
    return contours

def valid_contour(contour):
    x, y, w, h = cv2.boundingRect(contour)
    if w < 50 or h < 50: return False
    area = cv2.contourArea(contour)
    return area > 200

def find_boundaries(img, contours):
    y_1, x_1 = img.shape[:2]
    x_2 = 0
    y_2 = 0

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if x < x_1: x_1 = x
        if y < y_1: y_1 = y
        if x + w > x_2: x_2 = x + w
        if y + h > y_2: y_2 = y + h

    return (x_1, y_1, x_2, y_2)

def crop_image(image, boundaries):
    x_1, y_1, x_2, y_2 = boundaries
    return y_1, y_2, x_1, x_2

def parse_image(image):
    contours = get_contours(image)
    boundaries = find_boundaries(image, contours)
    return crop_image(image, boundaries)

lesion_data = h5py.File(os.path.join(destination_directory, 'lesion_data.h5'), 'w')
lesion_data.create_dataset('images', (39826, 264, 264, 2), dtype='f')
lesion_data.create_dataset('labels', (39826, 1), dtype='i')
lesion_data.close()

lesion_data = h5py.File(os.path.join(destination_directory, 'lesion_data.h5'), 'r+')     # open the file
lesion_images = lesion_data['images']
lesion_labels = lesion_data['labels']

root_directory = '../../Data/AVI/'
lesion_files = []
for path, subdirs, files in os.walk(root_directory):
    for file_name in files:
        if len(file_name) == 12:
            lesion_files.append(os.path.join(path, file_name))

lesion_count = 0
for file_path in tqdm(lesion_files):
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
                y1, y2, x1, x2 = parse_image(strain)

            strain_cropped = cv2.resize(strain[y1:y1 + image_size, :], dsize=(264, 264))
            bmode_cropped = cv2.resize(bmode[y1:y1 + image_size, :], dsize=(264, 264))

            lesion_images[lesion_count] = np.stack((strain_cropped, bmode_cropped), axis=2)
            lesion_labels[lesion_count] = 1 if file_path[18] == 'M' else 0

            lesion_count += 1

        success, frame = avi_sequence.read()
        count += 1

lesion_data.close()

# # TRANSFORM IMAGES
# augmented_lesions = []
# for i, lesion in enumerate(tqdm(lesions)):
#     transformed_lesion_1 = {
#         'strain_image': np.fliplr(lesion['strain_image']),
#         'bmode_image': np.fliplr(lesion['bmode_image']),
#         'classification': lesion['classification']
#     }
#
#     transformed_lesion_2 = {
#         'strain_image': np.flipud(lesion['strain_image']),
#         'bmode_image': np.flipud(lesion['bmode_image']),
#         'classification': lesion['classification']
#     }
#
#     transformed_lesion_3 = {
#         'strain_image': cv2.rotate(lesion['strain_image'], cv2.ROTATE_90_CLOCKWISE),
#         'bmode_image': cv2.rotate(lesion['bmode_image'], cv2.ROTATE_90_CLOCKWISE),
#         'classification': lesion['classification']
#     }
#
#     transformed_lesion_4 = {
#         'strain_image': cv2.rotate(lesion['strain_image'], cv2.ROTATE_90_COUNTERCLOCKWISE),
#         'bmode_image': cv2.rotate(lesion['bmode_image'], cv2.ROTATE_90_COUNTERCLOCKWISE),
#         'classification': lesion['classification']
#     }
#
#     transformed_lesion_5 = {
#         'strain_image': cv2.rotate(lesion['strain_image'], cv2.ROTATE_180),
#         'bmode_image': cv2.rotate(lesion['bmode_image'], cv2.ROTATE_180),
#         'classification': lesion['classification']
#     }
#
#     augmented_lesions.append(lesion)
#     augmented_lesions.append(transformed_lesion_1)
#     augmented_lesions.append(transformed_lesion_2)
#     augmented_lesions.append(transformed_lesion_3)
#     augmented_lesions.append(transformed_lesion_4)
#     augmented_lesions.append(transformed_lesion_5)
#
#
# training_set_size = int(0.95 * len(augmented_lesions))
# test_set_size = len(augmented_lesions) - training_set_size
#
# print("Dataset Size: " + str(len(augmented_lesions)))
# print("Training Set Size: " + str(training_set_size))
# print("Test Set Size: " + str(test_set_size))
#
# training_images = np.zeros((training_set_size, 264, 264, 2))
# training_labels = np.zeros((training_set_size, 1))
# test_images     = np.zeros((training_set_size, 264, 264, 2))
# test_labels     = np.zeros((training_set_size, 1))
#
# for i, lesion in enumerate(tqdm(augmented_lesions)):
#     if i <= training_set_size:
#         training_images[i, [lesion['strain_image'], lesion['bmode_image']]]
#         training_labels[i, lesion['classification']]
#     else:
#         test_images[i, [lesion['strain_image'], lesion['bmode_image']]]
#         test_labels[i, lesion['classification']]
#
# training_data = h5py.File(os.path.join(destination_directory, 'training_data.h5'), 'w')
# test_data     = h5py.File(os.path.join(destination_directory, 'test_data.h5'), 'w')
#
# training_data.create_dataset('training_images', data=training_images)
# training_data.create_dataset('training_labels', data=training_labels)
# training_data.close()
#
# test_data.create_dataset('test_images', data=test_images)
# test_data.create_dataset('test_labels', data=test_labels)
# test_data.close()
