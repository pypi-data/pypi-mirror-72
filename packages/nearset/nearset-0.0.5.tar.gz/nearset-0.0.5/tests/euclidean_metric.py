from nearset import Nearset
from nearset.metrics import euclidean_distance, cosine_distance
from sklearn.datasets import make_blobs
from tqdm import tqdm
import time
import numpy as np

# create dataset
N = 100000
X, y = make_blobs(N, n_features=10, centers=50)

# the vector queried: ie. find the nearest neighbors of this point
query = X[0]

# order data by comparing its distance to the query
ns = Nearset(euclidean_distance(query), max_size=10)

# add all points to the set by using standard __setitem__ method
for i in tqdm(range(X.shape[0])):
    ns["node_" + str(i)] = X[i]
print(len(ns))

# verify that points in the set are ordered by distance
# last_distance = -1
# for idx, value, distance in ns:
#     assert distance >= last_distance
#     last_distance = distance
#     print(idx, distance)
