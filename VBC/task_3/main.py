import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from hc12 import HC12
from ga import GA
from obj_func import Obj_Func

def graph(x, f, time, switch = 1):
    N = 100

    # switch
    #   1 - rastrigins
    #   2 - rossenbrock
    #   3 - schwefell
    if switch == 1:
        l = np.linspace(-5.12, 5.12, N)        
        x1, x2 = np.meshgrid(l, l)
        z = np.zeros((N, N))

        for i in range(N):
            for j in range(N):
                z[i,j] = Obj_Func().rastrigin([x1[i, j], x2[i, j]])
    
    elif switch == 2:
        l = np.linspace(-5, 10, N)        
        x1, x2 = np.meshgrid(l, l)
        z = np.zeros((N, N))

        for i in range(N):
            for j in range(N):
                z[i,j] = Obj_Func().rosenbrock([x1[i, j], x2[i, j]])
    
    elif switch == 3:
        l = np.linspace(-500, 500, N)        
        x1, x2 = np.meshgrid(l, l)
        z = np.zeros((N, N))

        for i in range(N):
            for j in range(N):
                z[i,j] = Obj_Func().schwefel([x1[i, j], x2[i, j]])
    
    else:
        print("U dont put valid switch var!")
        sys.exit()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x1, x2, z, cmap=cm.coolwarm,alpha=0.2)
    
    #for i in range(len(x)):
    #    ax.scatter(x[i][0],x[i][1],f, marker="^", color='r')
    
    ax.scatter(x[0],x[1],f, marker="^", color='r')

    ax.view_init(-90,90)
    plt.show()

    plt.boxplot(time)
    plt.show()

def statisctis(x,fx,time):
    # find min
    idx_min = np.argmin(fx)
    print(f'[INFO] min: x = {x[idx_min, :]}, fx = {fx[idx_min]}, t = {time[idx_min]:.4f}')
    
    # find mmax
    idx = np.argmax(fx)
    print(f'[INFO] max: x = {x[idx, :]}, fx = {fx[idx]}, t = {time[idx]:.4f}')

    # compute meam t
    mean = np.mean(time)
    print(f'[INFO] mean: t = {mean:.4f}')

    # compute meam fx
    mean = np.mean(fx)
    print(f'[INFO] mean: fx = {mean:.4f}')

    # compute meam x
    mean = np.mean(x)
    print(f'[INFO] mean: x = {mean:.4f}')

    # compute median t
    median = np.median(time)
    print(f'[INFO] median: t = {median:.4f}')

    # compute median fx
    median = np.median(fx)
    print(f'[INFO] median: fx = {median:.4f}')

    # compute median x
    median = np.median(x)
    print(f'[INFO] median: x = {median:.4f}')

    # plot graph
    graph(x[idx_min, :], fx[idx_min], time)
    # graph(x, fx, time)

if __name__ == "__main__":
    np.random.seed(200543)
    
    x, fx, time = HC12().hc12()
    # x, fx, time = GA().ga()

    statisctis(x, fx, time)