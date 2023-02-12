import numpy as np
import matplotlib.pyplot as plt
import random as rd

SRATE = 44100
dur = 0.1

def main():
    v = np.random.random(int(SRATE * dur)) * 2 - 1
    #np.arange(int(SRATE * dur), dtype=np.float32)
    #for i in range(len(v)):
        #v[i] = rd.random() * 2 - 1

    plt.plot(v)
    plt.show()

main()