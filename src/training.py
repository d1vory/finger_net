import cv2
import numpy as np
import keras

def prepare(img):

    x = img / 255.
    arr = np.asarray(x)
    arr = x.reshape(x.shape[0], x.shape[1], 1)

    arr = np.expand_dims(arr, axis=0)

    return arr

img  = cv2.imread('../fingerprints/enhanced/cutted2.bmp', cv2.IMREAD_GRAYSCALE)

arr = prepare(img)

model  = keras.models.load_model('models/fingerModel_SW2.h5')\

print(model.predict(arr))