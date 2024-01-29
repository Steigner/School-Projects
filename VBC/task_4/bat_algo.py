import numpy as np
import time
from params import Params

class Bat_Algorithm(Params):
    def __init__(self):
        super(Bat_Algorithm, self).__init__()
        
        # minimum fitness
        self.best_eval = None 

        #lower bound
        self.Lb = np.zeros(self.dim) 
        
        # upper bound
        self.Ub = np.zeros(self.dim)   
        
        # frequency
        self.f = np.zeros(self.NP) 
        
        # fitness
        self.Fitness = np.zeros(self.NP) 
        
        # best solution
        self.best = np.zeros(self.dim) 

        # velocity
        self.v = [[0 for i in range(self.dim)] for j in range(self.NP)]
        
        # population of solutions
        self.Sol = [[0 for i in range(self.dim)] for j in range(self.NP)]

    def __init_bat(self):
        l = 0

        # find the best fitness value and record the index on the variable j
        for i in range(self.dim):
            self.Lb[i] = self.dodParam[0]
            self.Ub[i] = self.dodParam[1]

        # store the values ​​of each dimension on the best solution
        for i in range(self.NP):
            self.f[i] = 0
            
            for j in range(self.dim):
                rnd = np.random.uniform(0, 1)
                self.v[i][j] = 0.0
                self.Sol[i][j] = self.Lb[j] + (self.Ub[j] - self.Lb[j]) * rnd
            
            self.Fitness[i] = self.func(self.Sol[i])

        for k in range(self.NP):
            if self.Fitness[k] < self.Fitness[l]:
                l = k
        
        for m in range(self.dim):
            self.best[m] = self.Sol[l][m]
        
        # save the fitness value of the best solution
        self.best_eval = self.Fitness[l]

    def __bounds(self, s, lower, upper):
        # if the value exceeds the upper limit then set the value to be the upper limit
        if s > upper:
            s = upper
        
        # if the value is less than the lower limit then set the value to be the lower limit
        elif s < lower:
            s = lower
        
        else:
            pass

        return s

    def __rand_sam(self):
        return np.random.random_sample()

    def bat_algo(self):
        times = self.nRuns 
        x_out = np.zeros((times,self.dim))
        fval = np.full(times, float('inf'))
        t = []
        
        for run_i in range(times):
            start = time.time()
            
            # solution matrix (number of bats x dimension)
            S = [[0.0 for i in range(self.dim)] for j in range(self.NP)]

            self.__init_bat()

            for k in range(self.maxGener):
                for i in range(self.NP):
                    rnd = np.random.uniform(0, 1)
                    # find the frequency of each bat using eq. 2 of the bat algorithm
                    self.f[i] = self.pF[0] + (self.pF[1] - self.pF[0]) * rnd
                    
                    # find the new v and x of each bat using eq. 3 and 4 of the bat algorithm
                    for j in range(self.dim):
                        self.v[i][j] = self.v[i][j] + (self.Sol[i][j] - self.best[j]) * self.f[i]
                        S[i][j] = self.Sol[i][j] + self.v[i][j]
                        S[i][j] = self.__bounds(S[i][j], self.Lb[j], self.Ub[j])
                    
                    rnd = self.__rand_sam()

                    # if the random value [0,1] is greater than the pulse rate of the bat, then do a local search based on the best bat
                    if rnd > self.pR:
                        for j in range(self.dim):
                            S[i][j] = self.best[j] + 0.001 * np.random.normal(-1, 1)
                            S[i][j] = self.__bounds(S[i][j], self.Lb[j], self.Ub[j])

                    # calculate the fitness value of the new solution    
                    Fnew = self.func(S[i])
                    
                    rnd =self.__rand_sam()

                    if (Fnew <= self.Fitness[i]) and (rnd < self.pA):
                        # change the best solution
                        for j in range(self.dim):
                            self.Sol[i][j] = S[i][j]
                        self.Fitness[i] = Fnew

                    if Fnew <= self.best_eval:
                        for j in range(self.dim):
                            self.best[j] = S[i][j]
                        self.best_eval = Fnew
                    
                # print(self.best)

            x_out[run_i,:] = self.best
            fval[run_i] = self.best_eval
            
            t.append(time.time() - start)

            print(f'[INFO] x = {x_out[run_i]}, fx = {fval[run_i]}')
        
        return x_out, fval, t