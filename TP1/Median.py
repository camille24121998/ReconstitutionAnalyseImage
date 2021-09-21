import numpy as np

def median(img) :

    img_d = img

    for i in range(0,len(img)) :
        # duplique les bordures pour chaque image i
        tmp = np.insert(img[i], 0, img[0, 0], axis=0)
        tmp = np.insert(tmp, -1, tmp[-1], axis=0)
        tmp = np.insert(tmp, 0, tmp[:, 0], axis=1)
        tmp = np.insert(tmp, -1, tmp[:, -1], axis=1)

        for j in range(0,len(img[i])) :

            for k in range(0,len(img[i,j])) :
                # extrait une matrice 3x3 autour du pixel (j,k) de l'image i
                ixgrid = np.ix_([j, j + 1, j + 2], [k, k + 1, k + 2])
                subMatrix = tmp[ixgrid]
                #calcul la medianne de la sous-matrice
                img_d[i,j,k] = np.median(subMatrix)
    return img_d
