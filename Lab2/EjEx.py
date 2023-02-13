from msilib.schema import FeatureComponents
import kbhit
import sounddevice as sd
import soundfile as sf
from scipy.io import wavfile # para manejo de wavs
#from scipy import signal
import numpy as np  # arrays    
import matplotlib.pyplot as plt

SRATE = 44100
CHUNK = 2048
STDFREC = 440
MODFREC = 27.5

class Osc:
    def __init__(self, f = 0):
        self.frec = f
        self.index = 0

    def changeFrec(self, frec):
        self.frec = frec

    def next(self):
        chunkWave = np.arange(CHUNK, dtype = np.float32)

        for i in range(len(chunkWave)):
            chunkWave[i] = np.sin((self.index + i) * (2 * np.pi) * self.frec / SRATE) # asumimos time = 1

        self.index += CHUNK

        return chunkWave

    def nextRingMod(self):
        chunkWave = np.arange(CHUNK, dtype = np.float32)

        for i in range(len(chunkWave)):
            chunkWave[i] = (np.sin((self.index + i) * (2 * np.pi) * self.frec / SRATE) + 1)/2  # asumimos time = 1

        self.index += CHUNK

        return chunkWave

    def nextSquare(self):
        chunkWave = np.arange(CHUNK, dtype = np.float32)

        for i in range(len(chunkWave)):
            # chunkWave[i] = signal.square((self.index + i) * (2 * np.pi) * self.frec / SRATE)
            chunkWave[i] = 1 if np.sin((self.index + i) * (2 * np.pi) * self.frec / SRATE) > 0 else -1

        self.index += CHUNK

        return chunkWave

    def nextTriangle(self):
        chunkWave = np.arange(CHUNK, dtype = np.float32)

        for i in range(len(chunkWave)):
            chunkWave[i] = (2 / np.pi) * np.arcsin(np.sin((self.index + i) * (2 * np.pi) * self.frec / SRATE))

        self.index += CHUNK

        return chunkWave

    def nextSaw(self):
        chunkWave = np.arange(CHUNK, dtype = np.float32)

        for i in range(len(chunkWave)):
            #chunkWave[i] = (2 / numpy.pi) * numpy.arctan(numpy.tan(wave[i] / SRATE * (time * 2 * numpy.pi) / 2))
            chunkWave[i] = (2 / np.pi) * np.arctan(np.tan(((self.index + i) * (2 * np.pi) * self.frec / SRATE)/2))

        self.index += CHUNK

        return chunkWave

# Modulador de Amplitud
def modula(sample, modWave):
    for i in range(len(sample)):
        sample[i] *= modWave[i]

# Muestra matplotlib
def setGraphics(wave):
    x = list(range(len(wave)))
    y = [sample for sample in wave]

    plt.plot(x, y)

bloque = np.arange(CHUNK, dtype = np.float32)

# abrimos stream
stream = sd.OutputStream(samplerate=SRATE, 
    blocksize=CHUNK,
    channels=len(bloque.shape))

# arrancamos stream
stream.start()

# En data tenemos el wav completo, ahora procesamos por bloques (chunks)
kb = kbhit.KBHit()
osc = Osc(STDFREC)
oscMod = Osc(MODFREC)
numBloque = 0
c = ' '

while c != 'q': 
    # nuevo bloque 
    bloque = osc.next() 
    # bloque = osc.nextSquare() 
    # bloque = osc.nextTriangle() 
    # bloque = osc.nextSaw() 

    # Ring Modulation
    # bloqueMod = oscMod.nextRingMod() 

    # Amplitude Modulation
    bloqueMod = oscMod.next() 

    modula(bloque, bloqueMod)

    stream.write(bloque)        
    
    if kb.kbhit():
        c = kb.getch()
        if (c=='f'): STDFREC= max(220,STDFREC-0.5)
        elif (c=='F'): STDFREC= min(880,STDFREC+0.5)
        print("Frec: ",STDFREC)

    osc.changeFrec(STDFREC)

    numBloque += 1


setGraphics(bloqueMod)
setGraphics(bloque)
plt.show()

kb.set_normal_term()        
stream.stop()