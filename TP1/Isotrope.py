import numpy as np

def isotrope(img) :
    return img[1:][1:][1:] - img[:-1][:-1][:-1]
