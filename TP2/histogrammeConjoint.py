import numpy as np
import matplotlib.pyplot as plt

########################################
#   Partie 1 : Histogramme conjoint    #
########################################

def JoinHist(image1Copy, image2Copy) :
    indexes = []
    x = []
    y = []
    z = []

    while(len(image1Copy) != 0 and len(image2Copy) != 0) :
        val1 = image1Copy[0]
        indexes1 = np.where(image1Copy == val1)[0]
        val2 = image2Copy[0]
        indexes2 = np.where(image2Copy == val2)[0]
        indexes = np.intersect1d(indexes1, indexes2)
        x.append(val1)
        y.append(val2)
        z.append(len(indexes))
        image1Copy = np.delete(image1Copy, indexes)
        image2Copy = np.delete(image2Copy, indexes)
        indexes = []

    plot3 = plt.figure(3)
    ax = plt.axes()
    ax.set_facecolor('#000090')
    plt.scatter(x, y, s=1, c=z, cmap='rainbow')
    plt.title('Histogramme conjoint')
    plt.xlabel('Image 1')
    plt.ylabel('Image 2')

    return (x, y, z)
