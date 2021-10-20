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
    NewI = np.zeros(I.shape)
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
    h, w = I.shape[:2]
    energieSSD = np.array([])

    p = 0
    q = 0
    for i in range(25):
        print("Itération ", i)
        # Translation de l'image I
        I_tmp = translation(I, p, q)

        # Ajoute des colonnes de 0 de chaque coté de l'image I
        bigIx = np.c_[np.zeros(h), I_tmp, np.zeros(h)]
        # Ajoute des lignes de 0 de chaque coté de l'image I
        bigIy = np.r_[[np.zeros(w)], I_tmp, [np.zeros(w)]]

        # Calcule les dérivés de l'image I par rapport à x et y
        dIx = np.array(bigIx[:, 0:-2] - bigIx[:, 2:])
        dIy = np.array(bigIy[0:-2, :] - bigIy[2:, :])

        # Calcule le gradiant du SSD par rapport à p et q
        grad_SSD_p = 2 * np.sum(np.multiply((translation(I, p, q) - J), dIx))
        grad_SSD_q = 2 * np.sum(np.multiply((translation(I, p, q) - J), dIy))

        print("gradp = ", grad_SSD_p)
        print("gradq = ", grad_SSD_q)

        if grad_SSD_p == 0 and grad_SSD_q == 0:
            break

        # Recalcule p et q pour améliorer le décalage
        #p = p - 1.0/(i+1) * grad_SSD_p
        #q = q - 1.0/(i+1) * grad_SSD_q
        p = p - 0.00003/np.power(2, i) * grad_SSD_p
        q = q - 0.00003/np.power(2, i) * grad_SSD_q

        print("newp = ", p)
        print("newq = ", q)

        # Calcule du SSD
        SSD = np.sum(np.power(translation(I, p, q)-J, 2))
        energieSSD = np.append(energieSSD, SSD)
        print("energieSSD = ", energieSSD)

    plt.plot(energieSSD)
    plt.show()

    return translation(I, p, q)

#
# rotation(I, theta) retourne une nouvelle image correspondant à lʼimage I a laquelle on a appliqué une rotation d'angle theta
# Pour faire cette fonction, j'ai repris la fonction tranlation, et me suis inspiré du lien suivant pour quelque détail :
#   https://medium.com/@bosssds65/how-to-rotate-image-using-only-numpy-in-15-lines-ddc1fca93c87
# Merci à son auteur
#
def rotation(I, theta):
    theta = theta * (np.pi/180)
    NewI = np.zeros(I.shape)
    R = np.transpose(np.array([[np.cos(theta), -np.sin(theta), 0.0], [np.sin(theta), np.cos(theta), 0.0], [0.0, 0.0, 1.0]])) # matrice de rotation
    h, w = I.shape[:2]

    # Pour chaque pixel, on recalcule sa nouvelle coordonné
    for i in range(h):
        for j in range(w):
            origin = np.array([j, i, 1])
            newXY = np.dot(R, origin)
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

    energieSSD = np.array([])

    theta = 1
    for i in range(25):
        print("Itération ", i)
        # Rotation de l'image I
        I_tmp = rotation(I, theta)
        #print("I_tmp = \n", I_tmp)

        # Ajoute des colonnes de 0 de chaque coté de l'image I
        bigIx = np.c_[np.zeros(h), I_tmp, np.zeros(h)]
        # Ajoute des lignes de 0 de chaque coté de l'image I
        bigIy = np.r_[[np.zeros(w)], I_tmp, [np.zeros(w)]]

        # Calcule les dérivés de l'image I par rapport à x et y
        dIx = np.array(bigIx[:, 0:-2] - bigIx[:, 2:])
        dIy = np.array(bigIy[0:-2, :] - bigIy[2:, :])

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
        b = np.multiply(dIx, np.matmul(-x.T * sin, -y * cos))
        c = np.multiply(dIy, np.matmul(x.T * cos, -y * sin))
        #print("a=",a)
        #print("b=",b)
        #print("c=",c)
        #print(dIx)
        #print(rotation(dIy, theta))
        grad_SSD_theta = 2 * np.sum(np.multiply(a, (b + c)))

        print("grad_SSD = ", grad_SSD_theta)

        if grad_SSD_theta == 0:
            break

        # Recalcule p et q pour améliorer le décalage
        #theta = theta - 1.0/(i+1) * grad_SSD_theta
        theta = theta - 0.0000000000001 / np.power(2, i) * grad_SSD_theta
        print("newt= ", theta)

        # Calcule du SSD
        SSD = np.sum(np.power(rotation(I, theta) - J, 2))
        energieSSD = np.append(energieSSD, SSD)
        print("energieSSD = ", energieSSD)

    plt.plot(energieSSD)
    plt.show()

    return rotation(I, theta)

#
# transRot(I, p, q, theta)
# retourne une nouvelle image correspondant à lʼimage I a laquelle on a appliqué une translation de p et q, et une rotation d'angle theta
#
def transRot(I, p, q, theta):
    NewI = np.zeros(I.shape)
    theta = theta * (np.pi / 180)
    T = np.transpose(np.array([[np.cos(theta), -np.sin(theta), p], [np.sin(theta), np.cos(theta), q], [0, 0, 1]]))  # matrice de transformation
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
# minSSD(I, J) retourne une nouvelle image correspondant à lʼimage I recalé sur l'image J
# Cette fonction fait un recalage 2D en minimisant la SSD en utilisant des translations et rotation
#
def minSSD(I, J):
    h, w = I.shape[:2]

    energieSSD = np.array([])

    p = 0
    q = 0
    theta = 1
    for i in range(25):
        print("Itération ", i)
        # Translation de l'image I
        I_tmp = transRot(I, p, q, theta)

        # Ajoute des colonnes de 0 de chaque coté de l'image I
        bigIx = np.c_[np.zeros(h), I_tmp, np.zeros(h)]
        # Ajoute des lignes de 0 de chaque coté de l'image I
        bigIy = np.r_[[np.zeros(w)], I_tmp, [np.zeros(w)]]

        # Calcule les dérivés de l'image I par rapport à x et y
        dIx = np.array(bigIx[:, 0:-2] - bigIx[:, 2:])
        dIy = np.array(bigIy[0:-2, :] - bigIy[2:, :])

        # Calcule le gradiant du SSD par rapport à p, q et theta
        grad_SSD_p = 2 * np.sum(np.multiply((translation(I, p, q) - J), dIx))
        grad_SSD_q = 2 * np.sum(np.multiply((translation(I, p, q) - J), dIy))
        cos = np.cos(theta)
        sin = np.sin(theta)
        x = np.arange(w)
        y = np.arange(h)
        a = (rotation(I, theta) - J)
        b = np.multiply(dIx, np.matmul(-x.T * sin, -y * cos))
        c = np.multiply(dIy, np.matmul(x.T * cos, -y * sin))
        grad_SSD_theta = 2 * np.sum(np.multiply(a, (b + c)))

        print("gradP = ", grad_SSD_p)
        print("gradQ = ", grad_SSD_q)
        print("gradTheta = ", grad_SSD_theta)

        if grad_SSD_p == 0 and grad_SSD_q == 0 and grad_SSD_theta == 0:
            break

        # Recalcule p, q et theta pour améliorer le décalage
        p = p - 0.00003 / np.power(2, i) * grad_SSD_p
        q = q - 0.00003 / np.power(2, i) * grad_SSD_q
        theta = theta - 0.0000000000001 / np.power(2, i) * grad_SSD_theta

        print("newp = ", p)
        print("newq = ", q)
        print("newt= ", theta)

        # Calcule du SSD
        SSD = np.sum(np.power(transRot(I, p, q, theta) - J, 2))
        energieSSD = np.append(energieSSD, SSD)
        print("energieSSD = ", energieSSD)

    plt.plot(energieSSD)
    plt.show()

    return transRot(I, p, q, theta)