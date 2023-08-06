import numpy as np
cimport numpy as np


cpdef edist(np.ndarray x, np.ndarray y):
    return ((x - y)**2).sum()


cpdef sedist(np.ndarray x, np.ndarray y):
    return (((x - y)**2).sum())**.5


cpdef cdist(np.ndarray x, np.ndarray y):
    xy = (x * y).sum()
    snorm_x = (x**2).sum()
    snorm_y = (y**2).sum()
    if snorm_x > 0 and snorm_y > 0:
        return 1 - xy / (snorm_x * snorm_y)**.5
    return np.nan


def squared_euclidean_distance(np.ndarray x):
    def func(np.ndarray y):
        return sedist(x, y)
    return func


def euclidean_distance(np.ndarray x):
    def func(np.ndarray y):
        return edist(x, y)
    return func


def cosine_distance(np.ndarray x):
    def func(np.ndarray y):
        return cdist(x, y)
    return func
