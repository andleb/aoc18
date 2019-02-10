# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 05:56:06 2018

@author: Andrej Leban
"""

import re

import numpy as np

#offx, offy = tuple(map(int, re.search('@ (\d+),(\d+)', item).groups()))
#sizx, sizy = tuple(map(int, re.search(': (\d+)x(\d+)', item).groups()))


def parseInput(inp):
    data = []
    with open(inp, 'r') as f:
        for line in f:
            data.append(line)

    return data


if __name__ == "__main__":

    data = parseInput("input.txt")
    res = []

    for d in data:
        first = d.split("[")[1]

        timestamp = first.split("]")[0]
        timestamp2 = timestamp.split("-")[0:]
        year, month = tuple(map(int, timestamp2[:2]))
        day = int(timestamp2[2].split(" ")[0])
        hour, minute = tuple(map(int, timestamp2[2].split(" ")[1].split(":")))

        msg = first.split("]")[1]
#        print(timestamp2, msg)

        res.append(((year, month, day, hour, minute), msg))

        resS = sorted(res, key=lambda t: t[0])

        guardI = {}
        count = 0
        for line in resS:
            try:
                gid = int(re.search('Guard #(\d+)', line[1]).groups()[0])
                continue
            except AttributeError:
                if line[1] == ' falls asleep\n':
                    startm = line[0][-1]
                elif line[1] == ' wakes up\n':
                    try:
                        guardI[gid][startm:line[0][-1]] += 1
                    except KeyError:
                        guardI[gid] = np.zeros((60,))
                        guardI[gid][startm:line[0][-1]] = 1

    # most minutes
    kmax = ""
    vmax = 0
    for k, v in guardI.items():
#            print(k, v)
#            print(sum(v))
        if (np.sum(v)) > vmax:
            kmax, vmax = k, np.sum(v)

    print(kmax, vmax)
    print(kmax * np.argmax(guardI[kmax]))

    # most freq on same minute
    kmax = ""
    vmax = 0
    for k, v in guardI.items():
#            print(k, v)
#            print(max(v))
        if (max(v)) > vmax:
            kmax, vmax = k, max(v)

    print(kmax, vmax)
    print(kmax * np.argmax(guardI[kmax]))
