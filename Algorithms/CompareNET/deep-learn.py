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

input_shape = (264, 264, 2)

convolution_parameters = {
    'filters'      : 32,
    'pool_window'  : 2,
    'kernel_size'  : 3
}

def build_model():
    model = Sequential()

    model.add(Conv2D(convolution_parameters['filters'], (convolution_parameters['kernel_size'], convolution_parameters['kernel_size']), padding = 'valid', input_shape = input_shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(convolution_parameters['pool_window'], convolution_parameters['pool_window'])))

    model.add(Conv2D(convolution_parameters['filters'], (convolution_parameters['kernel_size'], convolution_parameters['kernel_size'])))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(convolution_parameters['pool_window'], convolution_parameters['pool_window'])))

    model.add(Conv2D(64, (convolution_parameters['kernel_size'], convolution_parameters['kernel_size'])))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(convolution_parameters['pool_window'], convolution_parameters['pool_window'])))

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
