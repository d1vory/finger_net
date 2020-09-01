import cv2
import pandas as pd
import random
import os
import numpy as np
from PIL import Image


def makeDatasetFromDirs(src, val, padding):
    files = os.listdir(src)
    imagesList = []
    labels = []

    for filename in files:
        try:
            img = cv2.imread(src + filename, cv2.IMREAD_GRAYSCALE)

            arr = np.asarray(img)
            width, height = arr.shape
            if width != padding:
                padw = padding - width
                arr = np.pad(arr, pad_width=((padw, 0), (0, 0)), mode='edge')
            if height != padding:
                padh = padding - height
                arr = np.pad(arr, pad_width=((0, 0), (padh, 0)), mode='edge')
            arr = arr.reshape(padding, padding, 1)
        except:
            print("error at ", filename)
            continue

        imagesList.append(arr)
        labels.append(val)
    return imagesList, labels


def makeDatasetFromCsv(csvFileName, val, source, padding, invert = False, size = None):
    df = pd.read_csv(csvFileName, index_col=False, header=0)
    arr = df['0']

    imagesList = []
    labels = []
    print(arr[10],"        KEKEKEKKE")
    for filename in arr:
        if size != None and size <= len(imagesList):
            break
        try:
            #img = Image.open(source + filename)
            img = cv2.imread(source + filename, cv2.IMREAD_GRAYSCALE)
            if invert:
                ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
            if np.mean(img) == 255:
                continue

            arr = np.asarray(img)
            width,height = arr.shape
            if width != padding :
                padw = padding - width
                arr = np.pad(arr,pad_width=((padw,0),(0,0)), mode = 'edge')
            if height != padding:
                padh = padding - height
                arr = np.pad(arr, pad_width=( (0, 0),(padh, 0)), mode='edge')
            arr  = arr.reshape(padding,padding,1)
        except:
            print("erroe at ", filename)
            continue
        imagesList.append(arr)
        labels.append(val)

    return  imagesList, labels




trueImgs, trueLabels = makeDatasetFromDirs('temp2/true/', val = 1, padding = 30)
print("shape1 ", len(trueImgs))
falseImgs, falseLabels = makeDatasetFromDirs('temp2/false2/', val = 0, padding = 30)
print("shape2 ", (falseImgs))

resImgs = trueImgs + falseImgs
reslabels = trueLabels + falseLabels

resx = np.asarray(resImgs)
resy = np.asarray(reslabels)

print(resx.shape)
print(resy.shape)

dist = 'datasets/8/'

np.save(dist + 'x_data8.npy', resx)
np.save(dist + 'y_data8.npy', resy)

print("Done")




