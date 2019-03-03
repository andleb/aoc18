# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 06:00:33 2018

@author: Andrej Leban
"""

import sortedcontainers as sc
import numpy as np


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


def ttype(elevel):
    if elevel % 3 == 0:
        # rocky
        return 0
    elif elevel % 3 == 1:
        # wet
        return 1
    else:
        # narrow
        return 2


def printGrid(grid, mouth, target):

    res = np.chararray(grid.shape, itemsize=1, unicode=True)
    res[grid == 0] = '.'
    res[grid == 1] = '='
    res[grid == 2] = '|'

    res[mouth] = 'M'
    res[target] = 'T'

    print(res)
    return res


def buildGraphs(types, source):

    # undirected, weights are 1 or 8
    graphTR = {}
    graphCL = {}
    graphNone = {}

    graphs = ((graphCL, graphTR), (graphCL, graphNone), (graphTR, graphNone))
    neighs = ((1,2), (0,2), (0,1))

    for i in range(types.shape[0]):
        for j in range(types.shape[1]):
            node = (i, j)

            tp = types[i,j]
            graph1 = graphs[tp][0]
            graph2 = graphs[tp][1]

#            # rocky - tr & cl
            try:
                graph1[node]
            except KeyError:
                graph1[node] = {}
            try:
                graph2[node]
            except KeyError:
                graph2[node] = {}

            for (k, l) in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                neigh = (min(max(node[0] + k, 0), types.shape[0] - 1),
                         min(max(node[1] + l, 0), types.shape[1] - 1))
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
     (0, 1): 1,
     (0, 2): 0,
     (1, 0): 1,
     (1, 2): 2,
     (2, 0): 0,
     (2, 1): 2,
     }


def algo(types, graphs, eqstart, start, goal):
    """
    Models equipment change as changing the underlying graph
    """

    startel = (start, [(start, eqstart, 0)])
                                                        # sort on last running dist in path aka D[el]
    queue = sc.SortedKeyList([startel], key=lambda el: el[1][-1][2])
    # dont visit nodes twice
    inQ = {start}

    D = {}  # dictionary of final distances
    P = {}  # dictionary of predecessors
    D[start] = 0
    P[start] = None

    while queue:

        current, path = queue.pop(0)
        inQ.remove(current)
        eq = path[-1][1]

        if current == goal:
            break

        # change graph to present equipment
        graph = graphs[eq]

        for neighbor in graph[current]:
            # change of eq?
            if types[current] == types[neighbor]:
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
    start = (0, 0)
    target = (757, 12)

    # scratchpad for geo & erosion
    # geo on the boundaries

    temp = np.ones((factor * target[0] + 1, factor * target[1] + 1),
                   dtype=int) * -1

    # precalculate erosion
    temp[0, :] = (16807 * np.arange(0, temp.shape[1]) + depth) % 20183
    temp[:, 0] = (7905 * np.arange(0, temp.shape[0]) + depth) % 20183
    temp[0, 0] = depth % 20183
    temp[target] = depth % 20183

    # 1st pass
    for i in range(1, temp.shape[0]):
        for j in range(1, temp.shape[1]):

            if (i, j) == target:
                continue
            temp[i, j] = temp[i - 1, j]
            temp[i, j] *= temp[i, j - 1]
            temp[i, j] = (temp[i, j] + depth) % 20183

    temp[target] = depth

    types = np.vectorize(ttype)(temp)

    # risk level
    risk = np.sum(types[:target[0] + 1, :target[1] + 1])
    print('\n')
    print(risk)


### part two
    graphTR, graphCL, graphNone = buildGraphs(types, source=(0, 0))

    D, P = algo(types, [graphTR, graphCL, graphNone], eqstart=0, start=start,
                goal=target)

    print(P[target][-1][-1][-1] + 1 - 7)
