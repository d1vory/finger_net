import keras
import cv2
import numpy as np
import pandas as pd
import random
from scipy import ndimage, misc
import matplotlib.pyplot as plt
from skimage import filters
from skimage.color import rgb2gray  # only needed for incorrectly saved images
from skimage.measure import regionprops
import time

def prepare(img):

    x = img / 255.
    arr = np.asarray(x)
    arr = x.reshape(x.shape[0], x.shape[1], 1)

    arr = np.expand_dims(arr, axis=0)

    return arr


def getStride(imgShape, resShape, kernelShape):
    if kernelShape[0] != kernelShape[1]:
        raise ValueError

    dH = (imgShape[0] - kernelShape[0] ) / (resShape[1] - 1)
    dW =  (imgShape[1] - kernelShape[1] ) / (resShape[2] - 1)
    return int(dH)

def getRegionCenter(regionIndeces, stride):
    x = stride[0] * (regionIndeces[1]  ) + 15
    y = stride[1] * (regionIndeces[2]  ) + 15
    return x,y



def drawCircles2(img,centers):
    for point in centers:
        cv2.circle(img, tuple(point), 3, 64)
    return img


def drawRects2(img, prediction, mask ):
    stride = 1

    for j in range(prediction.shape[1]):
        for i in range(prediction.shape[2]):
            temp = np.array([0, j, i, 0])
            if (mask == temp).all(1).any():
                cv2.rectangle(img, (i*stride, j*stride), (i*stride + 30, j*stride + 30), 1, 1)

    return img



def predictImage(img, model ,kernelShape, threshold , invert = True, medianFilter = True):
    if invert:
        ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)


    probsMatrix = np.zeros(img.shape, dtype=np.uint8)
    arr = prepare(img)
    prediction = model.predict(arr)
    predictionIndeces  = np.argwhere(prediction > threshold)
    stride = getStride(img.shape, prediction.shape, kernelShape)

    for j in range(prediction.shape[1]):
        for i in range(prediction.shape[2]):
            temp = np.array([0, j, i, 0])
            if (predictionIndeces == temp).all(1).any():
                probsMatrix[j* stride + 15][i * stride + 15] = 255

    if medianFilter:
        probsMatrix = cv2.medianBlur(probsMatrix,3)

    return probsMatrix


def detectAngle(img, centers):
    kek = np.asarray(img)
    t = 3
    for point in centers:
        matr = kek[point[1] - t +1:  point[1] + t,point[0] - t +1: point[0] + t ]
        #matr = kek[10: 15, 10: 15]
        #print("as")

def detectCenters(predictionMask):
    contours , _= cv2.findContours(predictionMask.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)
    print(len(contours))
    centres = []
    for i in range(len(contours)):
        moments = cv2.moments(contours[i])
        if moments["m00"] != 0:
            x = int(moments['m10'] / moments['m00'])
            y = int(moments['m01'] / moments['m00'])
            centres.append((x,y) )

    return np.array(centres)

if __name__ == '__main__':
    img = cv2.imread('../fingerprints/enhanced/0010_01.bmp', cv2.IMREAD_GRAYSCALE)
    ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow("Original", img)
    fingerModel = keras.models.load_model('models/fingerModel_CSW4.h5')

    start_time = time.time()
    pr = predictImage(img,fingerModel,(30,30),0.98, invert=False, medianFilter=True)
    print("--- %s seconds ---" % (time.time() - start_time))
    cv2.imshow("mask", pr)

    centers = detectCenters(pr)
    orig =  cv2.imread('../fingerprints/all/0010_01.bmp', cv2.IMREAD_GRAYSCALE)
    centersOnImage = drawCircles2(orig.copy(), centers)

    #k = detectAngle(img, centers)
    cv2.imshow("centerss" , centersOnImage)

    #np.save('testPoints1b.npy', np.array(centers))

    print("ok")
    cv2.waitKey()