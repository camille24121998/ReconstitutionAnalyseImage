import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import matplotlib.widgets as wdg
import Isotrope
import Median

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
		elif(self.view == 'coronal') :
			self.img = self.ax.imshow(self.matrix[:, self.index, :], cmap='gray')
		elif(self.view == 'sagittal') :
			self.img = self.ax.imshow(self.matrix[self.index, :, :], cmap='gray')

		self.ax.set_title(self.view + " slice " + str(self.index))

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
		elif(self.view == 'coronal') :
			self.img.set_data(self.matrix[:, self.index, :])
		elif(self.view == 'sagittal') :
			self.img.set_data(self.matrix[self.index, :, :])
		self.ax.set_title(self.view + " slice " + str(self.index))
		self.img.axes.figure.canvas.draw()

def Viewer(matrix, view):
	if(view == 'Multi-D viewer'):
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

data = nib.load("fa.nii")
img = data.get_fdata()
print(data, "\n")
print("Voxel dimension (in mm) : ", data.header.get_zooms(),)
'''print(data.header.get_data_shape())
print(data.header.get_qform())
print(data.header.get_sform())
print(data.header.get_slope_inter())
print(data.header.get_dim_info())
print(data.header.get_xyzt_units())'''

plt.ioff()
fig = plt.figure()
print("Image dimension (in px) : ", fig.get_size_inches()*fig.dpi)
plt.close(fig)

print(img)

img_d = Isotrope.isotrope(img)

Viewer(img, 'Multi-D viewer')

plt.show()

