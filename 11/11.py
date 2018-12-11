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
#    serial = 18
#    serial = 42
    serial = 6303

#    print(serial)

    plmat = np.zeros((300,300))

    for y in range(plmat.shape[0]):
        for x in range(plmat.shape[1]):
            plmat[y][x] = powerLevel(x+1, y+1, serial)

    # brute force
    plsummat = np.zeros((300,300))

    for y in range(1, plsummat.shape[0] - 1):
        for x in range(1, plsummat.shape[1] - 1):

            for i in range(-1, 2):
                for j in range(-1, 2):
                    plsummat[y][x] += plmat[y+i][x+j]


    maxy, maxx=  np.unravel_index(plsummat.argmax(), plsummat.shape)

    print(maxx-1, maxy-1, plsummat[maxy][maxx])



    #part2

    known  = {}

    for siz in range(1,300):
        plsummat = np.zeros((300,300))

        if not siz % 3:
            prev = known[siz//3][3]

            for y in range(0, plsummat.shape[0] - siz + 1):
                for x in range(0, plsummat.shape[1] - siz + 1):

                    plsummat[y][x] = prev[y][x] + prev[y][x+1] +prev[y][x+2]\
                        + prev[y+1][x] + prev[y+1][x+1] + prev[y+1][x+2]\
                        + prev[y+2][x] + prev[y+2][x+1] + prev[y+2][x+2]

            maxy, maxx=  np.unravel_index(plsummat.argmax(), plsummat.shape)
            known[siz] = (maxx, maxy, plsummat[maxy][maxx], plsummat)

        elif not siz % 2:
            prev = known[siz//2][3]

            for y in range(0, plsummat.shape[0] - siz + 1 ):
                for x in range(0, plsummat.shape[1] - siz + 1):

                    plsummat[y][x] = prev[y][x] + prev[y+1][x] +prev[y][x+1]\
                        + prev[y+1][x+1]

            maxy, maxx=  np.unravel_index(plsummat.argmax(), plsummat.shape)
            known[siz] = (maxx, maxy, plsummat[maxy][maxx], plsummat)
        else:

            for y in range(0, plsummat.shape[0] - siz + 1):
                for x in range(0, plsummat.shape[1] - siz + 1):

                    for i in range(0, siz):
                        for j in range(0, siz):
                            plsummat[y][x] += plmat[y+i][x+j]

            maxy, maxx=  np.unravel_index(plsummat.argmax(), plsummat.shape)
            known[siz] = (maxx, maxy, plsummat[maxy][maxx], plsummat)

        print(siz, maxx, maxy, plsummat[maxy][maxx])


    maxsiz = 0
    maxp = -1
    for k, v in known.items():
        print(k, v[:3])
        if v[2] >= maxp:
            maxp = v[2]
            maxsix = k












