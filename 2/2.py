# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 18:21:05 2018

@author: Andrej Leban
"""


def parseInput(inp):
    data = []
    with open(inp, 'r') as f:
        for line in f:
            data.append(line)

    return data


def count(string, ret=None):
    if ret is None:
        ret = {}

    for c in string:
        try:
            ret[c] += 1
        except KeyError:
            ret[c] = 1
    return ret


def repeats(count):
    twos, threes = 0, 0
    for v in count.values():
        if v == 2:
            twos += 1
        elif v == 3:
            threes += 1

    return twos, threes


def checksum(data):
    run2, run3 = 0, 0
    for line in data:
        c = count(line)
        twos, threes = repeats(c)
        if twos:
            run2 += 1
        if threes:
            run3 += 1
    return run2 * run3


# second:

data = parseInput("input2.txt")

ll = list(map(list, data))

candidates = []

for i in range(0, len(ll)):
    for j in range(i, len(ll)):
        iN = list(map(ord, ll[i]))
        jN = list(map(ord, ll[j]))

        diff = list(map(lambda x, y: x - y, iN, jN))

        crit = len(list(filter(lambda x: x != 0, diff)))

        if crit == 1:
            print(i, j, diff)
            candidates.append(str(ll[i]))
            candidates.append(str(ll[j]))
