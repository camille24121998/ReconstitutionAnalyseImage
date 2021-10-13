import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

def JoinHist(I, J, bin) :
    print("test")
    image1 = plt.imread(I)
    plt.imshow(image1)
    plt.show()

def main():
    JoinHist("Data/I5.jpg", "I6.jpg", 30)

if __name__ == "__main__":
    main()
