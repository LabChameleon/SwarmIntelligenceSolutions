import numpy as np
import matplotlib.pyplot as plt

def exercise_a(num_steps = 50, alpha_s = 0.6, alpha_p = 0.2):

    n_s = [1]
    delta_n_s = []
    m = [1]
    delta_m =[]

    for t in range(num_steps*100-1):
        if t-200 >= 0:
            delta_n_s += [-alpha_s * n_s[t]*(n_s[t]+1) +
                    alpha_s * n_s[t-200]*(n_s[t-200]+1)]
        else:
            delta_n_s += [-alpha_s * n_s[t]*(n_s[t]+1)]
        n_s += [n_s[t] + delta_n_s[t] / 100] 
        delta_m += [-alpha_p * n_s[t] * m[t]]
        m += [m[t] + delta_m[t] / 100]

    plt.plot(np.arange(0,num_steps,1/100), n_s) 
    plt.plot(np.arange(0,num_steps,1/100), m) 
    plt.show()

def exercise_b(num_steps = 160, alpha_s = 0.6, alpha_p = 0.2):

    n_s = [1]
    delta_n_s = []
    m = [1]
    delta_m =[]
    n_ho = [0]
    delta_n_ho = []

    for t in range(num_steps*100-1):
        delta_n_cur = (-alpha_s * n_s[t]*(n_s[t]+1) - 
                    alpha_p * n_s[t] * m[t])
        if t-200 >= 0:
            delta_n_cur += alpha_s * n_s[t-200]*(n_s[t-200]+1)
        if t-1500 >= 0:
            delta_n_cur += alpha_p * n_s[t-1500]*m[t-1500]
        delta_n_s += [delta_n_cur]
        n_s += [n_s[t] + delta_n_s[t] / 100] 

        delta_m += [-alpha_p * n_s[t] * m[t]]
        m += [m[t] + delta_m[t] / 100]

        delta_ho_cur = alpha_p * n_s[t] * m[t]  
        if t - 1500 >= 0:
            delta_ho_cur += -alpha_p * n_s[t-1500] * m[t-1500]
        delta_n_ho += [delta_ho_cur]
        n_ho += [n_ho[t] + delta_n_ho[t] / 100]

    plt.plot(np.arange(0,num_steps,1/100), n_s) 
    plt.plot(np.arange(0,num_steps,1/100), m) 
    plt.plot(np.arange(0,num_steps,1/100), n_ho) 
    plt.show()

def exercise_b2(num_steps = 160, alpha_s = 0.6, alpha_p = 0.2):

    n_s = [1]
    delta_n_s = []
    m = [1]
    delta_m =[]
    n_ho = [0]
    delta_n_ho = []

    for t in range(num_steps*100-1):

        if t == 8000:
            m[t] = 0.5

        delta_n_cur = (-alpha_s * n_s[t]*(n_s[t]+1) - 
                    alpha_p * n_s[t] * m[t])
        if t-200 >= 0:
            delta_n_cur += alpha_s * n_s[t-200]*(n_s[t-200]+1)
        if t-1500 >= 0:
            delta_n_cur += alpha_p * n_s[t-1500]*m[t-1500]
        delta_n_s += [delta_n_cur]
        n_s += [n_s[t] + delta_n_s[t] / 100] 

        delta_m += [-alpha_p * n_s[t] * m[t]]
        m += [m[t] + delta_m[t] / 100]

        delta_ho_cur = alpha_p * n_s[t] * m[t]  

        if t - 1500 >= 0:
            delta_ho_cur += -alpha_p * n_s[t-1500] * m[t-1500]
        delta_n_ho += [delta_ho_cur]
        n_ho += [n_ho[t] + delta_n_ho[t] / 100]

    plt.plot(np.arange(0,num_steps,1/100), n_s) 
    plt.plot(np.arange(0,num_steps,1/100), m) 
    plt.plot(np.arange(0,num_steps,1/100), n_ho) 
    plt.show()

exercise_a(alpha_s = 0.6)
exercise_b(alpha_s = 0.6)
exercise_b2(alpha_s = 0.6)



