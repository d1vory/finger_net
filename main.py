from myEnhancement/enhance import enhanceImage
from src/matching import compareFingerprints
import mysql.connector
from mysql.connector import Error
import serial
from PIL import Image

def getTemplates():
    resultedSet = []
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='fingerprints',
                                             user='olexandr2',
                                             password='1234')

        cursor = connection.cursor()
        fingerprintNums = cursor.execute('SELECT num FROM Fingerprint')

        for num in fingerprintNums:
            template = cursor.execute('SELECT x,y FROM Point WHERE num == fingerprint_num')
            resultedSet.append(template)
    except Error as e:
        print("error in reading database: ", e)

    return resultedSet


def checkSimilarity(takenFingerprint, template):
    for dbTemplate in template:
        isSimilar = compareFingerprints(dbTemplate, takenFingerprint)
        if isSimilar:
            return True

def getImage():
    try:
        b = tobytes("xbm", "grayscale")
        img = Image.frombuffer("L", (256, 288), b, 'raw', "L", 0, 1)
    except Error:
        print(Error)
        img = None
    return img

def openDoor(arduino):
    arduino.write("rotate")


def door():
    templates = getTemplates()
    arduino = serial.Serial('COM3', 9600)
    while True:
        takenFingerprint= getImage()
        isRecognized = checkSimilarity(takenFingerprint,templates)
        if isRecognized:
            openDoor(arduino)