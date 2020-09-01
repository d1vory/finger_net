import numpy as np
import math
import cv2
import keras
from matplotlib import pyplot as plt
from transform import ransac, applyTransformation , estimateTransformation
from ConvSlidingWindow import predictImage, detectCenters
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../enhanecement/')

from main_enhancement import enhanceImage

import time

def compareFingerprints(dbPoints, takenImage, model = None):
    #Compares if two fingerprints are the same
    #anchorImage, takenImage   - matrixes of images
    #dbPoints - minuaties points
    # taken Image
    if model == None:
        model = keras.models.load_model('models/fingerModel_CSW4.h5')
    start_time = time.time()
    img  = prepareImage(takenImage)

    prediction =  predictImage(img,model,kernelShape = (30,30),threshold = 0.98, invert=False, medianFilter=True)
    print("prediction --- %s seconds ---" % (time.time() - start_time))
    takenImageCenters = detectCenters(prediction)
    plt.scatter(takenImageCenters[:, 0], takenImageCenters[:, 1], )

    print('takenCetners = ', takenImageCenters.shape)

    start_time = time.time()
    transformation, _ = ransac(dbPoints, takenImageCenters, n = 25, distanceThreshold = 7)
    transformedCenters = applyTransformation(takenImageCenters, transformation)
    print("ransac --- %s seconds ---" % (time.time() - start_time))
    plt.scatter(transformedCenters[:, 0], transformedCenters[:, 1])

    transformation, _ = ransac(transformedCenters, takenImageCenters, n=15, distanceThreshold=5)
    transformedCenters = applyTransformation(takenImageCenters, transformation)
    # plt.scatter(transformedCenters[:, 0], transformedCenters[:, 1])


    correcpondingPointsNum = estimateTransformation(dbPoints, transformedCenters, 9)

    print("corresp num = " , correcpondingPointsNum)
    correctPercent = correcpondingPointsNum /  len(takenImageCenters)
    print("percent = ", correctPercent)
    isSame = estimateCloseness(correctPercent,2)


    return isSame


def estimateCloseness(k , level):
    if level == 3:
        b = k > 0.2
    elif level == 2:
        b = k > 0.4
    elif level == 1:
        b = k > 0.6
    return b


def prepareImage(img, invert = False):
    enhanced = enhanceImage(img)
    if invert:
        ret, enhanced = cv2.threshold(enhanced, 127, 255, cv2.THRESH_BINARY_INV)
    return enhanced


if __name__ == '__main__':
    plt.gca().invert_yaxis()
    initImg = cv2.imread('../fingerprints/all/0010_01.bmp', cv2.IMREAD_GRAYSCALE)
    cv2.imshow("Init", initImg)
    pointsA = np.load('testPoints1a.npy').astype(np.int64)
    print(pointsA.shape)
    plt.scatter(pointsA[:, 0], pointsA[:, 1], )

    img = cv2.imread('../fingerprints/all/0010_05.bmp', cv2.IMREAD_GRAYSCALE)
    cv2.imshow("Second", img)
    start_time = time.time()
    a = compareFingerprints(pointsA, img)
    print("--- %s seconds ---" % (time.time() - start_time))
    print(a)

    plt.show()

    cv2.waitKey()

