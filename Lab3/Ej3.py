# creacion de una ventana de pygame
import pygame
import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
from pygame.locals import *


SRATE = 44100       # sampling rate, Hz, must be integer
CHUNK = 1024
# fc, carrier = pitch, fm frecuencia moduladora, beta = indice de modulacion
def oscFM(fc,fm,beta,vol,frame):
    # sin(2πfc+βsin(2πfm))   http://www.mrcolson.com/2016/04/21/Simple-Python-FM-Synthesis.html
    sample = np.arange(CHUNK)+frame
    mod = beta*np.sin(2*np.pi*fm*sample/SRATE)
    res = np.sin(2*np.pi*fc*sample/SRATE + mod)
    return vol*res

def osc(frec,vol):
    return np.float32(vol*np.sin(2*np.pi*(np.arange(CHUNK)+frame)*frec/SRATE))

WIDTH = 640 # ancho y alto de la ventana de PyGame
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Theremin")

# Control loop de la ventana
loop = True

stream = sd.OutputStream(samplerate=SRATE,blocksize=CHUNK,channels=1)  
stream.start()

fc = 440
fm = 300
beta = 1
vol = 0.8
frame = 0


while(loop):
    
    #samples = oscFM(fc,fm,beta,vol,frame)
    samples = osc(fc, vol)
    stream.write(np.float32(0.5*samples)) 
    frame += CHUNK

    # obtencion de la posicion del raton
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
            loop = False 
        if event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = event.pos
            # Control de la frecuencia y amplitud en función de la posicion del ratón
            if(mouseX >= 0 and mouseX <= WIDTH): fc = 9900 * (mouseX/WIDTH) + 100 
            if(mouseY >= 0 and mouseY <= HEIGHT): vol = mouseY / HEIGHT


stream.stop()
pygame.quit()