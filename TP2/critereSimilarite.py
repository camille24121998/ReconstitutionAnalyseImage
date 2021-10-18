import numpy as np
import matplotlib.pyplot as plt
import math

import histogrammeConjoint

##########################################
#   Partie 2 :  Critère de similarité    #
##########################################

def SSD(image1Copy, image2Copy) :
    ssd = (np.sum(image1Copy) - np.sum(image2Copy))**2
    print("SSD = ", ssd)
    return ssd

def CR(image1Copy, image2Copy) :
    moyI1 = np.average(image1Copy)
    moyI2 = np.average(image2Copy)
    diffAlaMoyI1 = np.subtract(image1Copy, moyI1)
    diffAlaMoyI2 = np.subtract(image2Copy, moyI2)
    numerateur = np.sum(diffAlaMoyI1*diffAlaMoyI2)
    varianceI1 = math.sqrt(np.sum(np.power(diffAlaMoyI1, 2)))
    varianceI2 = math.sqrt(np.sum(np.power(diffAlaMoyI2, 2)))
    denominateur = varianceI1*varianceI2
    cr = numerateur/denominateur
    print("Coefficient de corelation : ", cr)
    return cr

def IM(image1Copy, image2Copy) :
    (x, y, h) = histogrammeConjoint.JoinHist(image1Copy, image2Copy)
    xCopy = np.array(x)
    yCopy = np.array(y)
    hCopy = np.array(h)

    sumH = np.sum(h)
    MI = 0
    print("Attendez, c'est long, nous n'avons pas réussi à vectoriser le code")
    for i in range(0, len(xCopy)-1):
        pij = (hAB(xCopy[i], yCopy[i], xCopy, yCopy, hCopy)/sumH)
        MI = MI + pij*math.log((pij/(sumB(xCopy[i], xCopy, yCopy, hCopy)*sumA(yCopy[i], xCopy, yCopy, hCopy))), 2)
    print("Information mutuelle = ", MI)
    plt.show()

def hAB(a, b, x, y, h) :
    indexesX = np.where(x == a)[0]
    indexesY = np.where(y == b)[0]
    indexes = np.intersect1d(indexesX, indexesY)
    if(len(indexes)>0) :
        index = indexes[0]
    else :
        index = -1
    return h[index]

def sumB(a, x, y, h) :
    indexesX = np.where(x == a)[0]
    sumH = np.sum(h)
    sumB = 0
    if(len(indexesX)>0) :
        for i in indexesX :
            sumB = hAB(a, y[i], x, y, h)
        sumB = sumB/sumH
    return sumB

def sumA(b, x, y, h) :
    indexesY = np.where(y == b)[0]
    sumH = np.sum(h)
    sumA = 0
    if(len(indexesY)>0) :
        for i in indexesY :
            sumA = hAB(x[i], b, x, y, h)
        sumA = sumA/sumH
    return sumA
