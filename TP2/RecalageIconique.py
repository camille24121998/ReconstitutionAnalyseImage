import numpy as np
import scipy.ndimage
from scipy.ndimage import affine_transform
import nibabel as nib
import matplotlib.pyplot as plt
import imageio
import argparse
import glob

########################################
#   Partie 4 : Recalage iconique 2D    #
########################################


#
# translation(I, p, q) retourne une nouvelle image correspondant à lʼimage I translatée du vecteur t = (p, q)
#
# Pour faire cette fonction, je me suis inspiré du lien suivant :
#   https://medium.com/@bosssds65/translation-image-using-translation-matrix-with-python-d5d2b580d963
# Merci à son auteur
#
def translation(I, p, q):
    NewI = np.zeros(I.shape) # image translaté
    T = np.array([[1, 0, p], [0, 1, q], [0, 0, 1]]) # matrice de translation
    h, w = I.shape[:2]

    # Pour chaque pixel, on recalcule sa nouvelle coordonné
    for i in range(h):
        for j in range(w):
            origin = np.array([j, i, 1])
            newXY = np.matmul(T, origin)
            newX = round(newXY[0])
            newY = round(newXY[1])

            # Si la nouvelle coordonnée est toujours dans l'image on y met le pixel de la coordonnée original
            if 0 < newX < w and 0 < newY < h:
                NewI[newY, newX] = I[i, j]

    return NewI


#
# minSSDtranslation(I, J) retourne une nouvelle image correspondant à lʼimage I recalé sur l'image J
# Cette fonction fait un recalage 2D en minimisant la SSD et considérant uniquement des translations
#
def minSSDtranslation(I, J):
    e = 0.001
    h, w = I.shape[:2]

    # Ajoute des colonnes de 0 de chaque coté de l'image I
    bigIx = np.c_[np.zeros(h), I, np.zeros(h)]
    # Ajoute des lignes de 0 de chaque coté de l'image I
    bigIy = np.r_[[np.zeros(w)], I, [np.zeros(w)]]

    # Calcule les dérivés de l'image I par rapport à x et y
    dIx = np.array(bigIx[:, 0:-2] - bigIx[:, 2:])
    dIy = np.array(bigIy[0:-2, :] - bigIy[2:, :])

    p = 0
    q = 0
    for i in range(12):
        # Calcule le gradiant du SSD par rapport à p et q
        grad_SSD_p = 2 * np.sum(np.multiply((translation(I, p, q) - J), translation(dIx, p, q)))
        grad_SSD_q = 2 * np.sum(np.multiply((translation(I, p, q) - J), translation(dIy, p, q)))

        print("gradp = ", grad_SSD_p)
        print("gradq = ", grad_SSD_q)
        if abs(grad_SSD_p) < e and abs(grad_SSD_q) < e:
            break

        # Recalcule p et q pour améliorer le décalage
        p = p - 1.0/(i+1) * grad_SSD_p
        q = q - 1.0/(i+1) * grad_SSD_q

        print("newp = ",p)
        print("newq = ",q)
    return translation(I, p, q)

#
# rotation(I, theta) retourne une nouvelle image correspondant à lʼimage I a laquelle on a appliqué une rotation d'angle theta
#
# Pour faire cette fonction, j'ai repris la fonction tranlation,
# mais le lien suivant m'a donnée l'astuce du int(x) pour ne pas avoir de chiffre à virgule :
#   https://medium.com/@bosssds65/how-to-rotate-image-using-only-numpy-in-15-lines-ddc1fca93c87
# Merci à son auteur
#
def rotation(I, theta):
    NewI = np.zeros(I.shape) # image translaté
    T = np.array([[np.cos(theta), -np.sin(theta), 0.0], [np.sin(theta), np.cos(theta), 0.0], [0.0, 0.0, 1.0]]) # matrice de rotation
    h, w = I.shape[:2]

    # Pour chaque pixel, on recalcule sa nouvelle coordonné
    for i in range(h):
        for j in range(w):
            origin = np.array([j, i, 1])
            newXY = np.dot(T, origin)
            newX = round(newXY[0])
            newY = round(newXY[1])

            # Si la nouvelle coordonnée est toujours dans l'image on y met le pixel de la coordonnée original
            if 0 < newX < w and 0 < newY < h:
                NewI[newY, newX] = I[i, j]

    return NewI


#
# minSSDtranslation(I, J) retourne une nouvelle image correspondant à lʼimage I recalé sur l'image J
# Cette fonction fait un recalage 2D en minimisant la SSD et considérant uniquement des rotation
#
def minSSDrotation(I, J):
    h, w = I.shape[:2]

    # Ajoute des colonnes de 0 de chaque coté de l'image I
    bigIx = np.c_[np.zeros(h), I, np.zeros(h)]
    # Ajoute des lignes de 0 de chaque coté de l'image I
    bigIy = np.r_[[np.zeros(w)], I, [np.zeros(w)]]

    # Calcule les dérivés de l'image I par rapport à x et y
    dIx = np.array(bigIx[:, 0:-2] - bigIx[:, 2:])
    dIy = np.array(bigIy[0:-2, :] - bigIy[2:, :])

    theta = 0
    for i in range(12):
        #print("iteration = ", i)
        #print("theta = ", theta)
        # Calcule le gradiant du SSD par rapport à p et q
        cos = np.cos(theta)
        sin = np.sin(theta)
        #print("cos = ", cos)
        #print("sin = ", sin)
        x = np.arange(w)
        y = np.arange(h)
        a = (rotation(I, theta) - J)
        b = np.dot(rotation(dIx, theta), (-x*sin-y*cos))
        c = np.dot(rotation(dIy, theta), (x*cos-y*sin))
        #print("a=",a)
        #print("b=",b)
        #print(rotation(dIx, theta))
        #print("c=",c)
        #print(rotation(dIx, theta))
        grad_SSD_theta = 2 * sum(np.dot(a, (b + c)))
        #print("SSD = ", grad_SSD_theta)

        if grad_SSD_theta == 0:
            break

        # Recalcule p et q pour améliorer le décalage
        theta = theta - 1.0/(i+1) * grad_SSD_theta

    return rotation(I, theta)