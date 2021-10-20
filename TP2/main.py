import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import argparse
from os import listdir
from os.path import isfile, join

import RecalageIconique
import TransformationSpatiale
import histogrammeConjoint
import critereSimilarite

########################################################################
#   Fonction auxiliere d'affichage d'image et de test de dimensions    #
########################################################################

def transformeImageIntoVector(I, J) :
    plot1 = plt.figure(1)
    image1 = plt.imread(I)
    plt.imshow(image1)

    plot2 = plt.figure(2)
    image2 = plt.imread(J)
    plt.imshow(image2)

    sameDim = np.shape(image1) == np.shape(image2)
    if sameDim == False :
        print("ERREUR : Les images ne sont pas de la même taille, l'histogramme conjoint ne peut pas être réaliser")

    return (sameDim, image1.flatten(), image2.flatten())

############
#   Main   #
############
def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument('fonction',
                   help="Fonctionnalité à utiliser \n valeur possible :"
                        "\n\tjointHist"
                        "\n\tssd"
                        "\n\tcr"
                        "\n\tim"
                        "\n\tregularGrille\t   *si"
                        "\n\ttrans_rigide\t   *si"
                        "\n\tsimilitude\t   *si"
                        "\n\ttypeTransformation *si"
                        "\n\tminSSDtranslation"
                        "\n\tminSSDrotation"
                        "\n\tminSSD"
                        "\n*si = sans image")

    p.add_argument('imageI',
                   help="Image à traiter",
                   nargs='?',
                   default="Data/BrainMRI_2.jpg")

    p.add_argument('imageJ',
                   help="Image cible",
                   nargs='?',
                   default="Data/BrainMRI_1.jpg")

    arguments = p.parse_args()

    return arguments

def main():
    args = parse_args()

    ############
    # Partie 1 #
    ############

    if args.fonction == "joinHist":
        (sameDim, image1Copy, image2Copy) = transformeImageIntoVector(args.imageI, args.imageJ)
        if(sameDim == True) :
            histogrammeConjoint.JoinHist(image1Copy, image2Copy)
        plt.show()

    ############
    # Partie 2 #
    ############

    if args.fonction == "ssd" :
        (sameDim, image1Copy, image2Copy) = transformeImageIntoVector(args.imageI, args.imageJ)
        if(sameDim == True) :
            critereSimilarite.SSD(image1Copy, image2Copy)

    if args.fonction == "cr" :
        (sameDim, image1Copy, image2Copy) = transformeImageIntoVector(args.imageI, args.imageJ)
        if(sameDim == True) :
            critereSimilarite.CR(image1Copy, image2Copy)

    if args.fonction == "im" :
        (sameDim, image1Copy, image2Copy) = transformeImageIntoVector(args.imageI, args.imageJ)
        if(sameDim == True) :
            critereSimilarite.IM(image1Copy, image2Copy)

    ############
    # Partie 3 #
    ############

    if args.fonction == "regularGrille":
        x, y, z = (20, 20, 4)
        xs, ys, zs = TransformationSpatiale.genererGrille(x,y,z)
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        ax.set_xlim([0, x*2])
        ax.set_ylim([0, y*2])
        ax.set_zlim([0, z*2+15])

        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        ax.scatter(xs, ys, zs)
        plt.show()

    if args.fonction == "trans_rigide":
        x, y, z = (20, 20, 4)
        xs, ys, zs = TransformationSpatiale.genererGrille(x,y,z)

        theta = 13
        omega = 0
        phi = 0
        p = 0
        q = 0
        r = 10
        Transformation_Matrix = TransformationSpatiale.trans_rigide(theta,omega,phi,p,q,r)

        for p in range(x*y*z) :
            trans_p = np.matmul(Transformation_Matrix,np.transpose([xs[p],ys[p],zs[p],1]))
            xs[p] = trans_p[0]
            ys[p] = trans_p[1]
            zs[p] = trans_p[2]


        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        ax.set_xlim([0, x*2])
        ax.set_ylim([0, y*2])
        ax.set_zlim([0, z*2+15])

        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        ax.scatter(xs, ys, zs)
        plt.show()

    if args.fonction == "similitude":
        x, y, z = (20, 20, 4)
        xs, ys, zs = TransformationSpatiale.genererGrille(x,y,z)

        s = 0.5
        theta = 90
        omega = 45
        phi = 0
        p = 0
        q = 0
        r = 0
        Transformation_Matrix = TransformationSpatiale.similitude(s,theta,omega,phi,p,q,r)

        for p in range(x*y*z) :
            trans_p = np.matmul(Transformation_Matrix,np.transpose([xs[p],ys[p],zs[p],1]))
            xs[p] = trans_p[0]
            ys[p] = trans_p[1]
            zs[p] = trans_p[2]


        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        ax.set_xlim([0, x*2])
        ax.set_ylim([0, y*2])
        ax.set_zlim([0, z*2+15])

        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        ax.scatter(xs, ys, zs)
        plt.show()

    if args.fonction == "typeTransformation":
        x, y, z = (20, 20, 4)
        xs, ys, zs = TransformationSpatiale.genererGrille(x,y,z)

        M1 = [[0.9045,-0.3847,-0.1840,10.0000],[0.2939, 0.8750,-0.3847,10.0000],[0.3090, 0.2939, 0.9045,10.0000],[0,0,0,1.0000]]
        M2 = [[-0.0000,-0.2598, 0.1500,-3.0000],[0.0000,-0.1500,-0.2598, 1.5000],[0.3000,-0.0000, 0.0000,0],[0,0,0,1.0000]]
        M3 = [[0.7182,-1.3727,-0.5660, 1.8115],[-1.9236,-4.6556,-2.5512, 0.2873],[-0.6426,-1.7985,-1.6285, 0.7404],[0,0,0,1.0000]]

        for p in range(x*y*z) :
            trans_p = np.matmul(M2,np.transpose([xs[p],ys[p],zs[p],1]))
            xs[p] = trans_p[0]
            ys[p] = trans_p[1]
            zs[p] = trans_p[2]


        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        ax.set_xlim([0, x*2])
        ax.set_ylim([0, y*2])
        ax.set_zlim([0, z*2+15])

        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        ax.scatter(xs, ys, zs)
        plt.show()

    ############
    # Partie 4 #
    ############
    if args.fonction == "minSSDtranslation":
        I = plt.imread(args.imageI)
        plt.imshow(I)
        plt.show()
        J = plt.imread(args.imageJ)
        plt.imshow(J)
        plt.show()
        newI = RecalageIconique.minSSDtranslation(I, J)
        plt.imshow(newI)
        plt.show()

    if args.fonction == "minSSDrotation":
        I = plt.imread(args.imageI)
        plt.imshow(I)
        plt.show()
        J = plt.imread(args.imageJ)
        plt.imshow(J)
        plt.show()
        newI = RecalageIconique.minSSDrotation(I, J)
        plt.imshow(newI)
        plt.show()

    if args.fonction == "minSSD":
        I = plt.imread(args.imageI)
        plt.imshow(I)
        plt.show()
        J = plt.imread(args.imageJ)
        plt.imshow(J)
        plt.show()
        newI = RecalageIconique.minSSD(I, J)
        plt.imshow(newI)
        plt.show()

if __name__ == "__main__":
    main()
