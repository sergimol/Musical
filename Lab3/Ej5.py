import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs

import kbhit 

SRATE = 44100       # sampling rate, Hz, must be integer
CHUNK = 1024
FREQ = 220

def play(notes, scale):
    ks = KarplusStrong(FREQ * scale)
    ks.get_note()
    notes.append(ks)

class KarplusStrong():
    def __init__(self, freq):
        self.freq = freq
        self.N = SRATE // int(self.freq) # la frecuencia determina el tamanio del buffer
        self.samples = []
        
        
    def get_note(self, dur = 1):
        nSamples = int(dur*SRATE)
        self.buf = np.random.rand(self.N) * 2 - 1 # buffer inicial: ruido
        self.samples = np.empty(nSamples, dtype=float) # salida
        # generamos los nSamples haciendo recorrido circular por el buffer
        for i in range(nSamples):
            self.samples[i] = self.buf[i % self.N] # recorrido de buffer circular
            self.buf[i % self.N] = 0.5 * (self.buf[i % self.N] + self.buf[(1 + i) % self.N]) # filtrado
    
    def get_chunk(self):
        # obtener chunk a reproducir 
        outputChunk = self.samples[:CHUNK]
        self.samples = self.samples[CHUNK:]

        return outputChunk

scale = [1.0, 1.12, 1.25, 1.33, 1.5, 1.69, 1.88, 2.0, 2.24, 2.51, 2.66, 2.99, 3.36, 3.78, 4]

kb = kbhit.KBHit()

c = '-'

stream = sd.OutputStream(samplerate=SRATE,blocksize=CHUNK,channels=1)  
stream.start()

notes = []

# Espacio para parar
while c != ' ': 
    samples = np.zeros(CHUNK)

    for note in notes:
        # Cogemos los samples de la nota actual
        chunk = note.get_chunk()
        # En caso de ser menor al tamaño de CHUNK, se añaden 0s
        if(len(chunk) < CHUNK):
            chunk = np.append(chunk, np.zeros(CHUNK- len(chunk)))
            # Y se elimina de notes, ya acabó la nota 
            notes.remove(note)
        # Se añade al samples final
        samples += chunk

    stream.write(np.float32(samples))

    if kb.kbhit():
        c = kb.getch()

        if (c=='q'): play(notes, scale[0])
        elif (c=='w'): play(notes, scale[1])
        elif (c=='e'): play(notes, scale[2])
        elif (c=='r'): play(notes, scale[3])
        elif (c=='t'): play(notes, scale[4])
        elif (c=='y'): play(notes, scale[5])
        elif (c=='u'): play(notes, scale[6])
        elif (c=='a'): play(notes, scale[7])
        elif (c=='s'): play(notes, scale[8])
        elif (c=='d'): play(notes, scale[9])
        elif (c=='f'): play(notes, scale[10])
        elif (c=='g'): play(notes, scale[11])
        elif (c=='h'): play(notes, scale[12])
        elif (c=='j'): play(notes, scale[13])
        elif (c=='k'): play(notes, scale[14])


stream.stop()