import numpy as np
import matplotlib.pyplot as plt
import math

import histogrammeConjoint

##########################################
#   Partie 2 :  Critère de similarité    #
##########################################

# La fonction SSD calcule, affiche et retourne la différence des somme au carré de deux images
# image1Copy et image2Copy sont des vecteurs contenant les images
def SSD(image1Copy, image2Copy) :
    ssd = (np.sum(image1Copy) - np.sum(image2Copy))**2
    print("SSD = ", ssd)
    return ssd

# La fonction CR calcule, affiche et retourne le coefficient de corelation de deux images
# image1Copy et image2Copy sont des vecteurs contenant les images
def CR(image1Copy, image2Copy) :
    # On calcule la moyenne des intensité de chaques image
    moyI1 = np.average(image1Copy)
    moyI2 = np.average(image2Copy)
    # diffALaMoy est un vecteur contenant les différences de chaque intensité et de la moyenne
    diffAlaMoyI1 = np.subtract(image1Copy, moyI1)
    diffAlaMoyI2 = np.subtract(image2Copy, moyI2)
    # Le numerateur du coefficient de corelation est la somme du produit des différences à la moyenne des deux images
    numerateur = np.sum(diffAlaMoyI1*diffAlaMoyI2)
    # On calcule ensuite la variance des deux images
    varianceI1 = math.sqrt(np.sum(np.power(diffAlaMoyI1, 2)))
    varianceI2 = math.sqrt(np.sum(np.power(diffAlaMoyI2, 2)))
    # Le dénominateur du coefficient de corelation est le produit des deux variances
    denominateur = varianceI1*varianceI2
    # Calcul du coefficient de correlation
    cr = numerateur/denominateur
    # Affichage du coefficient de correlation
    print("Coefficient de corelation : ", cr)
    return cr

# La fonction IM calcule, affiche et retourne l'information mutuelle de deux images
# image1Copy et image2Copy sont des vecteurs contenant les images
def IM(image1Copy, image2Copy) :
    # On utilise l'histogramme conjoint pour calculer l'information mutuelle
    (x, y, h) = histogrammeConjoint.JoinHist(image1Copy, image2Copy)
    # On normalise l'histogramme (on converti ses valeurs pour qu'elles soient dans l'interval (-1, 1))
    sumH = sum(h)
    h = [x/sumH for x in h]
    # On converti les listes x, y et h en vecteurs
    xCopy = np.array(x)
    yCopy = np.array(y)
    hCopy = np.array(h)
    # On calcule l'information mutuelle
    MI = 0
    print("Attendez, c'est long, nous n'avons pas réussi à vectoriser le code")
    for i in range(0, len(xCopy)-1):
        pij = (hAB(xCopy[i], yCopy[i], xCopy, yCopy, hCopy))
        MI = MI + pij*math.log((pij/(sumB(xCopy[i], xCopy, yCopy, hCopy)*sumA(yCopy[i], xCopy, yCopy, hCopy))), 2)
    print("Information mutuelle = ", MI)
    return MI
# Fonction auxiliere à la donction IM
# Cette fonction renvoit la veleur de l'histogramme pour un certain couple d'intensité (a, b)
def hAB(a, b, x, y, h) :
    indexesX = np.where(x == a)[0]
    indexesY = np.where(y == b)[0]
    indexes = np.intersect1d(indexesX, indexesY)
    if(len(indexes)>0) :
        index = indexes[0]
    else :
        index = -1
    return h[index]
# Fonction auxiliere à la donction IM
# Cette fonction calcule la somme de toutes les intensités dans y correspondant à une intensité a dans x
def sumB(a, x, y, h) :
    indexesX = np.where(x == a)[0]
    sumB = 0
    if(len(indexesX)>0) :
        for i in indexesX :
            sumB = sumbB + hAB(a, y[i], x, y, h)
    return sumB
# Fonction auxiliere à la donction IM
# Cette fonction calcule la somme de toutes les intensités dans x correspondant à une intensité b dans y
def sumA(b, x, y, h) :
    indexesY = np.where(y == b)[0]
    sumA = 0
    if(len(indexesY)>0) :
        for i in indexesY :
            sumA = sumA + hAB(x[i], b, x, y, h)
    return sumA
