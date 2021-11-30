import numpy as np
import nibabel as nib

import diffusion

############
#   Main   #
############
def main():

    ############
    # Partie 2 #
    ############

    data = nib.load("Data/dmri.nii")
    img = data.get_fdata()

    txt = open("Data/gradient_directions_b-values.txt").read()
    arr = np.array(txt.split())
    arr = arr.reshape(-1,4)
    arr = arr.astype(float)

    b_vec = arr[:,:3]
    b_val = arr[:,3]

    D = diffusion.estimation_tenseur(img,b_vec,b_val)
    FA = diffusion.estimation_fa(D)

    ############
    # Partie 3 #
    ############

    '''dataDiff = nib.load("Data/dmri.nii")
    dataFonctionnelle = nib.load("Data/fmri.nii")
    dataT1 = nib.load("Data/t1.nii")

    diff = dataDiff.get_fdata()
    fonct = dataFonctionnelle.get_fdata()
    t1 = dataT1.get_fdata()

    print("Diffusion : ", np.shape(diff))
    print("Fonctionnelle : ", np.shape(fonct))
    print("T1 : ", np.shape(t1))'''

if __name__ == "__main__":
    main()
