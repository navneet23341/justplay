import numpy as np
import sounddevice as sd
import time
import random

sampple_rate= 44100
duration =0.5
freq = 440

def midi_to_freq(midi):
    return 440 * (2**((midi-69)/12))

#tuning c major 
# c_major = [60, 62, 64, 65, 67, 69, 71, 72]

# for note in c_major:
#     freq=midi_to_freq(note)
#     t= np.linspace(0 , duration , int(sampple_rate*duration), False)

#     wave = np.sin(2 *np.pi* freq * t)
#     sd.play(wave , sampple_rate)
#     sd.wait()
#     time.sleep(0.1)

# random suffling 
# c_major = [60, 62, 64, 65, 67, 69, 71, 72]
# random.shuffle(c_major)

# for note in c_major:
#     freq=midi_to_freq(note)
#     t= np.linspace(0 , duration , int(sampple_rate*duration), False)

#     wave = np.sin(2 *np.pi* freq * t)
#     sd.play(wave , sampple_rate)
#     sd.wait()
#     time.sleep(0.1)

#melody generator 
c_major = [60, 62, 64, 65, 67, 69, 71, 72]
melody = [random.randint(0, len(c_major)-1)]

for _ in range(15):
    step = random.choice([-2, -1, 1, 2])
    next_index = melody[-1] + step
    next_index = max(0, min(next_index, len(c_major)-1))
    melody.append(next_index)

melody_notes = [c_major[i] for i in melody]

for note in melody_notes:
    freq = midi_to_freq(note)
    t = np.linspace(0, duration, int(sampple_rate * duration), False)
    wave = np.sin(2 * np.pi * freq * t)

    print(freq)
    sd.play(wave, sampple_rate)
    sd.wait()
    time.sleep(0.05)