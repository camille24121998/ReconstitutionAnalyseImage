import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import imageio
import argparse
import glob

########################################
#   Partie 1 : Histogramme conjoint    #
########################################

def JoinHist(I, J, bin) :
    print("test")
    image1 = plt.imread(I)
    plt.imshow(image1)
    plt.show()

########################################
#   Partie 4 : Recalage iconique 2D    #
########################################




############
#   Main   #
############
def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('path_images',
                   help="Dossier contenant les fichiers.")
    """
    p.add_argument('nb_bins', type=int,
                   help="Nombre de bins dans l'histogramme conjoint.")
    """
    arguments = p.parse_args()

    return arguments

def main():
    args = parse_args()

    for i in range(1, 6):
        print("*       Paire (I{}, J{})\n".format(i, i))

        filename_i = glob.glob(args.path_images + "I{}.*".format(i))
        filename_j = glob.glob(args.path_images + "J{}.*".format(i))
        print("Using files {} and {}".format(filename_i, filename_j))

        img_i = imageio.imread(filename_i[0])
        img_j = imageio.imread(filename_j[0])

    JoinHist("Data/I5.jpg", "I6.jpg", 30)

if __name__ == "__main__":
    main()
