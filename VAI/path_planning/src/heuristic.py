#!/usr/bin/env python

import numpy as np

# calculate euclidian distance 
class Heuristic(object):
    @classmethod
    def euclidan_dist(self, arr1, arr2):
        arr1 = np.array(arr1)
        arr2 = np.array(arr2)
        return np.linalg.norm(arr1 - arr2)
