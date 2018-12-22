# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 06:00:33 2018

@author: Andrej Leban
"""

import copy
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


def printGrid(grid, mouth, target):

    res = np.chararray(grid.shape, itemsize=1, unicode=True)
    res[grid==0] = '.'
    res[grid==1] = '='
    res[grid==2] = '|'

    res[mouth] = 'M'
    res[target] = 'T'

    print(res)
    return res


def geoIndex(y, x, erosionData, target):
    if y == 0 and x == 0:
        return 0
    elif y == target[0] and x == target[1]:
        return 0
    elif y == 0:
        return x * 16807
    elif x == 0:
        return y * 48271
    else:
        return erosionData[y-1][x] * erosionData[y][x-1]


def erosion(y, x, geoIndexData, depth):
    elevel = (geoIndexData[y][x] + depth) % 20183
    return elevel


#def ttype(y,x, erosion):
#    elevel = erosion[y][x]
#    if elevel % 3 == 0:
#        #   rocky
#        return 0
#    elif elevel % 3 == 1:
#        #wet
#        return 1
#    else:
#        #narrow
#        return 2
#

def ttype(elevel):
    if elevel % 3 == 0:
        #   rocky
        return 0
    elif elevel % 3 == 1:
        #wet
        return 1
    else:
        #narrow
        return 2


def buildGraphs(types, source):

    #undirected, weights are 1 or 8
    graphTR = {source: {}}
    graphCL = {source: {}}
    graphNone = {source: {}}

#    sources = coll.deque()
#    print(source)

    for i in range(types.shape[0]):
        for j in range(types.shape[1]):
            node = (i, j)
#            print(i,j, graphTR, graphCL, graphNone)

            # rocky - tr & cl
            if types[i,j] == 0:
                try:
                    graphTR[node]
                except KeyError:
                    graphTR[node] = {}
                try:
                    graphCL[node]
                except KeyError:
                    graphCL[node] = {}

                for (k,l) in [(0,-1), (0,1), (-1,0), (1,0)]:
                    neigh = (min(max(node[0]+k, 0), types.shape[0] -1),
                             min(max(node[1]+l, 0), types.shape[1]-1))
                    if neigh == node:
                        continue

                    #wet
                    if types[neigh] == 1:
                        try:
                            graphCL[node][neigh]
                        except KeyError:
                            graphCL[node][neigh] = 1
                        try:
                            graphCL[neigh]
                        except KeyError:
                            graphCL[neigh] = {}
                        try:
                            graphCL[neigh][node]
                        except KeyError:
                            graphCL[neigh][node] = 1

                        try:
                            graphTR[node][neigh]
                        except KeyError:
                            graphTR[node][neigh] = 8
                        try:
                            graphTR[neigh]
                        except KeyError:
                            graphTR[neigh] = {}
                        try:
                            graphTR[neigh][node]
                        except KeyError:
                            graphTR[neigh][node] = 8

                    #narrow
                    if types[neigh] == 2:
                        try:
                            graphCL[node][neigh]
                        except KeyError:
                            graphCL[node][neigh] = 8
                        try:
                            graphCL[neigh]
                        except KeyError:
                            graphCL[neigh] = {}
                        try:
                            graphCL[neigh][node]
                        except KeyError:
                            graphCL[neigh][node] = 8

                        try:
                            graphTR[node][neigh]
                        except KeyError:
                            graphTR[node][neigh] = 1
                        try:
                            graphTR[neigh]
                        except KeyError:
                            graphTR[neigh] = {}
                        try:
                            graphTR[neigh][node]
                        except KeyError:
                            graphTR[neigh][node] = 1

                    #rocky again
                    else:
                        try:
                            graphCL[node][neigh]
                        except KeyError:
                            graphCL[node][neigh] = 1
                        try:
                            graphCL[neigh]
                        except KeyError:
                            graphCL[neigh] = {}
                        try:
                            graphCL[neigh][node]
                        except KeyError:
                            graphCL[neigh][node] = 1

                        try:
                            graphTR[node][neigh]
                        except KeyError:
                            graphTR[node][neigh] = 1
                        try:
                            graphTR[neigh]
                        except KeyError:
                            graphTR[neigh] = {}
                        try:
                            graphTR[neigh][node]
                        except KeyError:
                            graphTR[neigh][node] = 1


            # wet - cl & none
            if types[i,j] == 1:
                try:
                    graphCL[node]
                except KeyError:
                    graphCL[node] = {}
                try:
                    graphNone[node]
                except KeyError:
                    graphNone[node] = {}

                for (k,l) in [(0,-1), (0,1), (-1,0), (1,0)]:
                    neigh = (min(max(node[0]+k, 0), types.shape[0] -1),
                             min(max(node[1]+l, 0), types.shape[1]-1))
                    if neigh == node:
                        continue

                    #rocky
                    if types[neigh] == 0:
                        try:
                            graphCL[node][neigh]
                        except KeyError:
                            graphCL[node][neigh] = 1
                        try:
                            graphCL[neigh]
                        except KeyError:
                            graphCL[neigh] = {}
                        try:
                            graphCL[neigh][node]
                        except KeyError:
                            graphCL[neigh][node] = 1

                        try:
                            graphNone[node][neigh]
                        except KeyError:
                            graphNone[node][neigh] = 8
                        try:
                            graphNone[neigh]
                        except KeyError:
                            graphNone[neigh] = {}
                        try:
                            graphNone[neigh][node]
                        except KeyError:
                            graphNone[neigh][node] = 8

                    #narrow
                    if types[neigh] == 2:
                        try:
                            graphCL[node][neigh]
                        except KeyError:
                            graphCL[node][neigh] = 8
                        try:
                            graphCL[neigh]
                        except KeyError:
                            graphCL[neigh] = {}
                        try:
                            graphCL[neigh][node]
                        except KeyError:
                            graphCL[neigh][node] = 8

                        try:
                            graphNone[node][neigh]
                        except KeyError:
                            graphNone[node][neigh] = 1
                        try:
                            graphNone[neigh]
                        except KeyError:
                            graphNone[neigh] = {}
                        try:
                            graphNone[neigh][node]
                        except KeyError:
                            graphNone[neigh][node] = 1

                    #wet again
                    else:
                        try:
                            graphCL[node][neigh]
                        except KeyError:
                            graphCL[node][neigh] = 1
                        try:
                            graphCL[neigh]
                        except KeyError:
                            graphCL[neigh] = {}
                        try:
                            graphCL[neigh][node]
                        except KeyError:
                            graphCL[neigh][node] = 1

                        try:
                            graphNone[node][neigh]
                        except KeyError:
                            graphNone[node][neigh] = 1
                        try:
                            graphNone[neigh]
                        except KeyError:
                            graphNone[neigh] = {}
                        try:
                            graphNone[neigh][node]
                        except KeyError:
                            graphNone[neigh][node] = 1

            # narrow - torch & none
            if types[i,j] == 2:
                try:
                    graphTR[node]
                except KeyError:
                    graphTR[node] = {}
                try:
                    graphNone[node]
                except KeyError:
                    graphNone[node] = {}

                for (k,l) in [(0,-1), (0,1), (-1,0), (1,0)]:
                    neigh = (min(max(node[0]+k, 0), types.shape[0]-1),
                             min(max(node[1]+l, 0), types.shape[1]-1))
                    if neigh == node:
                        continue

                    #rocky
                    if types[neigh] == 0:
                        try:
                            graphTR[node][neigh]
                        except KeyError:
                            graphTR[node][neigh] = 1
                        try:
                            graphTR[neigh]
                        except KeyError:
                            graphTR[neigh] = {}
                        try:
                            graphTR[neigh][node]
                        except KeyError:
                            graphTR[neigh][node] = 1

                        try:
                            graphNone[node][neigh]
                        except KeyError:
                            graphNone[node][neigh] = 8
                        try:
                            graphNone[neigh]
                        except KeyError:
                            graphNone[neigh] = {}
                        try:
                            graphNone[neigh][node]
                        except KeyError:
                            graphNone[neigh][node] = 8

                    #wet
                    if types[neigh] == 1:
                        try:
                            graphTR[node][neigh]
                        except KeyError:
                            graphTR[node][neigh] = 8
                        try:
                            graphTR[neigh]
                        except KeyError:
                            graphTR[neigh] = {}
                        try:
                            graphTR[neigh][node]
                        except KeyError:
                            graphTR[neigh][node] = 8

                        try:
                            graphNone[node][neigh]
                        except KeyError:
                            graphNone[node][neigh] = 1
                        try:
                            graphNone[neigh]
                        except KeyError:
                            graphNone[neigh] = {}
                        try:
                            graphNone[neigh][node]
                        except KeyError:
                            graphNone[neigh][node] = 1

                    #narrow again
                    else:
                        try:
                            graphTR[node][neigh]
                        except KeyError:
                            graphTR[node][neigh] = 1
                        try:
                            graphTR[neigh]
                        except KeyError:
                            graphTR[neigh] = {}
                        try:
                            graphTR[neigh][node]
                        except KeyError:
                            graphTR[neigh][node] = 1

                        try:
                            graphNone[node][neigh]
                        except KeyError:
                            graphNone[node][neigh] = 1
                        try:
                            graphNone[neigh]
                        except KeyError:
                            graphNone[neigh] = {}
                        try:
                            graphNone[neigh][node]
                        except KeyError:
                            graphNone[neigh][node] = 1

    return graphTR, graphCL, graphNone


def bfs(graph, start, goal):

    if start == goal:
        return [start]
    visited = {start}
    queue = deque([(start, [])])

    while queue:
        current, path = queue.popleft()
        visited.add(current)

        for neighbor in graph[current]:
            if neighbor == goal:
                return path + [current, neighbor]
            if neighbor in visited:
                continue

            queue.append((neighbor, path + [current]))
            visited.add(neighbor)

    return None


if __name__ == "__main__":

    depth = 510
    target = (10, 10)

#    grid = np.zeros((2*target[0], 2*target[1]))


#    depth = 3198
#    target = (757, 12)

    # scratchpad for geo & erosion
    # geo on the boundaries

    temp = np.ones((2*target[0]+1, 2*target[1]+1), dtype=int) * -1
#    temp[0,:] = 16807 * np.arange(0,temp.shape[1])
#    temp[:,0] = 48271 * np.arange(0,temp.shape[0])
#    temp[0,0] = 0
#    temp[target] = 0

    #precalculate erosion
    temp[0,:] = (16807 * np.arange(0,temp.shape[1]) + depth) % 20183
    temp[:,0] = (7905 * np.arange(0,temp.shape[0]) + depth) % 20183
    temp[0,0] = depth % 20183
    temp[target] = depth % 20183


    #calculate erosion on the boundaries
#    ero1 = lambda g: (g + depth) % 20183
#    erov = np.vectorize(ero1)
#
#    temp[1:target[0], 0] = erov(temp[1:target[0], 0])
#    temp[0, 1:target[1]] = erov(temp[0, 1:target[1]])
#    temp[0,0] = erov(temp[0,0])
#    temp[target] = erov(temp[target])

#    #1st pass geo index - ero -1, -1
    for i in range(1, temp.shape[0]):
#    for i in range(1, 2):
        for j in range(1, temp.shape[1]):

            if (i,j) == target:
                continue

#            temp[i, j] = ((255 * (2+31*i)) % 20183)
#            temp[i, j] *= ((510 + (16807*j)) % 20183)
#            temp[i, j] = (temp[i,j] + 510) % 20183

            temp[i, j] = temp[i-1, j]
            temp[i, j] *= temp[i, j-1]
            temp[i, j] = (temp[i,j] + depth) % 20183

    temp[target] = 510

    print('\n')
    print(temp)
    types = np.vectorize(ttype)(temp)
    res = printGrid(types, (0,0), target)

    data = [\
            'M=.|=.|.|=.|=|=.',
            '.|=|=|||..|.=...',
            '.==|....||=..|==',
            '=.|....|.==.|==.',
            '=|..==...=.|==..',
            '=||.=.=||=|=..|=',
            '|.=.===|||..=..|',
            '|..==||=.|==|===',
            '.=..===..=|.|||.',
            '.======|||=|=.|=',
            '.===|=|===T===||',
            '=|||...|==..|=.|',
            '=.=|=.=..=.||==|',
            '||=|=...|==.=|==',
            '|=.=||===.|||===',
            '||.|==.|.|.||=||']
    ar = np.array(list(map(list, data)))
    print('\n', np.all(ar == res[:ar.shape[0], :ar.shape[1]]))

    #risk level
    risk = np.sum(types)
    print('\n', risk)



# part two
    graphTR, graphCL, graphNone = buildGraphs(types, source=(0,0))

