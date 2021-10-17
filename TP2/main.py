import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import argparse
from os import listdir
from os.path import isfile, join

import RecalageIconique

########################################
#   Partie 1 : Histogramme conjoint    #
########################################

def JoinHist(I, J, bin) :
    plot1 = plt.figure(1)
    image1 = plt.imread(I)
    plt.imshow(image1)

    plot2 = plt.figure(2)
    image2 = plt.imread(J)
    plt.imshow(image2)

    print(image1)
    print(np.shape(image1))
    print(image2)
    print(np.shape(image2))

    if(np.shape(image1) != np.shape(image2)) :
        print("ERREUR : Les images ne sont pas de la même taille, l'histogramme conjoint ne peut pas être réaliser")
    else :
        image1Copy = image1.flatten()
        image2Copy = image2.flatten()
        '''tuples = (np.array((image1, image2)).T)[0]
        print(tuples)'''
        indexes = []
        x = []
        y = []
        z = []

        '''a = [1, 2, 3, 4, 5, 6, 7 ]
        b = a[0:3]+a[4:7]
        print(b)'''

        '''while(len(image1Copy) != 0) :
            val1 = image1Copy[0]
            val2 = image2Copy[0]
            for i in range(0, len(image1Copy)) :
                if (image1Copy[i]==val1 and image2Copy[i]==val2) :
                    indexes.append(i)
            x.append(val1)
            y.append(val2)
            z.append(len(indexes))
            image1Copy = np.delete(image1Copy, indexes)
            image2Copy = np.delete(image2Copy, indexes)
            indexes = []
            print(image1Copy)
            print(len(image1Copy))
            print(image2Copy)
            print(len(image2Copy))'''

        while(len(image1Copy) != 0) :
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
            '''print(image1Copy)
            print(len(image1Copy))
            print(image2Copy)
            print(len(image2Copy))'''



        '''unique, counts = np.unique(tuples, return_counts=True)
        print("Unique : \n", unique)
        print("Counts : \n", counts)

        val = tuples[0]
        print(val)
        occurrences = np.count_nonzero(tuples == val)
        print(occurrences)
        tuples = tuples[tuples != val]
        print(tuples)'''

        plot3 = plt.figure(3)
        ax = plt.axes()
        ax.set_facecolor('#000090')
        plt.scatter(x, y, s=1, c=z, cmap='rainbow')
        plt.title('Histogramme conjoint')
        plt.xlabel('x')
        plt.ylabel('y')

        '''plot4 = plt.figure(4)
        plt.hist2d(image1.flatten(), image2.flatten(), bins=1000)'''

        plt.show()

    '''
    plot1 = plt.figure(1)
    image1 = (np.matrix(plt.imread(I))).flatten()
    plt.imshow(image1)

    print("Image1 : ", image1)
    print(image1[0][0])

    plot2 = plt.figure(2)
    image2 = (np.matrix(plt.imread(J))).flatten()
    plt.imshow(image2)

    plot3 = plt.figure(3)
    plt.hist(image1)

    print(np.shape(image1))

    plot4 = plt.figure(4)
    #h, x, y = plt.hist2d(image1[0],image2[0])
    #plt.hexbin(image1,image2, bins=bin)

    #plot5 = plt.figure(5)
    #np.histogram2d(image1[0], image2[0])

    plt.show()
    '''


############
#   Main   #
############
def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('path_images',
                   help="Dossier des images à traiter")

    p.add_argument('question',
                   help="Question à tester - ex : 1a")

    arguments = p.parse_args()

    return arguments

def main():
    args = parse_args()

    images = [args.path_images+f for f in listdir(args.path_images) if isfile(join(args.path_images, f))]

    if args.question == "1a":
        JoinHist("Data/I2.jpg", "Data/J2.jpg", 30)

    if args.question == "4a" :
        # Montre l'image de base
        img = plt.imread(images[4])
        plt.imshow(img)
        plt.show()
        # Montre l'image après la translation
        imgT = RecalageIconique.translation(img, 12, 15)
        plt.imshow(imgT)
        plt.show()

    if args.question == "4b" :
        I = plt.imread(images[0])
        plt.imshow(I)
        plt.show()
        J = plt.imread(images[1])
        plt.imshow(J)
        plt.show()
        newI = RecalageIconique.minSSDtranslation(I, J)
        plt.imshow(newI)
        plt.show()

    if args.question == "4c" :
        # Montre l'image de base
        img = plt.imread(images[4])
        plt.imshow(img)
        plt.show()
        # Montre l'image après la translation
        imgT = RecalageIconique.rotation(img, 50)
        plt.imshow(imgT)
        plt.show()

    if args.question == "4d" :
        I = plt.imread(images[2])
        plt.imshow(I)
        plt.show()
        J = plt.imread(images[3])
        plt.imshow(J)
        plt.show()
        newI = RecalageIconique.minSSDrotation(I, J)
        plt.imshow(newI)
        plt.show()

if __name__ == "__main__":
    main()
