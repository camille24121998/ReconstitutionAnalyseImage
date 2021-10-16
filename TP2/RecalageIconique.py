import numpy as np
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
def translation(I, p, q) :
    NewI = np.zeros(I.shape) # image translaté
    T = np.array([[1, 0, p], [0, 1, q], [0, 0, 1]]) # matrice de translation
    h,w = I.shape[:2]

    # Pour chaque pixel, on recalcule sa nouvelle coordonné
    for i in range(h):
        for j in range(w):
            origin = np.array([j, i, 1])
            newXY = np.matmul(T, origin)
            newX = newXY[0]
            newY = newXY[1]

            # Si la nouvelle coordonnée est toujours dans l'image on y met le pixel de la coordonnée original
            if 0<newX<w and 0<newY<h:
                NewI[newY, newX] = I[i, j]

    return NewI

#
# minSSDtranslation(I, J) retourne une nouvelle image correspondant à lʼimage I recalé sur l'image J
# Cette fonction fait un recalage 2D en minimisant la SSD et considérant uniquement des translations
#
def minSSDtranslation(I, J) :
    h,w = I.shape[:2]

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
        grad_SSD_p = 2 * np.matmul((translation(I, p, q) - J), translation(dIx, p, q))
        grad_SSD_q = 2 * np.matmul((translation(I, p, q) - J), translation(dIy, p, q))

        if grad_SSD_p.all() == 0 and grad_SSD_q.all() == 0:
            break

        # Recalcule p et q pour améliorer le décalage
        p = p - grad_SSD_p
        q = q - grad_SSD_q

    return translation(I, p, q)