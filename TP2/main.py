import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import argparse
import math
from os import listdir
from os.path import isfile, join

import RecalageIconique
import TransformationSpatiale

########################################################################
#   Fonction auxiliere d'affichage d'image et de test de dimensions    #
########################################################################

def transformeImageIntoMatrix(I, J) :
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

########################################
#   Partie 1 : Histogramme conjoint    #
########################################

def JoinHist(I, J, bin) :
    (sameDim, image1Copy, image2Copy,) = transformeImageIntoMatrix(I, J)

    if(sameDim == True) :
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

##########################################
#   Partie 2 :  Critère de similarité    #
##########################################

def SSD(I, J) :
    (sameDim, image1Copy, image2Copy,) = transformeImageIntoMatrix(I, J)

    if(sameDim == True) :
        image1Copy = image1.flatten()
        image2Copy = image2.flatten()
        ssd = (np.sum(image1Copy) - np.sum(image2Copy))**2
        print("SSD = ", ssd)
        return ssd

def CR(I, J) :
    (sameDim, image1Copy, image2Copy,) = transformeImageIntoMatrix(I, J)

    if(sameDim == True) :
        moyI1 = np.average(image1Copy)
        moyI2 = np.average(image2Copy)
        diffAlaMoyI1 = np.subtract(image1Copy, moyI1)
        diffAlaMoyI2 = np.subtract(image2Copy, moyI2)
        numerateur = np.sum(diffAlaMoyI1*diffAlaMoyI2)
        varianceI1 = math.sqrt(np.sum(np.power(diffAlaMoyI1, 2)))
        varianceI2 = math.sqrt(np.sum(np.power(diffAlaMoyI2, 2)))
        denominateur = varianceI1*varianceI2
        cr = numerateur/denominateur
        print("Coefficient de corelation : ", cr)
        return cr

def IM(I, J) :
    (sameDim, image1Copy, image2Copy,) = transformeImageIntoMatrix(I, J)

    if(sameDim == True) :
        (x, y, h) = JoinHist(I, J, 100)


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

    if args.question == "1":
        #I2/J2 ok, BrainMRI_1/BrainMRI_2/BrainMRI_3/BrainMRI_4 ok, I3/J3 ok, I4/J4 ok, I5/J5 ok, I6/J6 ok
        #I1/J1 pas de la même taille (512, 512, 4) et (512, 512)
        JoinHist("Data/I2.jpg", "Data/J2.jpg", 100)
        plt.show()

    if args.question == "2a" :
        SSD("Data/I2.jpg", "Data/J2.jpg")

    if args.question == "2b" :
        CR("Data/I2.jpg", "Data/J2.jpg")

    if args.question == "2c" :
        IM("Data/I2.jpg", "Data/J2.jpg")

    if args.question == "3a":
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

    if args.question == "3b":
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

    if args.question == "3c":
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

    if args.question == "3d":
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
        I = plt.imread(images[1])
        plt.imshow(I)
        plt.show()
        J = plt.imread(images[0])
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
        J = plt.imread(images[0])
        plt.imshow(J)
        plt.show()
        newI = RecalageIconique.minSSDrotation(I, J)
        plt.imshow(newI)
        plt.show()

    if args.question == "4e" :
        I = plt.imread(images[3])
        plt.imshow(I)
        plt.show()
        J = plt.imread(images[0])
        plt.imshow(J)
        plt.show()
        newI = RecalageIconique.minSSD(I, J)
        plt.imshow(newI)
        plt.show()


    if args.question == "test" :
        i = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        j = [
            [1,1,1],
            [2,2,2],
            [3,3,3]
        ]
        print(np.multiply(i,j))


if __name__ == "__main__":
    main()
