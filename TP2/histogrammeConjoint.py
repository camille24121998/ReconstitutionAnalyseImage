import numpy as np
import matplotlib.pyplot as plt

########################################
#   Partie 1 : Histogramme conjoint    #
########################################

# La fonction JoinHist calcule, affiche et renvoie l'histogramme join de deux images
# image1Copy et image2Copy sont des vecteurs contenant les images
def JoinHist(image1Copy, image2Copy) :
    indexes = [] # Cette liste contiendra, à chaque itération, les indices de chaque apparition d'un meme couple de valeur
    x = [] # x contiendra les valeurs de image1Copy sans répétitions des couples
    y = [] # y contiendra les valeurs de image2Copy sans répétitions des couples
    z = [] # z contiendra le nombre d'itération de chaque couple (x, y)
    # Tant que tous les couples n'ont pas été parcourus :
    while(len(image1Copy) != 0 and len(image2Copy) != 0) :
        # On récupere un coupe (val1, val2)
        val1 = image1Copy[0]
        val2 = image2Copy[0]
        # On récupere la liste des indices où ce couple apparait
        indexes1 = np.where(image1Copy == val1)[0]
        indexes2 = np.where(image2Copy == val2)[0]
        indexes = np.intersect1d(indexes1, indexes2)
        # On ajoute ce couple aux listes x, y, z
        x.append(val1)
        y.append(val2)
        z.append(len(indexes))
        # On supprime toutes les occurences de ce couple dans les deux images
        image1Copy = np.delete(image1Copy, indexes)
        image2Copy = np.delete(image2Copy, indexes)
    # Affichage de l'histogramme
    plot3 = plt.figure(3)
    ax = plt.axes()
    ax.set_facecolor('#000090')
    plt.scatter(x, y, s=1, c=z, cmap='rainbow') # On utilise un nuage de point avec l'échelle de couleur "Rainbow"
    plt.title('Histogramme conjoint')
    plt.xlabel('Image 1')
    plt.ylabel('Image 2')
    # On retourne tous les couples et leur nombre d'itération
    return (x, y, z)
