from msilib.schema import FeatureComponents
import kbhit
import sounddevice as sd
import soundfile as sf

import numpy as np  # arrays    
import matplotlib.pyplot as plt

# SRATE = 44100
CHUNK = 2048

# Muestra matplotlib
def setGraphics(wave):
    x = list(range(len(wave)))
    y = [sample for sample in wave]

    plt.plot(x, y)

data, SRATE = sf.read('piano.wav', dtype="float32")

# abrimos stream
stream = sd.OutputStream(samplerate=SRATE, 
    blocksize=CHUNK,
    channels=len(data.shape))

# arrancamos stream
stream.start()

# En data tenemos el wav completo, ahora procesamos por bloques (chunks)
kb = kbhit.KBHit()
numBloque = 0
c = ' '

vol = 1.0
minVol = -1.0

nSamples = CHUNK

while nSamples >= CHUNK: 
     # numero de samples a procesar: CHUNK si quedan y si no, los que queden
    nSamples = min(CHUNK, data.shape[0] - (numBloque + 1) * CHUNK)

    # nuevo bloque
    bloque = data[numBloque * CHUNK : numBloque * CHUNK + nSamples]

    maxValue = np.amax(np.abs(bloque))
    maxVol = 1 / maxValue

    bloque *= max(minVol, min(maxVol, vol))

    stream.write(bloque)        
    
    numBloque += 1

setGraphics(bloque)
plt.show()

kb.set_normal_term()        
stream.stop()
exit()