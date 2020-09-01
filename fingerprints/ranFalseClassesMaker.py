import os
import cv2
import numpy as np
import random


source = 'enhanced/'
dest = 'enhancedRandomData2/'

files = os.listdir(source)
files.sort()

padding = 15

for file in files:
    image = cv2.imread(source + file, cv2.IMREAD_GRAYSCALE)
    croppedName = file[:-4]

    for i in range(150):
        row = random.randint(padding, image.shape[0]-padding)
        col = random.randint(padding, image.shape[1]-padding)

        try:
            cropped = image[row - padding:row + padding, col - padding:col + padding]
            cv2.imwrite(dest + croppedName + '_' + str(i) + '.bmp', cropped)
        except:
            print(f"Problem with writing mins in {i} row   file {file}")
            continue

print('DOne')