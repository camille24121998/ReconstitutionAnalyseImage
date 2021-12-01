import numpy as np
import nibabel as nib

def projection(img) :
	h = img.shape[0]
	w = img.shape[1]
	l = img.shape[2]
#	minIMG = np.ones(img.shape) * 255

	mat1 = np.zeros((h,w))
	for i in range(h):
		for j in range(w):
			mat1[i,j] = np.min(img[i,j,:])

	mat2 = np.zeros((h,l))
	for i in range(h):
		for j in range(l):
			mat2[i,j] = np.min(img[i,:,j])

	mat3 = np.zeros((w,l))
	for i in range(w):
		for j in range(l):
			mat3[i,j] = np.min(img[:,i,j])

	return mat1,mat2,mat3
"""

	for i in range(h):
		for j in range(w):
			minIMG[i,j] = min(img[i,j])

	for j in range(w):
		for k in range(l):
			minIMG[j,k] = min(img[j,k])

	for k in range(l):
		for i in range(h):
			minIMG[k,i] = min(img[k,i])
"""