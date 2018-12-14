# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 05:47:28 2018

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


def mix(r1, r2):
#     return tuple(int(d) for d in str(r1+r2))
    s = r1+r2
    a = s//10
    b = s%10
    if a:
        return a,b
    else:
        return (b,)
#     return tuple(int(d) for d in str(r1+r2))

if __name__ == "__main__":

#    data = parseInput("input.txt")
    pass

    scoreboard = [3,7]
    nelves = 2
    elves=[(i,s) for s,i in zip(scoreboard, range(nelves))]

    n = 2
    after = 100000
    found = False
#    while len(scoreboard) < after+10:
#    compare = coll.deque([3,2,0,8,5,1])

#    compare = coll.deque([5,1,5,8,9])
#    compare = coll.deque([0,1,2,4,5])
#    compare = coll.deque([9,2,5,1,0])
    compare = coll.deque([5,9,4,1,4])
    lenS = len(compare)
    prev = lenS
    tally = coll.deque(scoreboard)

    while not found:
#        added = mix(*(elf[1] for elf in elves))
#        scoreboard.extend(added)
        scoreboard.extend(mix(*(elf[1] for elf in elves)))

#        newElves = []
        for i, elf in enumerate(elves):
#            cs = it.cycle(scoreboard)
            adv = 1 + elf[1]
#            pos = elf[0] # + nelves if (elf[0] >= len(scoreboard)) else 0
            newpos = (elf[0]+ adv) % len(scoreboard)
            elves[i] = (newpos,
                      scoreboard[newpos])
#            elves[i] = ((newpos + adv) % len(scoreboard),
#                      [i for i in it.islice(cs, newpos+adv, newpos+adv+1)][0])
#            newElves.append(newelf)

#        elves = newElves
#        print(scoreboard, elves)
        if len(scoreboard) < lenS:
            tally.extend(scoreboard[-nelves:])
        elif len(tally) < lenS:
            tally.append(scoreboard[prev-1])

        checked = 0
        for k in range(prev, len(scoreboard)):
            if tally == compare:
#            if scoreboard[i-5:i] == [5,9,4,1,4]:
                print(k-lenS)
                found = True
                break
            tally.append(scoreboard[k])
            if len(tally) > lenS:
                tally.popleft()
            checked += 1
#            if scoreboard[i-6:i] == [3,2,0,8,5,1]:

#        print(tally)
        n += 1
#        prev += len(added) if (len(scoreboard)>prev) else 0
        prev += checked

        if not n % 100000:
            print(n)

#print("".join(map(str, scoreboard[after:after+10])))

#2
#for i in range(10, len(scoreboard)):
#    if scoreboard[i-10:i] == [3,2,0,8,5,1]:
#        print(i-10)
#        break






