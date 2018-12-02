# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 17:37:13 2018

@author: Andrej Leban
"""

def parseInput(inp):
    data = []
    with open(inp, 'r') as f:
        for line in f:
            data.append(int(line))

    return data

def first(data):
    return sum(data)

def second(data):
    c = it.accumulate(it.cycle(data))
    seen = set()
    i = 0

    for el in c:
        i += 1
        if el in seen:
            return el, i
        else:
            seen.add(el)

