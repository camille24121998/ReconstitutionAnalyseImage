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
    NewI = np.zeros(I.shape)
    T = np.array([[1, 0, p], [0, 1, q], [0, 0, 1]])
    h,w = I.shape[:2]

    for i in range(h):
        for j in range(w):
            origin = np.array([j, i, 1])
            newXY = np.matmul(T, origin)
            newX = newXY[0]
            newY = newXY[1]

            if 0<newX<w and 0<newY<h:
                NewI[newY, newX] = I[i, j]
    return NewI