import kbhit
import sounddevice as sd
import soundfile as sf
import numpy as np

CHUNK = 1024
FREQ = 440

class Sampler():
    def __init__(self, sample, start, end, freq):
        self.sample = np.copy(sample) # full sample
        self.start = start # fixed loop start
        self.end = end # fixed loop end
        self.freq = freq # frequency
        self.loop = True
        self.index = 0 # current pos of sample

        if(self.end >= len(self.sample)):
            self.end = len(self.sample)

    def switch_loop(self):
        self.loop = not self.loop

    def get_chunk(self):
        # Reset de index
        if self.index >= len(self.sample): self.index = 0

        if not self.loop:
            # Se toma el menor, el tamaño de chunk o el de la muestra
            sampleSize = min(CHUNK, len(self.sample))

            # Rellenamos el chunk con la muestra
            samplesChunk = self.sample[self.index : self.index + sampleSize]

            # Rellenamos con 0s en caso de necesitarlo
            if sampleSize < CHUNK:
                samplesChunk = np.append(samplesChunk, np.zeros(CHUNK - len(samplesChunk), dtype=np.float32))
            
            # Avanzamos el index
            self.index += sampleSize

            return samplesChunk
        
        else:  
            # Fijamos verdadero final para el loop
            end = self.end if self.index + CHUNK > self.end else self.index + CHUNK

            samplesChunk = self.sample[self.index : end]

            # En caso de salirnos
            if end == self.end:
                # Reseteamos el bucle
                self.index = self.start
                # Y añadimos 0s a la muestra 
                samplesChunk = np.append(samplesChunk, np.zeros(CHUNK - len(samplesChunk), dtype=np.float32))
            else:
                self.index += CHUNK 

            return samplesChunk



        


# muestra
data, SRATE = sf.read('piano.wav', dtype=np.float32)

# stream
stream = sd.OutputStream(samplerate=SRATE,blocksize=CHUNK, channels=1, dtype=np.float32)
stream.start()

kb = kbhit.KBHit()

c = '-'

sampler = Sampler(data, 20000, 30000, 440)

while c != 'q':
    #if(stream.write_available >= SRATE):
    stream.write(sampler.get_chunk())

    if kb.kbhit():
        c = kb.getch()
        if c == 'l': sampler.switch_loop()

stream.stop()
