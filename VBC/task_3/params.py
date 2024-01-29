import numpy as np
from obj_func import Obj_Func

class Params(object):
    def __init__(self):
        # number of parameters
        self.nParam = 2

        # bound params
        dod = np.array([-5.12, 5.12])
        self.dodParam = np.tile(dod,(self.nParam,1))
        
        # runs
        self.nRuns = 1000
        
        # generations
        self.maxGener = 20

        # number of bits per parameter
        self.nBitParam = 15

        # GA
        # population size
        self.NP = 100

        # probability of crossing
        self.pC = 0.75
        
        # probability of mutation 
        self.pM = 1.0 / self.nBitParam

        # the power of selection
        self.pS = 4

        # obhectuve function
        self.func = Obj_Func().rastrigin

        # fitness
        self.fitness = 1e-4