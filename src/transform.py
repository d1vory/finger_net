import numpy as np
import cv2
import random
import math

#TODO find affine transformation using RANSAC algorithm

def eucDistance(pointA, pointB):
    return math.sqrt( float((pointA[0] - pointB[0])**2 +  (pointA[1] - pointB[1])**2) )

def randomPair(pointSet ):
    size = len(pointSet)
    if size < 2 :
        raise RuntimeError("size is to small")

    i = random.randint(0,size-1)
    j = random.randint(0,size-1)
    while i == j :
        j = random.randint(0,size-1)
    return pointSet[i] , pointSet[j]


def vectorAngle(pointA, pointB):
    try:
        return math.atan((pointB[1] - pointA[1] )  /  (pointB[0] - pointA[0] )  )
    except ZeroDivisionError:
        return math.atan((pointB[1] - pointA[1]) / (pointB[0] - pointA[0] + 0.000001))

def computeTransformation(pairA, pairB):
    # returns transformation between two pairs
    Aw, Bw = pairA
    Ai , Bi = pairB

    thetaA = vectorAngle(*pairA)
    thetaB = vectorAngle(*pairB)
    theta = thetaB - thetaA

    scale = (Bw[0] - Aw[0] ) / ( (math.cos(theta) * (Bi[0] - Ai[0]))  - (math.sin(theta) * (Ai[1] - Bi[1]) ))

    translX = Bw[0] - (Bi[0] * scale * math.cos(theta))  + (Bi[1] *  scale * math.sin(theta) )
    translY =  Bw[1] - (Bi[0] * scale * math.sin(theta))  - (Bi[1] * scale * math.cos(theta) )

    return np.array([  [scale*(math.cos(theta)) , (-1 * math.sin(theta)), translX],
                       [math.sin(theta), scale* math.cos(theta), translY],
                       [0   ,0    ,1]])


def applyTransformation(pointSet, transformation):
    res = []
    for point in pointSet:
        t = np.dot(transformation, np.array([[point[0]], [point[1]], [1]]) )
        res.append((t[0,0], t[1,0]))
    return np.array(res)

def estimateTransformation(setA , transformedB , threshold ):
    # returns number of minutiae which are close in fingerprint A
    # and in the transformed fingerprint B
    counter = 0
    for pointA in setA :
        for pointB in transformedB:
            distance = eucDistance(pointA,pointB)
            if distance < threshold:
                counter += 1

    return counter

def ransac(setA, setB, n,  distanceThreshold = 2):

    bestTransformation = None
    bestQuality = 0
    for k in range(n):
        a1 ,a2 = randomPair(setA)
        aDistanse = eucDistance(a1,a2)
        sizeb = len(setB)
        for i in range(sizeb):
            for j in range(sizeb):
                if i != j:
                    if math.fabs(eucDistance(setB[i], setB[j]) - aDistanse) <= distanceThreshold:
                        transformation = computeTransformation(pairA=(a1, a2), pairB=(setB[i], setB[j]))
                        transformedSet = applyTransformation(setB, transformation)

                        quality = estimateTransformation(setA, transformedSet ,distanceThreshold)

                        if quality > bestQuality:
                            bestQuality = quality
                            bestTransformation = transformation

    return bestTransformation, bestQuality