from msilib.schema import FeatureComponents
import kbhit
import sounddevice as sd
import soundfile as sf

import numpy as np  # arrays    
import matplotlib.pyplot as plt

SRATE = 44100
CHUNK = 2048

def osc(frec,dur,vol):
    return vol * np.sin(2*np.pi*np.arange(int(SRATE*dur))*frec/SRATE)

notas = {
    "A": 440,
    "B": 493.8835,
    "C": 523.251,
    "D": 587.33,
    "E": 659.255,
    "F": 698.456,
    "G": 783.991,
}

