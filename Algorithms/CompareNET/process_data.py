from PIL import Image, ImageEnhance
import os
import imageio
from matplotlib import pyplot as plt
from tqdm import tqdm
import cv2
import h5py
import numpy as np

source_directory = '../../../Data/Frames/'
destination_directory = '../../../Data/CompareNET/Raw/'

def to_numpy_array(address):
    image = imageio.imread(address)
    return image

def flip_horizontal(image):
    transformed_image = image.transpose(Image.FLIP_LEFT_RIGHT)
    return transformed_image, "FLR"

def flip_vertical(image):
    transformed_image = image.transpose(Image.FLIP_TOP_BOTTOM)
    return transformed_image, 'FTB'

def rotate_90(image):
    rotated_image = image.transpose(Image.ROTATE_90)
    return rotated_image, "R90"

def rotate_180(image):
    rotated_image = image.transpose(Image.ROTATE_180)
    return rotated_image, "R180"

def rotate_270(image):
    rotated_image = image.transpose(Image.ROTATE_270)
    return rotated_image, "R270"

def sharpen(image):
    enhancer = ImageEnhance.Sharpness(image)
    sharpened_image = enhancer.enhance(2.0)
    return sharpened_image, "S2"

def blur(image):
    enhancer = ImageEnhance.Sharpness(image)
    blurred_image = enhancer.enhance(0.0)
    return blurred_image, "B0"

def save_lesion(lesion, save_as = 'train'):
    destination_path = os.path.join(destination_directory, lesion['classification'])

    # destination_path = os.path.join(destination_directory, lesion['classification'] + '/', lesion['destination_name'] + ".jpg")
    # Image.fromarray(lesion['image']).save(destination_path, 'JPEG')
    #
    # transformations = [flip_horizontal, flip_vertical, rotate_90, rotate_180, rotate_270, sharpen, blur]
    # for transformation in transformations:
    #     transformed_image, transformation_suffix = transformation(Image.fromarray(lesion['image']))
    #     destination_path = os.path.join(destination_directory, lesion['classification'] + '/', lesion['destination_name'] + " " + transformation_suffix + ".jpg")
    #     transformed_image.save(destination_path, 'JPEG')

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

lesions = []
root_directory = '../../../Data/AVI/'

for path, subdirs, files in os.walk(root_directory):
    for file_name in files:
        if len(file_name) == 12:
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

                    lesion = {}
                    lesion['strain_image'] = strain_cropped
                    lesion['bmode_image'] = bmode_cropped
                    lesion['classification'] = 1 if file_path[18] == 'M' else 0
                    lesions.append(lesion)

                success, frame = avi_sequence.read()
                count += 1

# TRANSFORM IMAGES
for lesion in tqdm(lesions):

    transformed_lesion_1 = {
        'strain_image': np.fliplr(lesion['strain_image']),
        'bmode_image': np.fliplr(lesion['bmode_image']),
        'classification': lesion['classification']
    }

    transformed_lesion_2 = {
        'strain_image': np.flipud(lesion['strain_image']),
        'bmode_image': np.flipud(lesion['bmode_image']),
        'classification': lesion['classification']
    }

    transformed_lesion_3 = {
        'strain_image': cv2.rotate(lesion['strain_image'], cv2.ROTATE_90_CLOCKWISE),
        'bmode_image': cv2.rotate(lesion['bmode_image'], cv2.ROTATE_90_CLOCKWISE),
        'classification': lesion['classification']
    }

    transformed_lesion_4 = {
        'strain_image': cv2.rotate(lesion['strain_image'], cv2.ROTATE_90_COUNTERCLOCKWISE),
        'bmode_image': cv2.rotate(lesion['bmode_image'], cv2.ROTATE_90_COUNTERCLOCKWISE),
        'classification': lesion['classification']
    }

    transformed_lesion_5 = {
        'strain_image': cv2.rotate(lesion['strain_image'], cv2.ROTATE_180),
        'bmode_image': cv2.rotate(lesion['bmode_image'], cv2.ROTATE_180),
        'classification': lesion['classification']
    }

    lesions.append(transformed_lesion_1)
    lesions.append(transformed_lesion_2)
    lesions.append(transformed_lesion_3)
    lesions.append(transformed_lesion_4)
    lesions.append(transformed_lesion_5)

training_set_size = int(0.95 * len(lesions))
test_set_size = len(lesions) - training_set_size

print("Dataset Size: " + str(len(lesions)))
print("Training Set Size: " + str(training_set_size))
print("Test Set Size: " + str(test_set_size))

training_images = numpy.zeros((training_set_size, 264, 264, 2))
training_labels = numpy.zeros((training_set_size, 1))
test_images     = numpy.zeros((training_set_size, 264, 264, 2))
test_labels     = numpy.zeros((training_set_size, 1))

for i, lesion in enumerate(tqdm(lesions)):
    if i <= training_set_size:
        training_images[i, [lesion['strain_image'], lesion['bmode_image']]]
        training_labels[i, lesion['classification']]
    else:
        test_images[i, [lesion['strain_image'], lesion['bmode_image']]]
        test_labels[i, lesion['classification']]

training_data = h5py.File(os.path.join(destination_directory, 'training_data.h5'), 'w')
test_data     = h5py.File(os.path.join(destination_directory, 'test_data.h5'), 'w')

training_data.create_dataset('training_images', data=training_images)
training_data.create_dataset('training_labels', data=training_labels)
training_data.close()

test_data.create_dataset('test_images', data=test_images)
test_data.create_dataset('test_labels', data=test_labels)
test_data.close()
