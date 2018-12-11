# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 22:11:00 2018

@author: Andrej Leban
"""

import itertools as it
import functools as ft
import collections as coll

import sortedcontainers as sc
from blist import blist

import re

#re.search('@ (\d+),(\d+)', item).groups()))

def parseInput(inp):
    data = []
    with open(inp, 'r') as f:
        for line in f:
            data.append(line)

    return data


def consecutive_ones(sequence):
    def _consecutives():
        for itr in it.repeat(iter(sequence)):
            yield tuple(it.takewhile(lambda p: p == 1,
                                     it.dropwhile(lambda p: p != 1, itr)))
    return it.takewhile(lambda t: len(t), _consecutives())

def sames(sequence):
    def _same():
        for itr in it.repeat(iter(sequence)):
            yield tuple(it.takewhile(lambda p: p == 1,
                                     it.dropwhile(lambda p: p != 1, itr)))
    return it.takewhile(lambda t: len(t), _same())



def powerLevel(x, y, serial):

    rackID = x + 10
    power = rackID *y
    power += serial
    power *= rackID
    power = int(str(power//100)[-1])
    power -= 5

    return power


if __name__ == "__main__":

#    data = parseInput("input.txt")
    serial = 6303
#    serial = 18

#    print(serial)

    plmat = np.zeros((300,300))

    for y in range(plmat.shape[0]):
        for x in range(plmat.shape[1]):
            plmat[y][x] = powerLevel(x, y, serial)

    # brute force
    plsummat = np.zeros((300,300))

    for y in range(1, plsummat.shape[0] - 1):
        for x in range(1, plsummat.shape[1] - 1):

            for i in range(-1, 2):
                for j in range(-1, 2):
                    plsummat[y][x] += plmat[y+i][x+j]


    maxy, maxx=  np.unravel_index(plsummat.argmax(), plsummat.shape)

    print(maxx-1, maxy-1, plsummat[maxy][maxx])















