# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 22:00:43 2018

@author: Andrej Leban
"""

import itertools as it
import functools as ft
import collections as coll

import sortedcontainers as sc
from blist import blist

import matplotlib.pyplot as plt

import re

#re.search('@ (\d+),(\d+)', item).groups()))

def parseInput(inp):
    data = []
    with open(inp, 'r') as f:
        for line in f:
            data.append(line)

    return data


if __name__ == "__main__":
#    data = parseInput("input.txt")

#    init = '#..#.#..##......###...###'
    init = '##.######...#.##.#...#...##.####..###.#.##.#.##...##..#...##.#..##....##...........#.#.#..###.#'

#    rules = {'...##': '#',
#            '..#..': '#',
#            '.#...': '#',
#            '.#.#.': '#',
#            '.#.##': '#',
#            '.##..': '#',
#            '.####': '#',
#            '#.#.#': '#',
#            '#.###': '#',
#            '##.#.': '#',
#            '##.##': '#',
#            '###..': '#',
#            '###.#': '#',
#            '####.': '#'}

    rules = {'.###.':'#',
            '#.##.':'.',
            '.#.##':'#',
            '...##':'.',
            '###.#':'#',
            '##.##':'.',
            '.....':'.',
            '#..#.':'#',
            '..#..':'#',
            '#.###':'#',
            '##.#.':'.',
            '..#.#':'#',
            '#.#.#':'#',
            '.##.#':'#',
            '.#..#':'#',
            '#..##':'#',
            '##..#':'#',
            '#...#':'.',
            '...#.':'#',
            '#####':'.',
            '###..':'#',
            '#.#..':'.',
            '....#':'.',
            '.####':'#',
            '..###':'.',
            '..##.':'#',
            '.##..':'.',
            '#....':'.',
            '####.':'#',
            '.#.#.':'.',
            '.#...':'#',
            '##...':'#'}


    numgen = 1000

    siz = len(init)
    pad = numgen + 2
#    pad = 20

    state = "".join(["."]*pad) + init + "".join(["."]*pad)
    newstate = list(state)

    sums = []

    gen = 0
    while gen < numgen:
        for i in range(2, siz+2*pad-2):
#            changed = False
            for r, new in rules.items():
                if state[i-2:i+3] == r:
#                    print("matched", r, "at", i-2)
#                    state  = state[:i] + new + state[i+1:]
                    newstate[i] = new
#                    changed = True
                    break
#            if not changed:
#                newstate[i] = "."

#        if not gen % 1000000:
#            print(gen)
#        print(state, "\n")

        state = "".join(newstate)
        if state[2] == "#" or state[-2] == "#":
                pad += 2
                state = "".join(["."]*pad) + state + "".join(["."]*pad)
                newstate = list(state)

        s = 0
        for ind, c in enumerate(state):
            if c == "#":
                s += ind - pad
        print(s)
        sums.append(s)
        gen += 1

    final = "".join(newstate)

    plt.plot(sums)
#    print(final)
#    print(s)




##2###############
##    print("\n\n\n")
##    state = set()
#    state = sc.SortedList()
#
#    for ind, c in enumerate(init):
#        if c == "#":
#            state.add(ind)
#
##    print(state)
#
#    def interpret(ind, rule, res):
#        inc, exc = set(), set()
#
#        for i,c in enumerate(rule):
#            if c == "#":
#                inc.add(ind + i-2)
#            else:
#                exc.add(ind + i-2)
#
#        return inc, exc, res == "#"
#
#
##    for k, v in rules.items():
##        print(interpret(5, k,v))
#
#    #precalc rules
#    rulesP = []
#    for rule, res in rules.items():
#        rulesP.append(interpret(0, rule, res ))
#
#    gen = 0
#
#    globalShift = 0
#
#    while gen < numgen:
##        newstate = set(state)
#        deleted = sc.SortedList()
#        added = sc.SortedList()
#
#        #for each potted
##        for s in range(min(state)-2, max(state)+2):
#
#        #todo: apply to not in as well!
#        for ind, s in enumerate(state):
##            changed = False
##            for rule, res in rules.items():
##            stateShift = set(map(lambda x: x-s, state))
##            print(state)
#            for inc, exc, switch in rulesP:
##                inc, exc, switch = interpret(s, rule, res)
##                inc = set(map(lambda x: x+s, inc))
##                exc = set(map(lambda x: x+s, exc))
#
#                succ = True
#                if ind <= 1:
#                    pass
#                elif ind == len(state) - 2:
#                    pass
#                else:
#                    #check inclusive
#                    for ss in state[ind-1:ind+2]:
#                        #shift
#                        if ss-s not in inc:
#                            print(ss, ss-s, inc)
#                            succ = False
#                            break
#                    if len(inc) == 4 and succ:
#                        if (state[ind-2]-s) not in inc and (state[ind+2]-s) not in inc:
#                            succ = False
#                    if len(inc) == 5 and succ:
#                        if (state[ind-2]-s) not in inc or (state[ind+2]-s) not in inc:
#                            succ = False
#
#                    #check exl
#                    if succ:
#                        #first gap
#                        for ss in it.chain(range(state[ind-1]+1,s), range(s+1, state[ind+1])):
#                            if ss-s not in exc:
#                                print(ss, ss-s, inc)
#                                succ = False
#                                break
#                        #second gap
#                        if succ:
#                            for ss in it.chain(range(state[ind-2]+1, state[ind-1]),
#                                               range(state[ind+1]+, state[ind+1])):
#                                if ss-s not in exc:
#                                    print(ss, ss-s, inc)
#                                    succ = False
#                                    break
#                    #apply rule
#                    if succ:
#                        if not switch:
##                            state.pop(ind)
##                            state[ind] *= -1
#                            deleted.add(s)
#
#
##                if inc.issubset(stateShift) and (exc - stateShift == exc):
##                    print("matched", rule, "at", s)
##                    print(inc,exc, newstate)
##                    if not switch:
##                        if s in newstate:
##                            newstate.remove(s)
##                    else:
##                        newstate.add(s)
###                    changed = True
##                    break
#
##            if not changed:
##                if s in newstate:
##                    newstate.remove(s)
#
##FIXME
#        state = newstate
#        gen += 1
#        st = "".join(["."]*(max(state)-min(state)))
#        for s in state:
#            st = st[:s] + "#" + st[s+1:]
#        print(st)
#        print(state, "\n")
#
#    print(state)
#    print(sum(state))




