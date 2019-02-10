# -*- coding: utf-8 -*-
"""
Created on Mon Dec 3 05:36:23 2018

@author: Andrej Leban
"""

import re


def parseInput(inp):
    data = []
    with open(inp, 'r') as f:
        for line in f:
            data.append(line)

    return data


def color(data):
    items = []
    fabric = {}

    for item in data:
        itId = re.search('#\d+', item)[0]
        offx, offy = tuple(map(int, re.search('@ (\d+),(\d+)', item).groups()))
        sizx, sizy = tuple(map(int, re.search(': (\d+)x(\d+)', item).groups()))

        items.append((itId, offx, offy, sizx, sizy))
#        print(items[-1])

        for x in range(sizx):
            for y in range(sizy):
                try:
                    fabric[(x + offx, y+offy)] += 1
                except KeyError:
                    fabric[(x+offx, y+offy)] = 1

    return fabric, items


def sol(fabric):
    return len(list(filter(lambda x: x >= 2, fabric.values())))


def intact(items, fabric):
    candidates = []

    for item in items:
#        print(item)
        fail = False
        itId, offx, offy, sizx, sizy = item

        for x in range(sizx):
            if fail:
                break
            for y in range(sizy):
                val = fabric[(x + offx, y+offy)]
                if val != 1:
                    fail = True
                    break
        if not fail:
            candidates.append(item)

    return candidates


if __name__ == "__main__":

    data = parseInput("input.txt")

    color(data)

    fabric, items = color(data)

    print(sol(fabric))

    print(intact(items, fabric))
