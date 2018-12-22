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


#def buildGraphsold(types, source):
#
#    #undirected, weights are 1 or 8
#    graphTR = {source: {}}
#    graphCL = {source: {}}
#    graphNone = {source: {}}
#
##    sources = coll.deque()
##    print(source)
#
#
#    for i in range(types.shape[0]):
#        for j in range(types.shape[1]):
#            node = (i, j)
##            print(i,j, graphTR, graphCL, graphNone)
#
#            # rocky - tr & cl
#            if types[i,j] == 0:
#                try:
#                    graphTR[node]
#                except KeyError:
#                    graphTR[node] = {}
#                try:
#                    graphCL[node]
#                except KeyError:
#                    graphCL[node] = {}
#
#                for (k,l) in [(0,-1), (0,1), (-1,0), (1,0)]:
#                    neigh = (min(max(node[0]+k, 0), types.shape[0] -1),
#                             min(max(node[1]+l, 0), types.shape[1]-1))
#                    if neigh == node:
#                        continue
#
#                    #wet
#                    if types[neigh] == 1:
#                        try:
#                            graphCL[node][neigh]
#                        except KeyError:
#                            graphCL[node][neigh] = 1
#                        try:
#                            graphCL[neigh]
#                        except KeyError:
#                            graphCL[neigh] = {}
#                        try:
#                            graphCL[neigh][node]
#                        except KeyError:
#                            graphCL[neigh][node] = 1
#
#                        try:
#                            graphTR[node][neigh]
#                        except KeyError:
#                            graphTR[node][neigh] = 8
#                        try:
#                            graphTR[neigh]
#                        except KeyError:
#                            graphTR[neigh] = {}
#                        try:
#                            graphTR[neigh][node]
#                        except KeyError:
#                            graphTR[neigh][node] = 8
#
#                    #narrow
#                    if types[neigh] == 2:
#                        try:
#                            graphCL[node][neigh]
#                        except KeyError:
#                            graphCL[node][neigh] = 8
#                        try:
#                            graphCL[neigh]
#                        except KeyError:
#                            graphCL[neigh] = {}
#                        try:
#                            graphCL[neigh][node]
#                        except KeyError:
#                            graphCL[neigh][node] = 8
#
#                        try:
#                            graphTR[node][neigh]
#                        except KeyError:
#                            graphTR[node][neigh] = 1
#                        try:
#                            graphTR[neigh]
#                        except KeyError:
#                            graphTR[neigh] = {}
#                        try:
#                            graphTR[neigh][node]
#                        except KeyError:
#                            graphTR[neigh][node] = 1
#
#                    #rocky again
#                    else:
#                        try:
#                            graphCL[node][neigh]
#                        except KeyError:
#                            graphCL[node][neigh] = 1
#                        try:
#                            graphCL[neigh]
#                        except KeyError:
#                            graphCL[neigh] = {}
#                        try:
#                            graphCL[neigh][node]
#                        except KeyError:
#                            graphCL[neigh][node] = 1
#
#                        try:
#                            graphTR[node][neigh]
#                        except KeyError:
#                            graphTR[node][neigh] = 1
#                        try:
#                            graphTR[neigh]
#                        except KeyError:
#                            graphTR[neigh] = {}
#                        try:
#                            graphTR[neigh][node]
#                        except KeyError:
#                            graphTR[neigh][node] = 1
#
#
#            # wet - cl & none
#            if types[i,j] == 1:
#                try:
#                    graphCL[node]
#                except KeyError:
#                    graphCL[node] = {}
#                try:
#                    graphNone[node]
#                except KeyError:
#                    graphNone[node] = {}
#
#                for (k,l) in [(0,-1), (0,1), (-1,0), (1,0)]:
#                    neigh = (min(max(node[0]+k, 0), types.shape[0] -1),
#                             min(max(node[1]+l, 0), types.shape[1]-1))
#                    if neigh == node:
#                        continue
#
#                    #rocky
#                    if types[neigh] == 0:
#                        try:
#                            graphCL[node][neigh]
#                        except KeyError:
#                            graphCL[node][neigh] = 1
#                        try:
#                            graphCL[neigh]
#                        except KeyError:
#                            graphCL[neigh] = {}
#                        try:
#                            graphCL[neigh][node]
#                        except KeyError:
#                            graphCL[neigh][node] = 1
#
#                        try:
#                            graphNone[node][neigh]
#                        except KeyError:
#                            graphNone[node][neigh] = 8
#                        try:
#                            graphNone[neigh]
#                        except KeyError:
#                            graphNone[neigh] = {}
#                        try:
#                            graphNone[neigh][node]
#                        except KeyError:
#                            graphNone[neigh][node] = 8
#
#                    #narrow
#                    if types[neigh] == 2:
#                        try:
#                            graphCL[node][neigh]
#                        except KeyError:
#                            graphCL[node][neigh] = 8
#                        try:
#                            graphCL[neigh]
#                        except KeyError:
#                            graphCL[neigh] = {}
#                        try:
#                            graphCL[neigh][node]
#                        except KeyError:
#                            graphCL[neigh][node] = 8
#
#                        try:
#                            graphNone[node][neigh]
#                        except KeyError:
#                            graphNone[node][neigh] = 1
#                        try:
#                            graphNone[neigh]
#                        except KeyError:
#                            graphNone[neigh] = {}
#                        try:
#                            graphNone[neigh][node]
#                        except KeyError:
#                            graphNone[neigh][node] = 1
#
#                    #wet again
#                    else:
#                        try:
#                            graphCL[node][neigh]
#                        except KeyError:
#                            graphCL[node][neigh] = 1
#                        try:
#                            graphCL[neigh]
#                        except KeyError:
#                            graphCL[neigh] = {}
#                        try:
#                            graphCL[neigh][node]
#                        except KeyError:
#                            graphCL[neigh][node] = 1
#
#                        try:
#                            graphNone[node][neigh]
#                        except KeyError:
#                            graphNone[node][neigh] = 1
#                        try:
#                            graphNone[neigh]
#                        except KeyError:
#                            graphNone[neigh] = {}
#                        try:
#                            graphNone[neigh][node]
#                        except KeyError:
#                            graphNone[neigh][node] = 1
#
#            # narrow - torch & none
#            if types[i,j] == 2:
#                try:
#                    graphTR[node]
#                except KeyError:
#                    graphTR[node] = {}
#                try:
#                    graphNone[node]
#                except KeyError:
#                    graphNone[node] = {}
#
#                for (k,l) in [(0,-1), (0,1), (-1,0), (1,0)]:
#                    neigh = (min(max(node[0]+k, 0), types.shape[0]-1),
#                             min(max(node[1]+l, 0), types.shape[1]-1))
#                    if neigh == node:
#                        continue
#
#                    #rocky
#                    if types[neigh] == 0:
#                        try:
#                            graphTR[node][neigh]
#                        except KeyError:
#                            graphTR[node][neigh] = 1
#                        try:
#                            graphTR[neigh]
#                        except KeyError:
#                            graphTR[neigh] = {}
#                        try:
#                            graphTR[neigh][node]
#                        except KeyError:
#                            graphTR[neigh][node] = 1
#
#                        try:
#                            graphNone[node][neigh]
#                        except KeyError:
#                            graphNone[node][neigh] = 8
#                        try:
#                            graphNone[neigh]
#                        except KeyError:
#                            graphNone[neigh] = {}
#                        try:
#                            graphNone[neigh][node]
#                        except KeyError:
#                            graphNone[neigh][node] = 8
#
#                    #wet
#                    if types[neigh] == 1:
#                        try:
#                            graphTR[node][neigh]
#                        except KeyError:
#                            graphTR[node][neigh] = 8
#                        try:
#                            graphTR[neigh]
#                        except KeyError:
#                            graphTR[neigh] = {}
#                        try:
#                            graphTR[neigh][node]
#                        except KeyError:
#                            graphTR[neigh][node] = 8
#
#                        try:
#                            graphNone[node][neigh]
#                        except KeyError:
#                            graphNone[node][neigh] = 1
#                        try:
#                            graphNone[neigh]
#                        except KeyError:
#                            graphNone[neigh] = {}
#                        try:
#                            graphNone[neigh][node]
#                        except KeyError:
#                            graphNone[neigh][node] = 1
#
#                    #narrow again
#                    else:
#                        try:
#                            graphTR[node][neigh]
#                        except KeyError:
#                            graphTR[node][neigh] = 1
#                        try:
#                            graphTR[neigh]
#                        except KeyError:
#                            graphTR[neigh] = {}
#                        try:
#                            graphTR[neigh][node]
#                        except KeyError:
#                            graphTR[neigh][node] = 1
#
#                        try:
#                            graphNone[node][neigh]
#                        except KeyError:
#                            graphNone[node][neigh] = 1
#                        try:
#                            graphNone[neigh]
#                        except KeyError:
#                            graphNone[neigh] = {}
#                        try:
#                            graphNone[neigh][node]
#                        except KeyError:
#                            graphNone[neigh][node] = 1
#
#    return graphTR, graphCL, graphNone




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


def printGrid(grid, mouth, target):

    res = np.chararray(grid.shape, itemsize=1, unicode=True)
    res[grid==0] = '.'
    res[grid==1] = '='
    res[grid==2] = '|'

    res[mouth] = 'M'
    res[target] = 'T'

    print(res)
    return res


def buildGraphs(types, source):

    #undirected, weights are 1 or 8
    graphTR = {}
    graphCL = {}
    graphNone = {}

    graphs = ((graphCL, graphTR), (graphCL, graphNone), (graphTR, graphNone))
    neighs = ((1,2), (0,2), (0,1))

    for i in range(types.shape[0]):
        for j in range(types.shape[1]):
            node = (i, j)
#            print(i,j, graphTR, graphCL, graphNone)
#            print(i,j)

            tp = types[i,j]
            graph1 = graphs[tp][0]
            graph2 = graphs[tp][1]

#            # rocky - tr & cl
#            if types[i,j] == 0:
            try:
                graph1[node]
            except KeyError:
                graph1[node] = {}
            try:
                graph2[node]
            except KeyError:
                graph2[node] = {}

            for (k,l) in [(0,-1), (0,1), (-1,0), (1,0)]:
                neigh = (min(max(node[0]+k, 0), types.shape[0] -1),
                         min(max(node[1]+l, 0), types.shape[1]-1))
                if neigh == node:
                    continue

                if types[neigh] == neighs[tp][0]:
                    try:
                        graph1[node][neigh]
                    except KeyError:
                        graph1[node][neigh] = 1

                    try:
                        graph2[node][neigh]
                    except KeyError:
                        graph2[node][neigh] = 8

                if types[neigh] == neighs[tp][1]:
                    try:
                        graph1[node][neigh]
                    except KeyError:
                        graph1[node][neigh] = 8

                    try:
                        graph2[node][neigh]
                    except KeyError:
                        graph2[node][neigh] = 1

                else:
                    try:
                        graph1[node][neigh]
                    except KeyError:
                        graph1[node][neigh] = 1

                    try:
                        graph2[node][neigh]
                    except KeyError:
                        graph2[node][neigh] = 1


    return graphTR, graphCL, graphNone

terr2eq =\
    {
     (0,1) : 1,
     (0,2) : 0,
     (1,0) : 1,
     (1,2) : 2,
     (2,0) : 0,
     (2,1) : 2,
        }

def algo(types, graphs, eqstart, start, goal):

    startel = (start, [(start, eqstart, 0)])

#    if start == goal:
#        return [startel]
                                                        # sort on last running dist in path aka D[el]
    queue = sc.SortedKeyList([startel], key= lambda el: el[1][-1][2])
    # dont visit nodes twice
    inQ = {start}
    # queue: node, eq, totpath
    #path el: (node, eq, running dist)

    D = {} # dictionary of final distances
    P = {} # dictionary of predecessors
    D[start] = 0
    P[start] = None

    while queue:

        current, path = queue.pop(0)
        inQ.remove(current)
        eq = path[-1][1]

        if current == goal:
            break

        #change graph to present equipment
        graph = graphs[eq]

        for neighbor in graph[current]:
            # change of eq?
            if types[current] == types[neighbor] :
                neweq = eq
            else:
                neweq = terr2eq[(types[current], types[neighbor])]

            try:
                D[neighbor]
            except KeyError:
                D[neighbor] = int(1e32)

            if D[neighbor] > D[current] + graph[current][neighbor]:
                D[neighbor] = D[current] + graph[current][neighbor]
                if D[neighbor] <= 0:
                    raise RuntimeError

                P[neighbor] = (current, path[:])

                newel = (neighbor, path[:] + [(neighbor, neweq, D[neighbor])])
                if neighbor not in inQ:
                    queue.add(newel)
                    inQ.add(neighbor)

    return D, P


if __name__ == "__main__":

    factor = 8

    depth = 3198
    start = (0,0)
    target = (757, 12)

    # scratchpad for geo & erosion
    # geo on the boundaries

    temp = np.ones((factor*target[0]+1, factor*target[1]+1), dtype=int) * -1

    #precalculate erosion
    temp[0,:] = (16807 * np.arange(0,temp.shape[1]) + depth) % 20183
    temp[:,0] = (7905 * np.arange(0,temp.shape[0]) + depth) % 20183
    temp[0,0] = depth % 20183
    temp[target] = depth % 20183

#    #1st pass
    for i in range(1, temp.shape[0]):
        for j in range(1, temp.shape[1]):

            if (i,j) == target:
                continue
            temp[i, j] = temp[i-1, j]
            temp[i, j] *= temp[i, j-1]
            temp[i, j] = (temp[i,j] + depth) % 20183

    temp[target] = depth

#    print('\n')
#    print(temp)

    types = np.vectorize(ttype)(temp)

#    res = printGrid(types, (0,0), target)
#    data = [\
#            'M=.|=.|.|=.|=|=.',
#            '.|=|=|||..|.=...',
#            '.==|....||=..|==',
#            '=.|....|.==.|==.',
#            '=|..==...=.|==..',
#            '=||.=.=||=|=..|=',
#            '|.=.===|||..=..|',
#            '|..==||=.|==|===',
#            '.=..===..=|.|||.',
#            '.======|||=|=.|=',
#            '.===|=|===T===||',
#            '=|||...|==..|=.|',
#            '=.=|=.=..=.||==|',
#            '||=|=...|==.=|==',
#            '|=.=||===.|||===',
#            '||.|==.|.|.||=||']
#    ar = np.array(list(map(list, data)))
#    print('\n', np.all(ar == res[:ar.shape[0], :ar.shape[1]]))

    #risk level
    risk = np.sum(types[:target[0]+1, :target[1]+1])
    print('\n')
    print(risk)


# part two
    graphTR, graphCL, graphNone = buildGraphs(types, source=(0,0))

    D, P = algo(types, [graphTR, graphCL, graphNone], eqstart=0, start=start,
                goal=target)

    print(P[target][-1][-1][-1] + 1 - 7)




