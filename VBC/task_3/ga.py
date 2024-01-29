import numpy as np
import time
from params import Params

class GA(Params):
    def __init__(self):
        super(GA, self).__init__()

    # decode bitstring to numbers
    def decode(self, bounds, n_bits, bitstring):
        decoded = []
        largest = 2**n_bits
        for i in range(len(bounds)):
            # extract the substring
            start, end = i * n_bits, (i * n_bits)+n_bits
            substring = bitstring[start:end]
            # convert bitstring to a string of chars
            chars = ''.join([str(s) for s in substring])
            # convert string to integer
            integer = int(chars, 2)
            # scale integer to desired range
            value = bounds[i][0] + (integer/largest) * (bounds[i][1] - bounds[i][0])
            # store
            decoded.append(value)
        return decoded
        
    # selection 
    def selection(self, pop, scores):
        k = int(self.pS * len(pop))
        # first random selection
        selection_ix = np.random.randint(len(pop))
        for ix in np.random.randint(0, len(pop), k - 1):
            # check if better
            if scores[ix] < scores[selection_ix]:
                selection_ix = ix
        
        return pop[selection_ix]

    # crossover
    def crossover(self, p1, p2, r_cross):
        # children are copies of parents (default)
        c1, c2 = p1.copy(), p2.copy()
        
        # check for recombination
        if np.random.rand() < r_cross:
            # select crossover point
            pt = np.random.randint(1, len(p1) - 2)
            
            # perform crossover
            c1 = p1[:pt] + p2[pt:]
            c1 = p2[:pt] + p1[pt:]
        
        return [c1,c2]

    # mutation
    def mutation(self, bitstring, r_mut):
        for i in range(len(bitstring)):
            # check for mutation
            if np.random.rand() < r_mut:
                # flip the bit
                bitstring[i] = 1 - bitstring[i]

    # genetic algorithm
    def ga(self):
        objective = self.func
        n_bits = self.nBitParam
        n_iter = self.maxGener
        n_pop = self.NP
        r_cross = self.pC
        r_mut = self.pM
        bounds = self.dodParam
        times = self.nRuns 

        x_out = np.zeros((times,self.nParam))
        fval = np.full(times, float('inf'))
        t = []

        for run_i in range(times):
            start = time.time()

            # init population
            pop = [np.random.randint(0, 2, n_bits*len(bounds)).tolist() for _ in range(n_pop)]

            # keep track of best solution
            # best, best_eval = 0, objective(pop[0])
            best, best_eval = 0, objective(self.decode(bounds, n_bits, pop[0]))

            for gen in range(n_iter):
                # evaluate all candidates in population
                decoded = [self.decode(bounds, n_bits, p) for p in pop]

                scores = [objective(c) for c in decoded]

                for i in range(n_pop):
                    if scores[i] < best_eval:
                        best, best_eval = pop[i], scores[i]

                # selection
                selected = [self.selection(pop, scores) for _ in range(n_pop)]
                
                # new generation
                children = []
                
                for i in range(0, n_pop, 2):
                    # get selected parents in pairs
                    p1, p2 = selected[i], selected[i+1]

                    # crossover and mutation
                    for c in self.crossover(p1, p2, r_cross):
                        self.mutation(c, r_mut)
                        children.append(c)

                pop = children

                # fitness 
                # if best_eval < self.fitness:
                #    break

            x_out[run_i,:] = self.decode(bounds, n_bits, best)
            fval[run_i] = best_eval

            t.append(time.time() - start)

            print(f'[INFO] x = {x_out[run_i]}, fx = {fval[run_i]}')
        
        return x_out, fval, t