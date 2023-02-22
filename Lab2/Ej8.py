import kbhit
import sounddevice as sd
import soundfile as sf

# piano
data, SRATE = sf.read('piano.wav')

# stream
stream = sd.OutputStream(samplerate=SRATE, channels=len(data.shape))
stream.start()


kb = kbhit.KBHit()

c = '-'

# Multiplicador de pitch para generar notas las notas del piano

scale = [1.0, 1.12, 1.25, 1.33, 1.5, 1.69, 1.88, 2.0, 2.24, 2.51, 2.66, 2.99, 3.36, 3.78, 4]

i = 0
for s in scale:
    scale[i] = s * SRATE
    i += 1

# Espacio para parar
while c != ' ': 
    if kb.kbhit():
        c = kb.getch()

        if (c=='q'): sd.play(data, scale[0])
        elif (c=='w'): sd.play(data, scale[1])
        elif (c=='e'): sd.play(data, scale[2])
        elif (c=='r'): sd.play(data, scale[3])
        elif (c=='t'): sd.play(data, scale[4])
        elif (c=='y'): sd.play(data, scale[5])
        elif (c=='u'): sd.play(data, scale[6])
        elif (c=='a'): sd.play(data, scale[7])
        elif (c=='s'): sd.play(data, scale[8])
        elif (c=='d'): sd.play(data, scale[9])
        elif (c=='f'): sd.play(data, scale[10])
        elif (c=='g'): sd.play(data, scale[11])
        elif (c=='h'): sd.play(data, scale[12])
        elif (c=='j'): sd.play(data, scale[13])
        elif (c=='k'): sd.play(data, scale[14])

kb.set_normal_term()        
stream.stop()
exit()


