import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import matplotlib.widgets as wdg


#print("Filename : ")
#name = input()

class Image(object):
	def __init__(self, filename):
		data = nib.load(filename)
		self.matrix = data.get_fdata()
		rows, cols, self.slices = data.shape
		self.index = 0

		fig, self.ax = plt.subplots(1, 1)
		self.ax.set_title('slice %s' % self.index)
		self.img = self.ax.imshow(self.matrix[:, :, self.index], cmap="gray")

		self.bnext = wdg.Button(plt.axes([0.75, 0.01, 0.05, 0.04]), '>')
		self.bnext.on_clicked(self.next)
		self.bprev = wdg.Button(plt.axes([0.7, 0.01, 0.05, 0.04]), '<')
		self.bprev.on_clicked(self.prev)		

	def next(self, event):
		self.index = (self.index + 1) % self.slices
		self.update()

	def prev(self, event):
		self.index = (self.index - 1) % self.slices
		self.update()

	def update(self):
		self.img.set_data(self.matrix[:, :, self.index])
		self.ax.set_title('slice %s' % self.index)
		self.img.axes.figure.canvas.draw()

def Viewer(filename):
	data = nib.load(filename)
	print(data.header['dim'])

image = Viewer("t1.nii")
plt.show()

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