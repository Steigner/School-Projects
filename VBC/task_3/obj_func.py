import numpy as np
from scipy.optimize import rosen

class Obj_Func(object):
    @staticmethod
    #   input: x = [x] depands on input dimension, for more dimension change dodParam, more dimension ex. x = [x,x,x,x] 
    #   return computed rastrigins f(x) by given points
    def rastrigin(x):
        return 10 * len(x) + sum([(xi**2 - 10 * np.cos(2 * np.pi * xi)) for xi in x])
    
    @staticmethod
    #   input: x = [x] depands on input dimension, for more dimension change dodParam, more dimension ex. x = [x,x,x,x] 
    #   return computed schewefell f(x) by given points
    def schwefel(x):
        return 418.9829 * len(x) - sum([(xi * np.sin( np.sqrt(np.abs(xi)) )) for xi in x])

    @staticmethod
    #   input: x = [x] depands on input dimension, for more dimension change dodParam, more dimension ex. x = [x,x,x,x] 
    #   return computed rosenbrock f(x) by given points
    def rosenbrock(x):     
        return rosen(x)
