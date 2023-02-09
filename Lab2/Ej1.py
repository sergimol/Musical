import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit               # para lectura de teclas no bloqueante

CHUNK = 1024
SRATE = 44100

def osc(dur, freq):
    v = np.linspace(0, dur, int(SRATE*dur), endpoint=False)
    w = np.sin(2 * np.pi * v)
    return w

last = 0 # ultimo frame generado
def oscChuck(frec, vol):
    global last # var global
    data = vol * np.sin(2*np.pi*(np.arange(CHUNK,dtype="float32")+last)* frec/SRATE)
    last += CHUNK # actualizamos ultimo generado
    return data

vol = 1.0
freq = 20.0

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

while c!= 'q' and not(end)>0: 
    samples = oscChuck(freq, vol)
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
