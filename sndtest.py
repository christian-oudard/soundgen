#! /usr/bin/env python

from __future__ import division

import random
from pygame import mixer, time, sndarray
from math import sin
import numpy as np

mixer.init()
print 'init', mixer.get_init()
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

def make_sound(array):
    if len(array.shape) == 1:
        # Mono sound, copy the single channel to both left and right.
        array = np.array(zip(array, array))
    return sndarray.make_sound(array.astype(np.int16))

# generators #
def silence(length):
    return make_sound(np.zeros((nsamples(length), 2)))

def white_noise(length):
    values = np.random.normal(0, 1/4, (nsamples(length), 2))
    values = np.clip(values, -1.0, +1.0)
    values *= _int16max
    return make_sound(values)

def sinwave(length, freq):
    values = np.linspace(0, length * freq, num=nsamples(length))
    values = np.sin(2 * np.pi * values)
    values *= _int16max
    return make_sound(values)

def sawtooth(length, freq):
    values = np.linspace(0, length * freq, num=nsamples(length))
    values = (np.mod(values, 1.0) - .5) * 2
    values *= _int16max
    return make_sound(values)

# filters #
def echo(snd, period=.2, reps=4, decay=.5):
    snd = make_array(snd)

    sample_period = nsamples(period)
    shape = list(snd.shape)
    length = shape[0]
    shape[0] +=  sample_period * reps
    result = np.zeros(shape)

    for i in range(0, reps + 1):
        start = i * sample_period
        result[start: start + length] += snd
        snd *= decay

    return make_sound(result)

# mixers #
def mix(*args):
    return make_sound(sum(make_array(s) / len(args) for s in args))

def cat(*args):
    """
    Concatenate the given sounds.
    """
    arrays = [make_array(s) for s in args]
    return make_sound(np.concatenate(arrays))

if __name__ == '__main__':
    pass

    play(sinwave(.05, 880))

    t = .5
    f = 440

    play(silence(t))
    play(white_noise(t))
    play(sinwave(t, f))
    play(sawtooth(t, f))
