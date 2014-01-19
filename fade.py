import numpy as np
from soundgen import (
    mono_array_to_sound,
    play,
    write_wav,
    silence,
    sinewave,
)

t = 0.1
f = 440

clips = []
volume = 1.0
for _ in range(5):
    clips.append(sinewave(t, f) * volume)
    volume *= 0.6
    clips.append(silence(t))

values = np.concatenate(clips)

sound = mono_array_to_sound(values)
play(sound)
write_wav(sound, 'fade.wav')
