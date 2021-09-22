import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import matplotlib.widgets as wdg
import Gaussien
import medpy.filter.smoothing as smt
import scipy.signal as sig

#print("Filename : ")
#name = input()


class Image(object):
	def __init__(self, matrix, view, ax, bnext, bprev):
		self.view = view
		self.matrix = matrix
		self.ax = ax
		rows, cols, self.slices = matrix.shape
		self.index = 0
		if(self.view == 'axial') :
			self.img = self.ax.imshow(self.matrix[:, :, self.index], cmap='gray')
			min = np.min(self.matrix[:, :, self.index])
			max = np.max(self.matrix[:, :, self.index])
		elif(self.view == 'coronal') :
			self.img = self.ax.imshow(self.matrix[:, self.index, :], cmap='gray')
			min = np.min(self.matrix[:, self.index, :])
			max = np.max(self.matrix[:, self.index, :])
		elif(self.view == 'sagittal') :
			self.img = self.ax.imshow(self.matrix[self.index, :, :], cmap='gray')
			min = np.min(self.matrix[self.index, :, :])
			max = np.max(self.matrix[self.index, :, :])

		self.ax.set_title(self.view + " slice " + str(self.index) + "\nMin Intensity : " + str(min) + "\nMax Intensity : " + str(max))

		bnext.on_clicked(self.next)
		bprev.on_clicked(self.prev)
		self.update()


	def next(self, event):
		self.index = (self.index + 1) % self.slices
		self.update()

	def prev(self, event):
		self.index = (self.index - 1) % self.slices
		self.update()

	def update(self):
		if(self.view == 'axial') :
			self.img.set_data(self.matrix[:, :, self.index])
			min = np.min(self.matrix[:, :, self.index])
			max = np.max(self.matrix[:, :, self.index])
		elif(self.view == 'coronal') :
			self.img.set_data(self.matrix[:, self.index, :])
			min = np.min(self.matrix[:, self.index, :])
			max = np.max(self.matrix[:, self.index, :])
		elif(self.view == 'sagittal') :
			self.img.set_data(self.matrix[self.index, :, :])
			min = np.min(self.matrix[self.index, :, :])
			max = np.max(self.matrix[self.index, :, :])
		self.ax.set_title(self.view + " slice " + str(self.index) + "\nMin Intensity : " + str(min) + "\nMax Intensity : " + str(max))
		self.img.axes.figure.canvas.draw()

def Viewer(matrix, view, nameOfImage):
	if(view == 'Multi-D viewer'):
		xMax = len(img[0])
		yMax = len(img[0][0])
		if(nameOfImage=="t1.nii") :
			xMax = 40
			yMax = 26
		elif(nameOfImage=="fa.nii") :
			xMax = 28
			yMax = 24
		elif(nameOfImage=="flair.nii") :
			xMax = 52
			yMax = 24
		fig2, axs = plt.subplots(1, 1, sharey=True, tight_layout=True)
		axs.hist(img[0][0:xMax, 0:yMax])
		fig, axes = plt.subplots(1, 3)
		bnext = [wdg.Button(plt.axes([0.25+0.25*i, 0.01, 0.05, 0.04]), '>') for i in range(3)]
		bprev = [wdg.Button(plt.axes([0.2+0.25*i, 0.01, 0.05, 0.04]), '<') for i in range(3)]
		Image(matrix, 'sagittal', axes[0], bnext[0], bprev[0])
		Image(matrix, 'coronal', axes[1], bnext[1], bprev[1])
		Image(matrix, 'axial', axes[2], bnext[2], bprev[2])
	else :
		fig, ax = plt.subplots(1, 1)
		bnext = wdg.Button(plt.axes([0.75, 0.01, 0.05, 0.04]), '>')
		bprev = wdg.Button(plt.axes([0.7, 0.01, 0.05, 0.04]), '<')
		#Sens de l'image a determiner
		if(view == 'sagittal'):
			Image(matrix, 'sagittal', ax, bnext, bprev)
		elif(view == 'coronal'):
			Image(matrix, 'coronal', ax, bnext, bprev)
		elif(view == 'axial'):
			Image(matrix, 'axial', ax, bnext, bprev)
	plt.show()

def analyseImage(data, img) :
	print(data, "\n")
	print("Voxel dimension (in mm) : ", data.header.get_zooms(),)

	fig = plt.figure()
	dim = fig.get_size_inches()*fig.dpi
	print("Image dimension (in px) : ", dim)

	min = np.min(img[np.nonzero(img)])
	max = np.max(img)
	print("Cmichelson = ", (max-min)/(max+min))

	'''RMS constrast : sqrt[ 1/MN * for(i=0; i<=N-1; i++) for(j=0; j<=M-1; j++) (Lij - moyenne(L))^2 ] where Lij is the brightness of pixel ij'''
	imgMoy = img/max
	Lbarre = imgMoy.mean()
	diff = np.power(imgMoy - Lbarre, 2)
	diff = np.sum(diff)
	RMS = np.sqrt(diff/((dim[0]*dim[1])-1))
	print("RMS contrast = ", RMS)

nameOfImage = "t1.nii"
data = nib.load(nameOfImage)
img = data.get_fdata()

#img = Gaussien.gaussien(img)
#img = sig.medfilt(img)
#img = smt.anisotropic_diffusion(img, 10, 20, 0.1, None, 3)
Viewer(img, 'Multi-D viewer', nameOfImage)
analyseImage(data, img)
