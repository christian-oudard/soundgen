#! /usr/bin/env python

from __future__ import division

import random
from pygame import mixer, time, sndarray
from math import sin
import numpy as np

mixer.init()
sndarray.use_arraytype('numpy')

_int16max = (2<<14) - 1

# utility #
def play(sound):
    """Play a sound and wait for it to finish."""
    sound.play()
    while mixer.get_busy():
        time.wait(10)

def nsamples(seconds):
    """
    Calculate the number of samples equal to the given number of seconds, based on the current sampling rate.
    """
    frequency, size, channels = mixer.get_init()
    return int(frequency * seconds)

def make_array(sound):
    return sndarray.array(sound)

def mono_array_to_sound(array):
    print(array.shape)
    array = np.clip(array, -1.0, +1.0) * _int16max
    # Mono sound, so copy the single channel to both left and right.

    array = np.array(zip(array, array))
    return sndarray.make_sound(array.astype(np.int16))

# generators #
def silence(length):
    return np.zeros(nsamples(length))

def white_noise(length):
    return np.random.normal(0, 1/4, nsamples(length))

def sinewave(length, freq):
    values = np.linspace(0, length * freq, num=nsamples(length))
    values = np.sin(2 * np.pi * values)
    return values

def squarewave(length, freq):
    values = np.linspace(0, length * freq * 2, num=nsamples(length))
    values = np.mod(values, 2)
    values = np.floor(values)
    values = values * 2 - 1
    return values

def sawtooth(length, freq):
    values = np.linspace(0, length * freq, num=nsamples(length))
    values = (np.mod(values, 1.0) - .5) * 2
    return values

def trianglewave(length, freq):
    f1 = squarewave(length, freq)
    f2 = sawtooth(length, freq)
    return (f2 * f1) * 2 - 1

if __name__ == '__main__':

    t = .5
    f = 440

    arrays = [
        silence(t),
        white_noise(t),
        sinewave(t, f),
        squarewave(t, f),
        trianglewave(t, f),
    ]
    sounds = [mono_array_to_sound(a) for a in arrays]
    for s in sounds:
        play(s)
