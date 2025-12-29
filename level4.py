import re
import numpy as np
import sounddevice as sd
import time
import random

def counta_syllable(word):
    word = word.lower()
    vowels = "aeiou"
    count=0
    prev= False

    for ch in word:
        if ch in vowels:
            if not prev:
                count +=1
            prev = True
        else: 
            prev= False
    return max(1 , count)

line = "Jingle Bells, Jingle Bells Jingle all the way Oh what fun it is to ride in a One horse open sleigh"

words = re.findall(r"[a-zA-Z]+",line)

syllable= []
for w in words:
    syllable += [w] * counta_syllable(w)

print(syllable)

duration = [0.3]* len(syllable)
print(duration)

scale = [57, 59, 60, 62, 64 ,65, 67]
melody_idx = [len(scale)//2]

for _ in range(len(syllable)-1):
    step =random.choice([-2, -1, 1 ,2])
    ni = melody_idx[-1]+ step

    if ni<0:
        ni = abs(ni)
    elif ni>= len(scale):
        ni = (len(scale)-1) - (ni- (len(scale)-1))
    
    melody_idx.append(ni)

meloddy_notes = [scale[i] for i in melody_idx]

def midi_freq(m):
    return 440 * 2**((m-69)/12)

for note , dur in zip(meloddy_notes , duration):
    freq = midi_freq(note)
    t = np.linspace(0 , dur , int(44100 * dur), False)
    wave = np.sin(2 * np.pi * freq * t)
    sd.play(wave, 44100)
    sd.wait()
    time.sleep(0.05)