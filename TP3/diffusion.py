import numpy as np
import nibabel as nib
from dipy.reconst.dti import fractional_anisotropy, color_fa
from dipy.io.image import load_nifti, save_nifti
import dipy.reconst.dti as dti


def estimation_tenseur(img_data, b_vec, b_val) :
	mat = 0
	s0 = img_data[:,:,:,0]

	X = np.array([1/b_val[i] * np.log(img_data[:,:,:,i]/s0) for i in range(1,65)])
	X = np.transpose(X,(1,2,3,0))

	b_x = b_vec[1:,0]
	b_y = b_vec[1:,1]
	b_z = b_vec[1:,2]
	B = np.array([b_x**2, b_x*b_y, b_x*b_z, b_y**2, b_y*b_z, b_z**2]).transpose()
	D = np.matmul(np.linalg.inv(np.matmul(B.T,B)),B.T)

	D = np.einsum('ij,klmj->klmi',D,X)

	return mat

def estimation_fa(D) :
	mat1 = np.zeros((len(D),len(D[0]),len(D[0][0]),3,3))
	for i in range(len(D)) :
		for j in range(len(D[0])) :
			for k in range(len(D[0][0])) :
				D_xx = D[i,j,k,0]
				D_xy = D[i,j,k,1]
				D_xz = D[i,j,k,2]
				D_yy = D[i,j,k,3]
				D_yz = D[i,j,k,4]
				D_zz = D[i,j,k,5]
				D_temp = np.array([[D_xx,D_xy,D_xz],[D_xy,D_yy,D_yz],[D_xz,D_yz,D_zz]])
				mat[i,j,k] = D_temp

	mat = np.zeros((len(D),len(D[0]),len(D[0][0])))
	for i in range(len(D)) :
		for j in range(len(D[0])) :
			for k in range(len(D[0][0])) :
				if(np.inf not in D[i,j,k] and -np.inf not in D[i,j,k] and np.isnan(D[i,j,k]).any() == False) :
					u,s,vh = np.linalg.svd(D[i,j,k])
					mat[i,j,k] = fractional_anisotropy(s)
		print(i/len(D))
	print(mat)
	return mat

def estimation_fa2(D) :


	return 0