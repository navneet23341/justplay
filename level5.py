import re
import numpy as np
import sounddevice as sd
import random

SAMPLE_RATE = 44100
BPM = 100
SECOND_PER_BEAT= 60 /BPM

def counta_syllable(word):
    word = word.lower()
    vowels = "aeiou"
    count = 0
    prev = False

    for ch in word:
        if ch in vowels:
            if not prev:
                count += 1
            prev = True
        else:
            prev = False

    return max(1, count)


def midi_freq(m):
    return 440 * 2 ** ((m - 69) / 12)

def syllable_beats(words):
    beats = []
    for w in words:
        c = counta_syllable(w)
        if c == 1:
            beats.append(1)          # quarter note
        else:
            beats.append(1)          # stressed
            beats.extend([0.5] * (c - 1))  # unstressed
    return beats



def apply_envelope(wave, sample_rate):
    attack = int(0.05 * sample_rate)
    release = int(0.1 * sample_rate)

    envelope = np.ones(len(wave))
    envelope[:attack] = np.linspace(0, 1, attack)
    envelope[-release:] = np.linspace(1, 0, release)

    return wave * envelope


lyrics = [
    "Jingle Bells Jingle Bells",
    "Jingle all the way",
    "Oh what fun it is to ride",
    "In a one horse open sleigh"
]

scale = [57, 59, 60, 62, 64, 65, 67]

for line in lyrics:
    words = re.findall(r"[a-zA-Z]+", line)

    syllables = []
    durations = []
    beats =[]

    # -------- syllable + duration creation --------
    for w in words:
        count = counta_syllable(w)

        for i in range(count):
            syllables.append(w)

            if i == 0:
                beats.append(1)          # quarter note
            else:
                beats.append(0.5)          # stressed
                  # unstressed

    # beats = syllable_beats(words)
    durations = [b * SECOND_PER_BEAT for b in beats]
    durations[-1] += 1 * SECOND_PER_BEAT
# phrase ending

    # -------- melody generation --------
    melody_idx = [len(scale) // 2]

    for _ in range(len(syllables) - 1):
        step = random.choice([-2, -1, 1, 2])
        ni = melody_idx[-1] + step

        if ni < 0:
            ni = 0
        elif ni >= len(scale):
            ni = len(scale) - 1

        melody_idx.append(ni)

    melody_notes = [scale[i] for i in melody_idx]
    melody_notes[-1] = scale[0]  # resolve

    # -------- play --------
    for note, dur in zip(melody_notes, durations):
        freq = midi_freq(note)
        t = np.linspace(0, dur, int(SAMPLE_RATE * dur), False)

        wave = (
            1.0 * np.sin(2 * np.pi * freq * t) +
            0.5 * np.sin(2 * np.pi * freq * 2 * t) +
            0.25 * np.sin(2 * np.pi * freq * 3 * t)
        )

        wave = wave / np.max(np.abs(wave))
        wave = apply_envelope(wave, SAMPLE_RATE)

        sd.play(wave, SAMPLE_RATE)
        print(freq)
        print(dur)
        sd.wait()
