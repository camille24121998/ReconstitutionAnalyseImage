import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

import diffusion
import projection

############
#   Main   #
############
def main():

    ############
    # Partie 1 #
    ############
    """
    data = nib.load("Data/Tproject.nii")
    img = data.get_fdata()
    mat1,mat2,mat3 = projection.projection(img)

    plt.imshow(mat3,cmap="Greys")
    plt.show()
    """
    ############
    # Partie 2 #
    ############
    
    data = nib.load("Data/dmri.nii")
    img = data.get_fdata()

    b_vec, b_val = diffusion.get_b_vec_b_val("Data/gradient_directions_b-values.txt")
    D, mask = diffusion.estimation_tenseur(img,b_vec,b_val)
    D_mat = diffusion.tensor_2D_to_3D(D,mask)
    fa, eigenvectors, eigenvalues = diffusion.estimation_fa(D_mat,mask)
    diffusion.tractographie(fa,eigenvectors,eigenvalues,data,"tractographie.tck")
    
    ############
    # Partie 3 #
    ############

    """
    dataDiff = nib.load("Data/dmri.nii")
    dataFonctionnelle = nib.load("Data/fmri.nii")
    dataT1 = nib.load("Data/t1.nii")

    diff = dataDiff.get_fdata()
    fonct = dataFonctionnelle.get_fdata()
    t1 = dataT1.get_fdata()

    print("Diffusion : ", np.shape(diff))
    print("Fonctionnelle : ", np.shape(fonct))
    print("T1 : ", np.shape(t1))
    """

if __name__ == "__main__":
    main()
