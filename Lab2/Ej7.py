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

notas = "A.BC.D.EF.G.a.bc.d.ef.g"

# abrimos stream
stream = sd.OutputStream(samplerate=SRATE, 
    blocksize=CHUNK,
    channels=1)

stream.start()

# partitura
part = [('G', 0.5), ('G', 0.5), ('a', 1), ('G', 1),
('c', 1), ('b',2), ('G', 0.5), ('G', 0.5), ('a', 1), ('G', 1),
('d', 1), ('c',2), ('G', 0.5), ('G',0.5), ('g', 1), ('e', 1),
('c', 1), ('b', 1), ('a', 1), ('f', 0.5), ('f', 0.5), ('e', 1),
('c', 1), ('d', 1),('c', 2)]

i = 0
while len(part) > i:
    
    frec = 440 * (2**(notas.index(part[i][0])/12))
    dur = part[i][1]

    nota = osc(frec, dur, 1)
    # silencio para separar las notas
    nota = np.append(nota, np.zeros(5))

    stream.write(np.float32(nota))
    i += 1

stream.stop()
exit()