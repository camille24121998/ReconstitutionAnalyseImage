import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

def JoinHist(I, J, bin) :
    plot1 = plt.figure(1)
    image1 = (np.matrix(plt.imread(I))).flatten()
    plt.imshow(image1)

    print("Image1 : ", image1)
    print(image1[0][0])

    plot2 = plt.figure(2)
    image2 = (np.matrix(plt.imread(J))).flatten()
    plt.imshow(image2)

    '''plot3 = plt.figure(3)
    plt.hist(image1)'''

    print(np.shape(image1))

    plot4 = plt.figure(4)
    #h, x, y = plt.hist2d(image1[0],image2[0])
    #plt.hexbin(image1,image2, bins=bin)

    #plot5 = plt.figure(5)
    #np.histogram2d(image1[0], image2[0])

    plt.show()

def main():
    JoinHist("Data/I5.jpg", "Data/I6.jpg", 30)

if __name__ == "__main__":
    main()
