import numpy as np
from soundgen import (
    mono_array_to_sound,
    play,
    write_wav,
    silence,
    sinewave,
)

volume = 0.5
fundamental = 55
t = 0.4

print('building scale')
scale_clips = [silence(t)]
for i in range(1, 16 + 1):
    scale_clips.append(
        sinewave(t, i * fundamental) * volume
    )

melody = [
    8, 9,
    8, 9, 10, 9,
    8, 9, 10, 11, 10, 9,
    8, 9, 10, 11, 12, 11, 10, 9,
    8, 9, 10, 11, 12, 13, 12, 11, 10, 9,
    8, 9, 10, 11, 12, 13, 14, 13, 12, 11, 10, 9,
    8, 9, 10, 11, 12, 13, 14, 15, 14, 13, 12, 11, 10, 9,
    8, 9, 10, 11, 12, 13, 14, 15, 16, 15, 14, 13, 12, 11, 10, 9,
    8,
]

print('generating melody')
values = np.concatenate([
    scale_clips[m] for m in melody
])

sound = mono_array_to_sound(values)
write_wav(sound, 'harmonic_scale.wav')
play(sound)
