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

def make_sound(array):
    if len(array.shape) == 1:
        # Mono sound, copy the single channel to both left and right.
        array = np.array(zip(array, array))
    return sndarray.make_sound(array.astype(np.int16))

# generators #
def _make_generator(f):
    def generator(*args, **kwargs):
        return make_sound(np.clip(f(*args, **kwargs), -1.0, +1.0) * _int16max)
    return generator

def silence(length):
    return make_sound(np.zeros((nsamples(length), 2)))

def _white_noise(length):
    return np.random.normal(0, 1/4, (nsamples(length), 2))
white_noise = _make_generator(_white_noise)

def _sinewave(length, freq):
    values = np.linspace(0, length * freq, num=nsamples(length))
    values = np.sin(2 * np.pi * values)
    return values
sinewave = _make_generator(_sinewave)

def _squarewave(length, freq):
    values = np.linspace(0, length * freq * 2, num=nsamples(length))
    values = np.mod(values, 2)
    values = np.floor(values)
    values = values * 2 - 1
    return values
squarewave = _make_generator(_squarewave)

def _sawtooth(length, freq):
    values = np.linspace(0, length * freq, num=nsamples(length))
    values = (np.mod(values, 1.0) - .5) * 2
    return values
sawtooth = _make_generator(_sawtooth)

def _trianglewave(length, freq):
    f1 = _squarewave(length, freq)
    f2 = _sawtooth(length, freq)
    return (f2 * f1) * 2 - 1
trianglewave = _make_generator(_trianglewave)

def _pulsewave(length, freq, width=.25):
    values = _sawtooth(length, freq)
    values = values - (1 - width * 2)
    values = np.clip(values, -1.0, +1.0)
    values = np.floor(values)
    values = values * 2 + 1
    return values
pulsewave = _make_generator(_pulsewave)

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

    play(sinewave(.05, 880))

    t = .5
    f = 440

    play(silence(t))
    play(white_noise(t))
    play(sinewave(t, f))
    play(squarewave(t, f))
    play(sawtooth(t, f))
    play(trianglewave(t, f))
    play(pulsewave(t, f, .10))
    play(pulsewave(t, f, .25))
    play(pulsewave(t, f, .40))
