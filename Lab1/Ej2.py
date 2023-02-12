import numpy as np
import matplotlib.pyplot as plt
import random as rd

SRATE = 44100

def osc(dur, freq):
    v = np.linspace(0, dur, int(SRATE*dur), endpoint=False)
    w = np.sin(2 * np.pi * freq * v)
    return w

def vol(sample, vol):
    newSample = sample * vol
    return newSample
    
sample = osc(1, 2)
sample = vol(sample, 2)
plt.plot(sample)
plt.show()