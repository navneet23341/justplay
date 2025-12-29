import re
import numpy as np
import sounddevice as sd
import random

SAMPLE_RATE = 44100

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

    # -------- syllable + duration creation --------
    for w in words:
        count = counta_syllable(w)

        for i in range(count):
            syllables.append(w)

            if i == 0:
                durations.append(0.6)   # stressed
            else:
                durations.append(0.45)  # unstressed

    durations[-1] += 0.5  # phrase ending

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
