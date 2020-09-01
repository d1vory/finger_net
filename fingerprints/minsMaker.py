import cv2
import pandas
import random
import os
import numpy as np



def makeMins(file, padding, imgSource = 'enhanced/', csvSource = 'csvData/' , minsDest = 'enhancedMinsData/'):

    try:
        image  = cv2.imread(imgSource + file,cv2.IMREAD_GRAYSCALE)
        ret, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
        height,width = image.shape
        croppedName = file[:-4]
        data  = pandas.read_csv(csvSource + croppedName + '.csv')
    except:
        print("cant open file ", file)
        return

    for i in range(len(data)):
        row = data['rows'][i] + random.randint(-7,7)
        col = data['cols'][i] + random.randint(-7,7)
        try:

            cropped = image[row - padding:row + padding, col - padding:col + padding]
            cv2.imwrite(minsDest + croppedName + '_' + str(i) + '.bmp', cropped )
        except:

            #print(f"Problem with writing mins in {i} row   file {file}")
            continue



files = os.listdir('enhanced/')
for file in files:
    makeMins(file,15 , minsDest = 'enhancedMarginMinsData')

print('DOne')