from PIL import Image, ImageEnhance
import os
import imageio
from matplotlib import pyplot as plt
from tqdm import tqdm

source_directory = '../../../Data/Frames/'
destination_directory = '../../../Data/CompareNET/'

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

def resize(image, target = (300, 300)):
    resized_image = image.resize(target)
    return resized_image

def save_lesion(lesion):
    image = Image.open(lesion['source_path'])
    resized_image = resize(image)

    destination_path = os.path.join(destination_directory, lesion['classification'] + '/', lesion['destination_name'] + ".jpg")
    resized_image.save(destination_path, 'JPEG')

    transformations = [flip_horizontal, flip_vertical, rotate_90, rotate_180, rotate_270, sharpen, blur]
    for transformation in transformations:
        transformed_image, transformation_suffix = transformation(resized_image)
        destination_path = os.path.join(destination_directory, lesion['classification'] + '/', lesion['destination_name'] + " " + transformation_suffix + ".jpg")
        transformed_image.save(destination_path, 'JPEG')

lesions = []
for path, subdirs, files in os.walk(source_directory):
    for file_name in files:
        lesion = {}
        lesion['source_path'] = os.path.join(path, file_name)
        lesion['classification'] = 'Malignant' if path[21] == 'M' else 'Benign'
        lesion['frame_number'] = path[path.rfind("/")+1:]
        lesion['image_type'] = 'S' if path[-5] == 'n' else 'B'
        lesion['destination_name'] = path[path.rfind("/", 0, path.rfind("/"))+1:path.rfind("/")] + " (" + lesion['image_type'] + '-' + str(lesion['frame_number']) + ")"

        lesions.append(lesion)

for lesion in tqdm(lesions):
    save_lesion(lesion)
