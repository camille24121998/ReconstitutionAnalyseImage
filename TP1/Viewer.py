import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import matplotlib.widgets as wdg
import Isotrope

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


data = nib.load("t1.nii")
img = data.get_fdata()
print(data)

img_d = Isotrope.isotrope(img)

Viewer(img_d, 'Multi-D viewer')

"""
class Image(object):
	def __init__(self, filename):
		self.data = nib.load(filename)
		self.matrix = self.data.get_fdata()
		rows, cols, self.slices = self.data.shape
		fig, self.ax = plt.subplots(1, 1)
		self.img = self.ax.imshow(self.matrix[:, :, self.slices//2], cmap="gray")

image = Image("t1.nii")
plt.show()
"""

"""
class IndexTracker(object):
    def __init__(self, ax, X):
        self.ax = ax
        ax.set_title('use scroll wheel to navigate images')

        self.X = X
        rows, cols, self.slices = X.shape
        self.ind = self.slices // 2

        self.im = ax.imshow(self.X[:, :, self.ind], cmap="gray")
        self.update()

    def onscroll(self, event):
        print("%s %s" % (event.button, event.step))
        if event.button == 'up':
            self.ind = (self.ind + 1) % self.slices
        else:
            self.ind = (self.ind - 1) % self.slices
        self.update()

    def update(self):
        self.im.set_data(self.X[:, :, self.ind])
        self.ax.set_ylabel('slice %s' % self.ind)
        self.im.axes.figure.canvas.draw()


def plot3d(image):
    fig, ax = plt.subplots(1, 1)
    tracker = IndexTracker(ax, image)
    fig.canvas.mpl_connect('scroll_event', tracker.onscroll)
    plt.show()


if __name__ == "__main__":
	img = open_nii("/home/pvong/Documents/imn530/Fiji.app/Data/Data_MiseEnForme/IRM/Brain/t1.nii")
	data = img.get_fdata()
	#print(data)
	plot3d(data)
"""