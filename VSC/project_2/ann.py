#                   ---Integral script---

# little elimination billions info outputs from tensorflou library
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# import Keras liberary dependencies from tensorflow framework
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LayerNormalization

# possibility to use CuPy if u have Nvidia graphics card, this should approach faster generated points
import numpy as np

# import class Graph from graph.py for plotting graphs
from graph import Graph

class ANN(object):
    # init method:
    # in this method is set up:
    #       R = number of iteration
    #       N = number of generated training points
    #       __lim_rast = defined limits of rastrigin function via. [0] - originally [-5.12, 5.12]
    #       __lim_schwe = defined limits of schewefell function via [1] - originally [-500, 500]
    #       __net_rast = compile architecture ann for rastrigin function
    #       __net_schwe = complie architecture ann for schewefell function
    #       switch = simple switch for switching between defined functions for computing etc. 

    def __init__(self):
        self.R           = 5
        self.N           = 10000
        self.graph       = Graph()
        self.switch      = 0

        self.__lim_rast    = [-5.12, 5.12]
        self.__lim_schwe   = [-500, 500]
        self.__net_rast = self.__architecture_rast()
        self.__net_schwe = self.__architecture_schwe()
    
    # private method:
    #   input:
    #   return
    # Note: reset function for remove all traces from graph
    def __reset(self):
        self.graph.fig.data = []
    
    # private method:
    #   input: x = [x,x] -> 2d, according assigment, but can be add i more dimensional input ex. x = [x,x,x] 
    #   return computed rastrigin f(x) by given points
    def __rastrigin(self, x):
        return 10 * len(x) + sum([(xi**2 - 10 * np.cos(2 * np.pi * xi)) for xi in x])
    
    # private method:
    #   input: x = [x,x] -> 2d, according assigment, but can be add i more dimensional input ex. x = [x,x,x] 
    #   return computed schewefell f(x) by given points
    def __schwefel(self, x):
        return 418.9829 * len(x) - sum([(xi * np.sin( np.sqrt(np.abs(xi)) )) for xi in x])
    
    # private method:
    #   input:
    #   return reshaped generated x[x1,x2], fx[z]
    # Note: In this method we generate x1,x2 in defined limites, then is computed f(x) = z, in __rastrigin method
    def __generate_rastrigin(self):
        x1 = np.random.uniform(self.__lim_rast[0], self.__lim_rast[1], self.N)
        x2 = np.random.uniform(self.__lim_rast[0], self.__lim_rast[1], self.N)
        z = self.__rastrigin([x1, x2])

        return np.vstack((x1, x2)).T, np.reshape(z, (self.N, 1))
    
    # private method:
    #   input:
    #   return reshaped generated x[x1,x2], fx[z]
    # Note: In this method we generate x1,x2 in defined limites, then is computed f(x) = z, in __schewefell method
    def __generate_schwefel(self):
        x1 = np.random.uniform(self.__lim_schwe[0], self.__lim_schwe[1], self.N)
        x2 = np.random.uniform(self.__lim_schwe[0], self.__lim_schwe[1], self.N) 
        z = self.__schwefel([x1,x2])

        return np.vstack((x1, x2)).T, np.reshape(z, (self.N, 1))

    # private method:
    #   input: N = number of points, switch == 0 -> rastrigin lim, switch == 1 -> schewefell lim
    #   return N, generated linspaced x1, x2, then zeroes matrix (NxN)
    def __comp(self, N, switch):
        if switch == 0:
            bound = self.__lim_rast

        elif self.switch == 1:
            bound = self.__lim_schwe

        else:
            raise ValueError("U put wrong int number!")

        l = np.linspace(bound[0], bound[1], N)        
        x1, x2 = np.meshgrid(l, l)
        z = np.zeros((N, N))

        return N, x1, x2, z

    # private method:
    #   input:
    #   return compiled ann architecture of rastrigin function
    def __architecture_rast(self):
        net = Sequential()
        net.add(Dense(200, input_dim=2, activation ='relu'))
        net.add(Dense(125, activation ='relu'))
        net.add(Dense(64, activation ='relu'))
        net.add(Dense(9, activation ='relu'))
        net.add(Dense(6, activation ='relu'))
        net.add(Dense(1, activation ='linear'))
        
        net.compile(loss='mse', optimizer='Nadam', metrics=['mae'])
        
        return net
    
    # private method:
    #   input:
    #   return compiled ann architecture of schewefell function
    def __architecture_schwe(self):
        net = Sequential()
        net.add(Dense(500, input_dim=2, activation ='relu'))
        net.add(Dense(150, activation ='relu'))
        net.add(Dense(64, activation ='relu'))
        net.add(Dense(18, activation ='relu'))
        net.add(Dense(1, activation ='linear'))
        
        net.compile(loss='mse', optimizer='Nadam', metrics=['mae'])
        
        return net
    
    # private method:
    #   input: defined limites, number of steps, function
    #   return searched minimum points
    # Note: This method compute min. extreme by Random Search algo.
    def __optimize(self, lim, steps, f):
        D = len(lim)
        best_f = 9999.0 
        best_p = [None] * D

        for i in range(steps):
            new_p = [lim[d][0] + np.random.random() * (lim[d][1] - lim[d][0]) for d in range(D)]
            new_f = f(new_p)
            
            if new_f < best_f:
                best_f = new_f
                best_p = new_p

        return best_p
    
    # public method:
    #   input:
    #   return
    # Note: In this method is by switch value init dependenciesm, then
    # start training in for lopp in range defined R(iterations), then
    # is finded min. extreme by Random Search algo and concancenated to training datas, then
    # is add traces for finded min. points, and as last is add traces for approximated model
    def net(self):
        # rastrigin
        if self.switch == 0:
            net = self.__net_rast
            x, z = self.__generate_rastrigin()
            lims = [self.__lim_rast, self.__lim_rast]
        
        # schewefell
        elif self.switch == 1:
            net = self.__net_schwe
            x, z = self.__generate_schwefel()
            lims = [self.__lim_schwe, self.__lim_schwe]
        
        else:
            raise ValueError("U put wrong int number!")

        for i in range(self.R):
            print("[INFO] start training iteration no. " + str(i))
            hist = net.fit(x, z, validation_split = 0.2, epochs = 500, batch_size = 64, verbose=0)
            
            print("[INFO] validation loss: " + str(round(hist.history['val_loss'][-1],2)))

            # this function is used for find min. extrem on approximated function
            def approx(x):
                return net.predict(np.array([[x[0],x[1]]]))
            
            # call Random Search algo with defined parametress
            sol = self.__optimize(lims, 5000, approx)

            z_ = np.array([[net.predict( [[sol[0], sol[1]]] )]])
            x_ = np.array([[sol[0],sol[1]]])
            
            # Print to terminal
            print(
                str("[INFO] ") + \
                str("iter. no. " + str(i) + " [x*opt] ") + \
                str([round(sol[0],2), round(sol[1],2)]) + \
                str(" [f*opt] ") + \
                str([round(z_[0][0][0].astype(float).tolist()[0],2)])
            )
            
            # show finded minimum point
            self.graph.add_minim(x_[:,0], x_[:,1], z_[0][0][0], lab = "min. in iteration: " + str(i))

            # add min extreme to training datas
            x = np.concatenate((x,x_))
            z = np.concatenate((z,z_[0][0]))

        # shouw approximated model
        N, x1, x2, z = self.__comp(N=50, switch=self.switch)

        for i in range(N):
            for j in range(N):
                z[i,j] = net.predict(np.array([[x1[i, j], x2[i, j]]]))
        
        self.graph.plot_function(x1, x2, z, func="approximated function")
    
    # public method:
    #   input:
    #   return
    # Note: This method is used for show original rastrigin function
    def show_rastrigin(self):
        self.__reset()
        N, x1, x2, z = self.__comp(N=500, switch=0)
        
        for i in range(N):
            for j in range(N):
                z[i,j] = self.__rastrigin([x1[i, j], x2[i, j]])
        
        self.graph.plot_function(x1, x2, z, func="rastrigin")

    # public method:
    #   input:
    #   return
    # Note: This method is used for show original schewefell function
    def show_schwefel(self):
        self.__reset()
        N, x1, x2, z = self.__comp(N=500, switch=1)

        for i in range(N):
            for j in range(N):
                z[i,j] = self.__schwefel([x1[i, j], x2[i, j]])
        
        self.graph.plot_function(x1, x2, z, func="schwefel")
