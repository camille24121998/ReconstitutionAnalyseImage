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

    if(np.shape(image1) != np.shape(image2)) :
        print("ERREUR : Les images ne sont pas de la même taille, l'histogramme conjoint ne peut pas être réaliser")
    else :
        tuples = (np.array((image1, image2)).T)[0]
        print(tuples)
        indexes = []
        x = []
        y = []
        z = []

        a = [1, 2, 3, 4, 5, 6, 7 ]
        b = a[0:3]+a[4:7]
        print(b)

        #while(tuples.size != 0) :
        val = tuples[0]
        print("val : ", val)
        for i in range(0, (tuples.shape)[0]-1) :
            if (tuples[i]==val).all() :
                indexes.append(i)
        print("shape of val : ", np.shape(val))
        x.append(val[0])
        y.append(val[1])
        z.append(len(indexes))
        print(tuples)
        indexes = []
        print("x : ", x, "\n y : ", y, "\n z : ", z)
        print(tuples)

        '''unique, counts = np.unique(tuples, return_counts=True)
        print("Unique : \n", unique)
        print("Counts : \n", counts)

        val = tuples[0]
        print(val)
        occurrences = np.count_nonzero(tuples == val)
        print(occurrences)
        tuples = tuples[tuples != val]
        print(tuples)'''

        '''plot3 = plt.figure(3)
        x = [1,2,3,4,5,6,7,8]
        y = [4,1,3,6,1,3,5,2]
        z = [10,2,2,1,1,2,1, 1]
        plt.scatter(x, y, s=500, c=z)
        plt.title('Histogramme conjoint')
        plt.xlabel('x')
        plt.ylabel('y')'''

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
        JoinHist("Data/I5.jpg", "Data/I6.jpg", 30)

    if args.question == "4a" :
        # Montre l'image de base
        img = plt.imread(images[4])
        plt.imshow(img)
        plt.show()
        # Montre l'image après la translation
        imgT = RecalageIconique.translation(img, 100, 100)
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

if __name__ == "__main__":
    main()
