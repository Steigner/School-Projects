import numpy as np
import time
from params import Params

class HC12(Params):
    #getter a setter - method for entering and obtaining rank
    @property
    def dod_param(self):
        return self._dod_param

    @dod_param.setter
    def dod_param(self, dod_param):
        if len(dod_param) == self.n_param:
            self._dod_param = np.array(dod_param)
        else:
            self._dod_param = np.array([dod_param for _ in range(self.n_param)])
    
    def __init__(self):
        super(HC12,self).__init__()

        self.n_param = self.nParam
        self.n_bit_param = np.array([self.nBitParam for _ in range(self.nParam)], dtype = np.uint16)
        self.dod_param = self.dodParam
        self.uint_type = np.uint16
        self.float_type = np.float64
        self.total_bits = int(np.sum(self.n_bit_param))

        # rows of matrix M0
        self.__M0_rows = 1
        # rows of matrix M0
        self.__M1_rows = self.total_bits
        # rows of matrix M0
        self.__M2_rows = self.total_bits*(self.total_bits-1)//2
        # total number of rows
        self.rows = self.__M0_rows + self.__M1_rows + self.__M2_rows
        # matrix K - kernel
        self.K = np.zeros((1,self.n_param), dtype = self.uint_type)
        # matrix M - matrix of numbers for masks
        self.M = np.zeros((self.rows,self.n_param), dtype = self.uint_type) 
        # matrix B - binary
        self.B = np.zeros((self.rows,self.n_param), dtype = self.uint_type)
        # matrix I - integer
        self.I = np.zeros((self.rows,self.n_param), dtype = self.uint_type)
        # matrix R - real value
        self.R = np.zeros((self.rows,self.n_param), dtype = self.float_type)
        # matrix F - functional value
        self.F = np.zeros((self.rows,self.n_param), dtype = self.float_type) 
        self.__init_M() 

    def __init_M(self):
        #matrix M
        bit_lookup = []
        for p in range(self.n_param):
            for b in range(self.n_bit_param[p]):
                bit_lookup.append((p,b))

        for j in range(1, 1+self.__M1_rows):
            # bit shift
            p, bit = bit_lookup[j-1] 
            self.M[j,p] |= 1 << bit

        j = self.__M0_rows+ self.__M1_rows

        for bit in range(self.total_bits-1):
            # bit shift
            for bit2 in range (bit+1, self.total_bits):
                self.M[j,bit_lookup[bit][0]] |= 1 << bit_lookup[bit][1]
                self.M[j,bit_lookup[bit2][0]] |= 1 << bit_lookup[bit2][1]
                j += 1

    def hc12(self):    
        func = self.func
        times = self.nRuns 
        max_iter = self.maxGener

        dod = self.dod_param
        n_bit = self.n_bit_param

        x_out = np.zeros((times,self.n_param),dtype = self.float_type)
        fval = np.full(times, float('inf'))

        def interval_to_float(int_i, a, b, n_bits):
            return(b-a)/(2**n_bits-1)*int_i + a
        
        iterations = np.zeros((times, 1))
        winning_run = 0
        t = []

        for run_i in range(times):
            start = time.time()
            # prepare K
            self.K[:] = [np.random.randint(0, 2**n_bit[i]) for i in range(self.n_param)]
            run_fval = float('inf')

            for iter_i in range(max_iter):
                # K xor M -> result B
                np.bitwise_xor(self.K, self.M, out = self.B)
                # Decode Graye B to I -> result I
                np.bitwise_and(self.B, 1 << n_bit, out=self.I)
                for par in range(self.n_param):
                    for bit in range(n_bit[par], 0, -1):
                        self.I[:, par] |= np.bitwise_xor((self.I[:, par] & 1 << bit) >>1, self.B[:,par]&1<<(bit-1))
                    # Convert I to real numbers -> result R
                    self.R[:,par] = interval_to_float(self.I[:,par], dod[par,0], dod[par,1], n_bit[par])

                # Calculating the chase of the objective function -> result F
                self.F = [self.func(c) for c in self.R]
                
                # select the best one and then either terminate it or declare it a new K
                best_idx = np.argmin(self.F)
                
                run_fval = self.F[best_idx]
                
                # 1. basic quiting
                if best_idx == 0:
                    break
                
                # 2. fitness quiting
                # if run_fval < self.fitness:
                #    break

                self.K = self.B[best_idx, :]

            iterations[run_i] = iter_i
            x_out[run_i,:] = self.R[best_idx,:]

            if run_fval < min(fval):
                winning_run = run_i

            fval[run_i] = run_fval
            t.append(time.time() - start)

            print(f'[INFO] x = {x_out[run_i]}, fx = {fval[run_i]}')

        return x_out, fval, t