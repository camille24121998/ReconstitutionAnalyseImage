import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import argparse

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
    p.add_argument('image',
                   help="Images à traiter")

    arguments = p.parse_args()

    return arguments

def main():
    args = parse_args()
    img = plt.imread("Data/" + args.image)
    plt.imshow(img)
    plt.show()

    imgT = RecalageIconique.translation(img, 100.0, 100.0)
    plt.imshow(imgT)
    plt.show()

    JoinHist("Data/I5.jpg", "I6.jpg", 30)

if __name__ == "__main__":
    main()
