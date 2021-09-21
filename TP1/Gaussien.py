import numpy as np

def gaussien(img) :
    gausse = np.array([
        [1, 2, 1],
        [2, 4, 2],
        [1, 2, 1]
    ])
    row, col, slice = img.shape
    print(img.shape)

    img_d = np.zeros((row-2, col-2, slice-2))
    print(img_d.shape)
    #img_d = np.zeros(img.shape)

    for x in range(1, row-1) :
        tmp = img[x, :, :][1:-1, 1:-1] * 4
        for y in range(0,3) :
            for z in range(0,3) :
                if (y,z) != (1,1) :
                    tmp = tmp + img[x,:,:][y:col-2+y,z:slice-2+z] * gausse[y,z]
        tmp = tmp * 1 / 16
        img_d[x-1, :, :] = tmp

    for x in range(1, col-1):
        tmp = img[1:-1,x, 1:-1] * 4
        for y in range(0, 3):
            for z in range(0, 3):
                if (y, z) != (1, 1):
                    tmp = tmp + img[y:row - 2 + y, x, z:slice - 2 + z] * gausse[y,z]
        tmp = tmp * 1 / 16
        img_d[:,x-1,:] = tmp

    for x in range(1, slice-1):
        tmp = img[1:-1, 1:-1, x] * 4
        for y in range(0, 3):
            for z in range(0, 3):
                if (y, z) != (1, 1):
                    tmp = tmp + img[y:row - 2 + y, z:col - 2 + z, x] * gausse[y,z]
        tmp = tmp * 1 / 16
        img_d[:,:, x-1] = tmp

    print(img_d.shape)

    return img_d
