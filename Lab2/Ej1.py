import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit               # para lectura de teclas no bloqueante

CHUNK = 1024

# leemos wav en array numpy (data)
# por defecto lee float64 (no soportado por portAudio) 
# podemos hacer directamente la conversion a float32
data, SRATE = sf.read('piano.wav',dtype="float32")


# informacion de wav)
print("\n\nInfo del wav ",SRATE)
print("  Sample rate ",SRATE)
print("  Sample format: ",data.dtype)
print("  Num channels: ",len(data.shape))
print("  Len: ",data.shape[0])