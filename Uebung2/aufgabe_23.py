import numpy as np
import matplotlib.pyplot as plt 


def createSwarm(num_flies = 150, r = 0.1):
    fireflies = np.random.uniform(size=(num_flies,2))

    neighbour_relation = []
    for i, fly_a in enumerate(fireflies):
        n_flies = []
        for j, fly_b in enumerate(fireflies):
            if not i == j:
                if np.sqrt((fly_a[0] - fly_b[0])**2 + (fly_a[1] - fly_b[1])**2) < r:
                    n_flies = n_flies + [j]
        neighbour_relation = neighbour_relation + [n_flies]

    return fireflies, neighbour_relation

def majority(fly, relation, cur_time):
    counter = 0
    for i in relation[fly]:
        if cur_time[i] > 24:
            counter = counter + 1
    if counter > len(relation[fly]) / 2:
        return True
    return False

def simulate(flies, relation):
    cur_time = {}
    glowing_stats = []
    max_glowing = 0
    min_glowing = 150
    for i, fly in enumerate(flies):
        cur_time[i] = np.random.randint(0, 49)
    for num_epoch in range(5000):
        num_glowing = 0 
        for i, fly in enumerate(flies):
            if cur_time[i] > 24:
                num_glowing = num_glowing + 1 
            if cur_time[i] == 25 and majority(i, relation, cur_time):
                cur_time[i] = cur_time[i] + 1
            cur_time[i] = (cur_time[i] + 1) % 50
        glowing_stats = glowing_stats + [num_glowing]
        if num_epoch >= 4949:
            if num_glowing > max_glowing:
                max_glowing = num_glowing
            if num_glowing < min_glowing:
                min_glowing = num_glowing
    return glowing_stats, max_glowing - min_glowing
         
def exerciseA():
    for r in [0.05, 0.1, 0.5, 1.4]:
        flies, relation = createSwarm(num_flies = 150, r = r)
        average_neigh = 0.
        for neighbour in relation:
            average_neigh = average_neigh + len(neighbour)
        average_neigh = average_neigh / len(flies)
        glowing_stats, _ = simulate(flies, relation)
        fig = plt.figure()
        ax = fig.add_subplot(111, label="1")
        print("Average neighbours for r = %.2f: %.2f" % (r, average_neigh))
        ax.set_ylim(0,150)
        ax.plot(range(0,5000), glowing_stats)
        plt.show()

def exerciseB():
    amplitudes = []
    for r in range(25, 1400, 25):
        amplitude_sum = 0
        for epoch in range(50):
            flies, relation = createSwarm(num_flies = 150, r = r/1000.0)
            _, amplitude = simulate(flies, relation)
            amplitude_sum = amplitude_sum + amplitude
        amplitudes = amplitudes + [amplitude_sum / 50]
        print(r)
    fig = plt.figure()
    ax = fig.add_subplot(111, label="1")
    ax.set_ylim(0,160)
    x_val = [x/1000 for x in range(25, 1400, 25)]
    ax.plot(x_val, amplitudes)
    plt.show()

