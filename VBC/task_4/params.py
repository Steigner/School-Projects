import numpy as np
from obj_func import Obj_Func

class Params(object):
    def __init__(self):
        # dimensions
        self.dim = 2

        # bound params
        self.dodParam = [-5.12,5.12]

        # runs
        self.nRuns = 10

        # generations
        self.maxGener = 400

        # population size
        self.NP = 150

        # loudness
        self.pA = 0.8

        # pulse rate
        self.pR = 0.6

        # frequency qmin - qmax
        self.pF = [0, 5]

        # objective function
        self.func = Obj_Func().rastrigin