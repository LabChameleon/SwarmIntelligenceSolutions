import numpy as np
import matplotlib.pyplot as plt

np.random.seed()
fig = plt.figure()

def excA(steps = 1000, num_p = 5):
    s = 100 / num_p
    p_c = 1 / (1 + np.exp(-0.1*(num_p - 30)))
    p_h = 0.5 * (1 - 1 / (1 + np.exp(-0.05*(s-15)))) + 0.25
    work_todo = np.tile(s, num_p)
    work_done = 0

    for i in range(steps):
        for j in range(num_p):
            toss = np.random.uniform()
            if toss > p_c and toss < p_h and work_todo[j] > 0:
                work_todo[j] = work_todo[j] - 1
                if work_todo[j] == 0:
                    work_done = work_done + 1
                    work_todo[j] = s

    
    return work_done

def excB():
    num_p = range(1,80)
    work_done = [excA(num_p = p)/p for p in num_p]
    ax = fig.add_subplot(111, label = "1")
    ax.plot(num_p, work_done)
    plt.show()

