#                   ---Integral script---

# little elimination billions info outputs from tensorflou library
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# import Keras liberary from tensorflow framework
from tensorflow import keras

from keras.models import Sequential
from keras.layers import Dense

# import python files Graph for draw graphs and OutputCom for output to terminal
from graph import Graph
from out import OutputCom

# possibility to use CuPy if u have Nvidia graphics card, this should approach faster generated points
import numpy as np 

# for saveing data to csv file
import csv

# library for tensorboard save datasets
import datetime

class ANN(object):
    def __init__(self):
        # info part
        OutputCom.info()
        
        # private values for generating training datase
        self.__x1_range = [-4, 2]
        self.__x2_range = [ 2, 5]
        self.__r = 5000
        self.__net = keras.models.load_model('net_model')
        self.graph = Graph()
        
        # default values
        self.filename = "data.csv"
        self.write = 'a+'

    # private method:
    #   input: x1, x2
    #   return equation form
    # Note: There is place where to change equation form
    def __equation(self, x1, x2):
        return 0.4444444 * (x1 + 2)**2 + 2.3668639 * (x2 - 3)**2 

    # private method:
    #   input:
    #   return Transform form of numpy array with generated points in pre-defined range
    # !!!Please read this Note!!!: There is classified generated points to "inside" / "outside", one of the possibility of 
    # approach to the problem, is not classified, but put input pure range as gradient to ANN. Output activaction 
    # function shouldn't be sigmoid but linear, output will be range, and if will be > 1 "outside", if will be < 1 "inside"!!
    def __gen_numb(self):
        x1 = np.random.uniform(self.__x1_range[0], self.__x1_range[1], self.__r)
        x2 = np.random.uniform(self.__x2_range[0], self.__x2_range[1], self.__r)
        r = self.__equation(x1, x2)

        for i in range(len(r)):
            if r[i] < 1:
                r[i] = 1
            else:
                r[i] = 0  
        
        return np.vstack((x1, x2)).T, r

    # private method:
    #   input: number of points for linspace function
    #   return generated linspace points + transform meshgrid points
    def __lin_points(self, num):
        x1 = np.linspace(self.__x1_range[0], self.__x1_range[1], num)
        x2 = np.linspace(self.__x2_range[0], self.__x2_range[1], num)

        x1_,x2_ = np.meshgrid(x1,x2)

        return x1, x2, x1_, x2_ 

    # private method:
    #   input:
    #   return
    # Note: There is place where to change equation form
    # In this function is generated points of defined function, in this example is it elipse 
    def __equation_bound(self):
        x1, x2, x1_, x2_ = self.__lin_points(100)

        z = 0.4444444 * (x1_ + 2)**2 + 2.3668639 * (x2_ - 3)**2  - 1

        self.graph.set_equation(x1,x2,z)

    # private method:
    #   input: classification, 2-D numpy array 
    #   return
    # Note: This function is used for filter inside, outside points by
    # defined equation. On my opinion, it maybe can be done more elegant, but
    # i don't have not enough time to optimaze it. But it works, so heh. Also
    # in this function is called add trace to graph for outside/inside.
    def __filter(self, k, x):        
        t, n = [], []
        
        for i in range(len(k)):
            if k[i] == 1: 
                t.append([x[i,0],x[i,1]])
            else:
                n.append([x[i,0],x[i,1]])

        t = np.array(t)
        n = np.array(n)

        if not t.size == 0:
            self.graph.gen_points(t, 'inside')
        
        if not n.size == 0:
            self.graph.gen_points(n, 'outside')

    # private method:
    #   input: points, rande, default_percentage_split = 0.8
    #   return split data to x_train, x_test, r_train, r_test
    def __split_data(self, x, r, per_train=0.8):
        p_train = int(len(x) * per_train)

        x_train = [x[i] for i in range( p_train )]
        x_test = [x[i] for i in range( p_train, len(x) )]
        r_train = [r[i] for i in range( p_train )]
        r_test = [r[i] for i in range( p_train, len(x) )]

        return np.asarray(x_train), np.asarray(x_test), np.asarray(r_train), np.asarray(r_test)

    # private method:
    #   input: classification, loaded points, or manualy added points
    #   return
    # Note: Once again iam not sure, if it is most optimezed way, but in this
    # function is just added to loaded points inside/outside label and write to
    # output of terminal and csv file.
    def __save_data(self, k, points):
        
        for i in range(len(k)):
            if k[i] == 1:
                points[i].append("inside")

            else:
                points[i].append("outside")

        OutputCom.print_data(points)

        with open(self.filename, self.write) as file:
            writer = csv.writer(file, delimiter = ';')
            writer.writerows(points)
    
    # public method:
    #   input:
    #   return
    # There we approximate bounderies by defined classificator
    # in generated lin points, which higher number, time delay is longer
    def approx_bound(self):
        self.reset()
        x1, x2, x1_, x2_ = self.__lin_points(100)
        
        z = np.zeros((len(x1),len(x2)))

        for i in range(len(x1)):
            for j in range(len(x2)):
                z[i,j] = self.__net.predict( np.array( [[ x1_[i,j], x2_[i,j] ]] ) )

        self.graph.aprox_equation(x1,x2,z)
    
    # public method:
    #   input:
    #   return
    # Note: In this function is loaded ann model, and used for predict
    # generated points, and then filter.
    def net_gp(self):
        x, _ = self.__gen_numb()
        
        net = self.__net
        k = (net.predict(x) > 0.5).astype("int32")

        self.reset()
        self.__equation_bound()
        
        self.graph.set_color = "generated"
        self.__filter(k, x)
    
    # public method:
    #   input: points
    #   return
    # Note: In this function is loaded ann model, and used for predict
    # loaded points, and then filter.  
    def net_sp(self,points):
        p = np.array(points)

        net = self.__net
        k = (net.predict(p) > 0.5).astype("int32")

        self.graph.set_color = "new_points"

        self.__filter(k, p)
        self.__save_data(k, points)

    # publick method:
    #   input: save_file - by default is True for option to once again to train ann
    #   return
    # Note: In this function is pre - defined network to maximaze accuracy to classification points. 
    def train_net(self, save=False):
        x, r = self.__gen_numb()

        x_train, x_test, r_train, r_test = self.__split_data(x,r) 

        net = Sequential()

        net.add(Dense(64, input_dim=2, activation ='tanh'))
        net.add(Dense(8, activation ='tanh'))
        net.add(Dense(2, activation ='tanh'))
        net.add(Dense(1, activation ='sigmoid'))

        net.compile(loss='binary_crossentropy', optimizer='Nadam', metrics=['accuracy'])
        
        log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        tensorboard_callback = keras.callbacks.TensorBoard(log_dir = log_dir, histogram_freq = 1)
        
        net.fit(x_train, r_train, epochs = 500, batch_size = 64, verbose=0, callbacks = [tensorboard_callback])

        test_loss, test_acc = net.evaluate(x_test, r_test)
        
        print("[INFO] " + str(test_acc))
        print("[INFO] " + str(test_loss))
        
        #                       -- TENSORBOARD --
        # Is there possibility to run tensorboard, after training or before training,
        # default there are 2 datasets.
        # In this lovely tool you can see loss and accuracy during training and much more. 
        # for run: "tensorboard --logdir logs/fit"

        if save:
           net.save('net_model')
        
        k = (net.predict(x) > 0.5).astype("int32")
        
        self.graph.set_color = "generated"
        self.reset()
        self.__equation_bound()
        self.__filter(k, x)

        return test_acc, test_loss        

    # publick method:
    # pure draw equation
    def elipse(self):
        self.reset()
        self.__equation_bound()
    
    # publick method:
    # reset function to remove all traces from graph
    def reset(self):
        self.graph.fig.data = []
