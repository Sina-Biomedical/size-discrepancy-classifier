import os
import cv2
import h5py
import imageio
import numpy as np
from tqdm import tqdm
from PIL import Image, ImageEnhance
from matplotlib import pyplot as plt
from preprocessing_methods import preprocess

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

training_data = h5py.File(os.path.join(destination_directory, 'training_data.h5'), 'w')
training_data.create_dataset('images', (39000, 128, 128, 2), dtype='f')
training_data.create_dataset('labels', (39000, 1), dtype='i')
training_data.close()

test_data = h5py.File(os.path.join(destination_directory, 'test_data.h5'), 'w')
test_data.create_dataset('images', (826, 128, 128, 2), dtype='f')
test_data.create_dataset('labels', (826, 1), dtype='i')
test_data.close()

training_data = h5py.File(os.path.join(destination_directory, 'training_data.h5'), 'r+')
training_images = training_data['images']
training_labels = training_data['labels']

test_data = h5py.File(os.path.join(destination_directory, 'test_data.h5'), 'r+')
test_images = test_data['images']
test_labels = test_data['labels']

root_directory = '../../Data/AVI/'
lesion_files = []
for path, subdirs, files in os.walk(root_directory):
    for file_name in files:
        if len(file_name) == 12:
            lesion_files.append(os.path.join(path, file_name))

hyperparameters = {
    'strain': {
        'preprocessing_methods': {
            'closing_size'  :  5,
            'closing_iters' :  1,
            'med_blurring'  :  9
        },
    },
    'bmode': {
        'preprocessing_methods': {
            'closing_size'  : 3,
            'closing_iters' : 1,
            'bilat_filter'  : 1,
            'med_blurring'  : 5
        },
    }
}

malignant_count = 0
benign_count = 0
for i, file_path in enumerate(tqdm(lesion_files)):
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


            strain_cropped = cv2.resize(strain[y1:y1 + image_size, :], dsize=(128, 128))/255.
            bmode_cropped = cv2.resize(bmode[y1:y1 + image_size, :], dsize=(128, 128))/255.

            # strain_cropped = preprocess(cv2.resize(strain[y1:y1 + image_size, :], dsize=(64, 64)), 'strain', hyperparameters)/255.
            # bmode_cropped = preprocess(cv2.resize(bmode[y1:y1 + image_size, :], dsize=(64, 64)), 'bmode', hyperparameters)/255.
            #
            # plt.subplot(221), plt.imshow(cv2.resize(strain[y1:y1 + image_size, :], dsize=(64, 64)), cmap='gray')
            # plt.subplot(222), plt.imshow(cv2.resize(bmode[y1:y1 + image_size, :], dsize=(64, 64)), cmap='gray')
            # plt.subplot(223), plt.imshow(strain_cropped, cmap='gray')
            # plt.subplot(224), plt.imshow(bmode_cropped, cmap='gray')
            # plt.show()

            classification = 1 if file_path[15] == 'M' else 0

            # 7795 Malignant & 32,031 Benign --> 413 Malignant + 413 Benign Test // 7,382 Malignant + 31,618 Benign Train
            if classification:
                if malignant_count <= 412:
                    # Test // 0 --> 412
                    # print("Test Set w/ Index: " + str(malignant_count))
                    test_images[malignant_count] = np.stack((strain_cropped, bmode_cropped), axis=2)
                    test_labels[malignant_count] = classification
                else:
                    # Training // 0 --> 7381
                    # print("Training Set w/ Index: " + str(malignant_count-413))
                    training_images[malignant_count-413] = np.stack((strain_cropped, bmode_cropped), axis=2)
                    training_labels[malignant_count-413] = classification

                malignant_count += 1
            else:
                if benign_count <= 412:
                    # print("Test Set w/ Index: " + str(413+benign_count))
                    test_images[413+benign_count] = np.stack((strain_cropped, bmode_cropped), axis=2)
                    test_labels[413+benign_count] = classification
                else:
                    # print("Training Set w/ Index: " + str(malignant_count-413+benign_count))
                    training_images[malignant_count-413+benign_count-413] = np.stack((strain_cropped, bmode_cropped), axis=2)
                    training_labels[malignant_count-413+benign_count-413] = classification

                benign_count += 1

        success, frame = avi_sequence.read()
        count += 1

training_data.close()
test_data.close()
