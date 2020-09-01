import keras
import tensorflow
from keras import layers
from keras.layers import Input, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D
from keras.layers import AveragePooling2D, MaxPooling2D, Dropout, GlobalMaxPooling2D, GlobalAveragePooling2D
from keras.models import Model

import numpy as np



def fingerModel(input_shape):
    X_input = keras.Input(input_shape)

    print("SHAPE =", X_input.shape)
    X = Conv2D(64, (5, 5), padding='same', strides=(1, 1))(X_input)
    X = BatchNormalization(axis=3, name='bn1')(X)
    X = Activation('relu')(X)
    X = MaxPooling2D((2, 2), strides=(2, 2), padding='same')(X)
    print("SHAPE2 =", X.shape)

    X = Conv2D(128, (5, 5), padding='same')(X)
    X = BatchNormalization(axis=3, name='bn2')(X)
    X = Activation('relu')(X)
    X = MaxPooling2D((2, 2), strides=(2, 2),padding='same')(X)
    print("SHAPE3 =", X.shape)

    X = Conv2D(32, (3, 3), padding='same')(X)
    X = BatchNormalization(axis=3, name='bn3')(X)
    X = Activation('relu')(X)

    X = Conv2D(32, (3, 3), padding='same' )(X)
    X = BatchNormalization(axis=3, name='bn4')(X)
    X = Activation('relu')(X)

    X = Conv2D(32, (3, 3))(X)
    X = BatchNormalization(axis=3, name='bn5')(X)
    X = Activation('relu')(X)

    print("SHAPE6 =", X.shape)
    X = Flatten()(X)
    X = Dense(1024, activation='relu')(X)
    X = Dense(1024, activation='relu')(X)
    X = Dense(1, activation='sigmoid')(X)

    model = Model(inputs=X_input, outputs=X, name='FingerNet')

    return model
kek = fingerModel((40,40,1))