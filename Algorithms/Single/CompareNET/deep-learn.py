import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (10.0, 8.0)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPooling2D
from keras import backend as K

from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot
from keras.preprocessing.image import ImageDataGenerator

img_rows, img_cols = 225, 300 # 224, 224 resized down from 360, 528
color_channels = 1

if K.image_data_format() == 'channels_first':
    input_shape = (color_channels, img_rows, img_cols)
else:
    input_shape = (img_rows, img_cols, color_channels)

print('Input Shape: ', input_shape)

convolution_parameters = {
    'filters'      : 32,
    'pool_window'  : 2,
    'kernel_size'  : 3
}

def buildModelStructure():
    model = Sequential()

    model.add(Conv2D(filters, (conv_kernel, conv_kernel), padding='valid', input_shape = input_shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size = (pooling_area, pooling_area)))

    model.add(Conv2D(filters, (conv_kernel, conv_kernel)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(pooling_area, pooling_area)))

    model.add(Conv2D(64, (conv_kernel, conv_kernel)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(pooling_area, pooling_area)))

    model.add(Flatten())
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    return model

def visualize(model):
    model.summary()
    SVG(model_to_dot(model).create(prog='dot', format='svg'))
