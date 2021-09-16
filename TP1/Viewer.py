import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

def open_nii(filename) :
	return nib.load(filename)

img = open_nii("/home/pvong/Documents/imn530/Fiji.app/Data/Data_MiseEnForme/IRM/Brain/t1.nii")
data = img.get_fdata()

plt.imshow(data[160])
plt.show()
