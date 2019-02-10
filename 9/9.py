# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 20:15:20 2018

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


def cwise(curr, n, lst):
    if curr is None:
        curr = 0
    if not len(lst):
        return 1
    return (curr + n) % len(lst)


def ccwise(curr, n, lst):
    if curr is None:
        curr = 0
    if not len(lst):
        return 1
    return (curr - n) % len(lst)

def solve(maxM, nplayers):

    data = [i for i in range(1, maxM+1)]

    cycle = blist([0])
    current = 0

    kept = [set() for i in range(nplayers)]
    elves = it.cycle(range(nplayers))
    elf = elves.__next__()

    for m in data:
#        print(cycle, cycle[current], current)

        #tie break
        if not m % 23:

            irem = ccwise(current, 7, cycle)
            rem = cycle.pop(irem)

            kept[elf].add(m)
            kept[elf].add(rem)

            current = irem
            elf = elves.__next__()
            continue

        i = cwise(current, 2, cycle)

        if len(cycle) == 1 and i == 0:
            cycle = cycle + [m]
            i = 1
        else:
            cycle.insert(i, m)

        current = i
        elf = elves.__next__()

    return kept


if __name__ == "__main__":

    maxM = 71628
    nplayers = 448

    kept = solve(maxM, nplayers)

    score = list(map(sum, kept))
    print(max(score))

    maxM = 7162800
    nplayers = 448

    kept = solve(maxM, nplayers)

    score = list(map(sum, kept))
    print(max(score))