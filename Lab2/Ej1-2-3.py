import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
from scipy import signal
import kbhit               # para lectura de teclas no bloqueante
import soundfile as sf     # para lectura/escritura de wavs
import matplotlib.pyplot as plt

CHUNK = 2048
SRATE = 44100

last = 0 # ultimo frame generado
lastMod = 0

def osc(dur, freq):
    v = np.linspace(0, dur, int(SRATE*dur), endpoint=False)
    w = np.sin(2 * np.pi * v * freq/SRATE)
    return w

def oscChuckRing(frec, vol):
    global last # var global
    data = vol * np.sin(2*np.pi*(np.arange(CHUNK,dtype="float32")+last)* frec/SRATE + 1) / 2
    last += CHUNK # actualizamos ultimo generado
    return np.float32(data)


def oscChuckSawtooth(frec, vol):
    global last # var global
    data = vol * signal.sawtooth(2*np.pi*(np.arange(CHUNK,dtype="float32")+last)* frec/SRATE)
    last += CHUNK # actualizamos ultimo generado
    return np.float32(data)

def oscChuckSquare(frec, vol):
    global last # var global
    data = vol * signal.square(2*np.pi*(np.arange(CHUNK,dtype="float32")+last)* frec/SRATE)
    last += CHUNK # actualizamos ultimo generado
    return np.float32(data)

def oscChuckTriangle(frec, vol):
    global last # var global
    data = vol * (2/np.pi) * np.arcsin(np.sin(2*np.pi*(np.arange(CHUNK,dtype="float32")+last)* frec/SRATE))
    last += CHUNK # actualizamos ultimo generado
    return np.float32(data)

def oscChuck(frec, vol):
    global last # var global
    data = vol * np.sin(2*np.pi*(np.arange(CHUNK,dtype="float32")+last)* frec/SRATE)
    last += CHUNK # actualizamos ultimo generado
    return np.float32(data)

def oscChuckMod(frec, vol):
    global lastMod # var global
    data = vol * np.sin(2*np.pi*(np.arange(CHUNK,dtype="float32")+last)* frec/SRATE)
    lastMod += CHUNK # actualizamos ultimo generado
    return np.float32(data)

vol = 1.0
freq = 440.0

# abrimos stream de salida
stream = sd.OutputStream(
    samplerate = SRATE,            # frec muestreo 
    blocksize  = CHUNK,            # tamaño del bloque (muy recomendable unificarlo en todo el programa)
    channels   = 1)  # num de canales

# arrancamos stream
stream.start()

kb = kbhit.KBHit()
c= ' '

# En data tenemos el audio completo, ahora procesamos por bloques (chunks)
numBloque = 0 # contador de bloques/chunks

print('\n\nProcessing chunks: ',end='')

while c!= 'q': 
    samples = oscChuckTriangle(freq, vol)

    samples *= oscChuckMod(27.5, vol)
    # lo pasamos al stream
    stream.write(samples) # escribimos al stream

    # modificación de volumen 
    if kb.kbhit():
        c = kb.getch()
        if (c=='v'): vol= max(0,vol-0.05)
        elif (c=='V'): vol= min(1,vol+0.05)
        elif(c=='f'): freq = max(20, freq-1)
        elif(c=='F'): freq = min(20000, freq+1)
        print("Vol: ",vol)

    numBloque += 1
    print('.',end='')

print('end')

stream.stop()
stream.close()
kb.set_normal_term()
