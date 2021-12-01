import numpy as np
import nibabel as nib
from dipy.reconst.dti import fractional_anisotropy, color_fa
from dipy.io.stateful_tractogram import Space, StatefulTractogram
from dipy.io.streamline import load_tractogram, save_tck
from dipy.io.image import load_nifti, save_nifti
import dipy.reconst.dti as dti
import random
from math import degrees
from time import time

def estimation_tenseur(img_data, b_vec, b_val) :
	s0 = img_data[:,:,:,0]
	mask = []
	for (i,j,k) in list(np.ndindex(s0.shape)) :
		if(s0[i,j,k] > 700) :
			mask.append([i,j,k])
	mask = np.array(mask)		
	print("Mask shape : ", mask.shape)

	X = np.zeros((len(img_data),len(img_data[0]),len(img_data[0][0]),len(img_data[0][0][0])-1))
	t = time()
	for (i,j,k) in mask :
		X[i,j,k] = [1/b_val[l] * np.log(img_data[i,j,k,l]/s0[i,j,k]) for l in range(1,len(img_data[0][0][0]))]
		if(time()-t>1) :
			print(i,j,k)
			t = time()
	X = np.array(X)

	print("X shape : ",X.shape)

	b_x = b_vec[1:,0]
	b_y = b_vec[1:,1]
	b_z = b_vec[1:,2]
	B = np.array([b_x**2, b_x*b_y, b_x*b_z, b_y**2, b_y*b_z, b_z**2]).transpose()
	D = np.matmul(np.linalg.inv(np.matmul(B.T,B)),B.T)

	D = np.einsum('ij,klmj->klmi',D,X)

	return D, mask

def tensor_2D_to_3D(D,mask) :
	D_mat = np.zeros((len(D),len(D[0]),len(D[0][0]),3,3))
	for (i,j,k) in mask :
		D_xx = D[i,j,k,0]
		D_xy = D[i,j,k,1]
		D_xz = D[i,j,k,2]
		D_yy = D[i,j,k,3]
		D_yz = D[i,j,k,4]
		D_zz = D[i,j,k,5]
		D_mat[i,j,k] = np.array([[D_xx,D_xy,D_xz],[D_xy,D_yy,D_yz],[D_xz,D_yz,D_zz]])
	return D_mat

def estimation_fa(D,mask) :
	fa = np.zeros((len(D),len(D[0]),len(D[0][0])))
	eigenvectors = np.zeros((len(D),len(D[0]),len(D[0][0]),3,3))
	eigenvalues = np.zeros((len(D),len(D[0]),len(D[0][0]),3))

	print("Estimation FA")
	t = time()
	for (i,j,k) in mask :
		if(np.inf not in D[i,j,k] and -np.inf not in D[i,j,k] and np.isnan(D[i,j,k]).any() == False) :
			eigenvectors[i,j,k],eigenvalues[i,j,k],vh = np.linalg.svd(D[i,j,k])
			fa[i,j,k] = np.float32(fractional_anisotropy(eigenvalues[i,j,k]))
		if(time()-t>1) :
			print(i,j,k)
			t = time()
		#print('{:2.2%}'.format(i/len(D)))
	return fa, eigenvectors, eigenvalues

def tractographie(fa,eigenvectors,eigenvalues,img) :
	tracto = []

	print("Create mask")
	mask = []
	for (i,j,k) in list(np.ndindex(fa.shape)) :
		if(fa[i,j,k] > 0.1) :
			mask.append([i,j,k])
	mask = np.array(mask)

	print("Create streamline")
	t = time()
	for n in range(100000) :
		ite = 0
		rand = random.randrange(len(mask))
		(i,j,k) = mask[rand]
		streamline = [[np.float64(i),np.float64(j),np.float64(k)]]
		v1 = eigenvectors[i,j,k][0]
		while(fa[i,j,k] > 0.15 and ite <100) :
			ite = ite + 1
			(i,j,k) = (i,j,k) + eigenvectors[i,j,k][0] * 2
			i = round(i)
			j = round(j)
			k = round(k)

			if(i >= len(fa)) :
				i = len(fa) - 1
			elif(i < 0) :
				i = 0

			if(j >= len(fa[0])) :
				j = len(fa[0]) - 1
			elif(j < 0) :
				j = 0

			if(k >= len(fa[0,0])) :
				k = len(fa[0,0]) - 1
			elif(k < 0) :
				k = 0

			streamline.append([np.float64(i),np.float64(j),np.float64(k)])

			v2 = eigenvectors[i,j,k][0]
			if(degrees(angle_between(v1,v2)) > 45) :
				break
			else :
				v1 = v2

		tracto.append(streamline)

		if(time()-t>1) :
			print('{:2.2%}'.format(n/100000))
			t = time()
	stf = StatefulTractogram(tracto,img,Space.RASMM)
	print(stf)
	print(stf.is_bbox_in_vox_valid())
	stf.remove_invalid_streamlines()
	save_tck(stf,"tractographie.tck")


def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))