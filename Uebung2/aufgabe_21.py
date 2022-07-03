import numpy as np
import matplotlib.pyplot as plt

np.random.seed(1)
rng = np.random.default_rng()
fig = plt.figure()  

def samplePoisson(lambda_par):
    return rng.poisson(lam=lambda_par, size=1)[0]

def excC(steps = 2000, lamb = 0.1, speed = 4):
    queue = 0
    cur_work = 0
    avg_queue = 0
    for i in range(0,steps):
        queue = queue + samplePoisson(lamb)
        if cur_work == 0 and queue > 0:
            queue = queue - 1
            cur_work = speed
        if cur_work > 0:
            cur_work = cur_work - 1
        avg_queue = avg_queue + queue
        if i % 50 == 0:
            print("step: %i: %f" % (i, avg_queue / i))
    return avg_queue / steps

def excD(speed = 4):
    results = []
    for i in range(5, 250, 5):
        results = results + [excC(200, i / 1000, speed)]

    ax = fig.add_subplot(111, label="1")
    ax.plot([x / 1000 for x in range(5, 250, 5)], results)  
    plt.show()

def excE():
    excD(4)
    excD(2)
    plt.show()

