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
    print("test")
    image1 = plt.imread(I)
    plt.imshow(image1)
    plt.show()



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
        JoinHist("Data/I5.jpg", "I6.jpg", 30)

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
