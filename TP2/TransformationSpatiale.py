import numpy as np
import matplotlib.pyplot as plt

####################################################################################################
#genererGrille génère une grille régulière de point 3D de taille x*y*z
#Prends en entrées 3 scalaires correspondants aux dimensions de la grille à générer
#Renvoie 3 listes correspondant aux coordonnées x, y et z, chacunes de taille x*y*z
####################################################################################################
def genererGrille(x,y,z) :
	xs = np.arange(0,x)
	xs = np.tile(xs,y*z)

	ys = np.arange(0,y)
	ys = np.tile(ys,(x,1)).T.flatten()
	ys = np.tile(ys,z)

	zs = np.arange(0,z)
	zs = np.tile(zs, (x*y,1)).T.flatten()


	return xs, ys, zs

#####################################################################################################
#trans_rigide génère la matrice de transformation avec les paramètres theta, omega, phi, p, q et r
#theta : Angle de rotation sur l'axe x
#omega : Angle de rotation sur l'axe y
#phi : Angle de rotation sur l'axe z
#p : distance de translation sur l'axe x
#q : distance de translation sur l'axe y
#r : distance de translation sur l'axe z
#Renvoie la matrice de transformation
#####################################################################################################
def trans_rigide(theta, omega, phi, p, q, r):
	theta = theta * (np.pi/180)
	omega = omega * (np.pi/180)
	phi = phi * (np.pi/180)
	R_theta = np.transpose(np.array([[1, 0, 0, 0],[0,np.cos(theta), np.sin(theta), 0],[0,-np.sin(theta), np.cos(theta), 0],[0, 0, 0, 1]]))
	R_omega = np.transpose(np.array([[np.cos(omega), 0, -np.sin(omega), 0], [0, 1, 0, 0], [np.sin(omega), 0, np.cos(omega), 0], [0, 0, 0, 1]]))
	R_phi = np.transpose(np.array([[np.cos(phi), -np.sin(phi), 0, 0], [np.sin(phi), np.cos(phi), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]))
	
	T = [[1,0,0,p],[0,1,0,q],[0,0,1,r],[0,0,0,1]]

	Transformation_Matrix = np.matmul(T,np.matmul(R_theta,np.matmul(R_omega,R_phi)))

	return Transformation_Matrix

#####################################################################################################
#similitude génère la matrice de transformation avec scaling avec les paramètres s, theta, omega, phi, p, q et r
#s : rapport d'homothétie
#theta : Angle de rotation sur l'axe x
#omega : Angle de rotation sur l'axe y
#phi : Angle de rotation sur l'axe z
#p : distance de translation sur l'axe x
#q : distance de translation sur l'axe y
#r : distance de translation sur l'axe z
#Renvoie la matrice de transformation
#####################################################################################################
def similitude(s, theta,  omega,  phi, p, q, r) :
	scaling_matrix = s * np.identity(4)
	scaling_matrix[3,3] = 1
	return np.matmul(scaling_matrix,trans_rigide(theta,  omega,  phi, p, q, r))