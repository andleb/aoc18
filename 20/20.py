# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 20:51:57 2018

@author: Andrej Leban
"""

import collections as coll
import operator as op

from prioritydict import priorityDictionary
import numpy as np


def parseInput(inp):
    data = []
    with open(inp, 'r') as f:
        for line in f:
            data.append(line)

    return data


def printGraph(graph, source):

    yedges = set()
    for node, edges in graph.items():
        yedges |= {frozenset([node, ed]) for ed in edges if ed[0] != node[0]}

    xedges = set()
    for node, edges in graph.items():
        xedges |= {frozenset([node, ed]) for ed in edges if ed[1] != node[1]}

    maxY = 2 * (max(graph, key=lambda t: t[0], default=(1, 1))[0] + 1) + 1
    maxX = 2 * (max(graph, key=lambda t: t[1], default=(1, 1))[1] + 1) + 1

    res = np.chararray((maxY, maxX), itemsize=1, unicode=True)
    res[:] = '#'

    for node, edges in graph.items():

        res[2 * node[0] + 1, 2 * node[1] + 1] = '.'
        print(node, edges)

        for edge in edges:
            edge = min(edge, node)

            if {edge, node} in xedges:
                res[2 * edge[0] + 1, 2 * edge[1] + 2] = '|'
            elif {edge, node} in yedges:
                res[2 * edge[0] + 2, 2 * edge[1] + 1] = '--'

    res[2 * source[0] + 1, 2 * source[1] + 1] = 'X'

    print(res)
    return res


def getEdge(node, c):
    dic = {
            'N': (-1, 0),
            'E': (0, 1),
            'S': (1, 0),
            'W': (0, -1),
            }

    diff = dic[c]
    return (node[0] + diff[0], node[1] + diff[1])


def buildGraph(source, sregex):

    # undirected, weights are 1
    graph = {source: set()}
    node = source
    sources = coll.deque()

    for i, c in enumerate(regex):
        if c == '^':
            continue
        elif c == '$':
            break

        # branching
        if c == '(':
            sources.append(node)
            continue
        if c == '|':
            node = sources[-1]
            continue
        if c == ')':
            sources.pop()
            continue

        edge = getEdge(node, c)
        try:
            graph[node].add(edge)
        except KeyError:
            graph[node] = {edge}
        try:
            graph[edge].add(node)
        except KeyError:
            graph[edge] = {node}

        # follow the edge
        node = edge

    return graph


def Dijkstra(G, start, end=None):

    D = {}  # dictionary of final distances
    P = {}  # dictionary of predecessors
    Q = priorityDictionary()  # est.dist. of non-final vert.
    Q[start] = 0

    for v in Q:
        D[v] = Q[v]
        if v == end:
            break

        for w in G[v]:
            vwLength = D[v] + 1
            if w in D:
                if vwLength < D[w]:
                    raise ValueError("Dijkstra: found better path to already-final vertex")
            elif w not in Q or vwLength < Q[w]:
                Q[w] = vwLength
                P[w] = v

    return (D, P)


if __name__ == "__main__":

### EXAMPLES:

#    graph1 = {
#    (2,2):[(2,1)],
#    (2,1):[(1,1)],
#    (1,1):[(1,2)],
#    (1,2):[(1,1)]}

#    data =\
#['#####',
#'#.|.#',
#'#-###',
#'#.|X#',
#'#####']
#
#    source = (1,1)
#    regex = '^WNE$'
#    graph = buildGraph(source, regex)
#    res = printGraph(graph,source)
#
#    ar = np.array(list(map(list, data)))
#    print(np.all(ar == res))
#
#    D, P = Dijkstra(graph, source)

#    data =\
#['#########',
#'#.|.|.|.#',
#'#-#######',
#'#.|.|.|.#',
#'#-#####-#',
#'#.#.#X|.#',
#'#-#-#####',
#'#.|.|.|.#',
#'#########']

#    source = (2,2)
#    regex = '^ENWWW(NEEE|SSE(EE|N))$'
#    graph = buildGraph(source, regex)
#    res = printGraph(graph,source)
#
#    ar = np.array(list(map(list, data)))
#    print(np.all(ar == res))
#    D, P = Dijkstra(graph, source)
#    print(D)

#    data =[\
#'###########',
#'#.|.#.|.#.#',
#'#-###-#-#-#',
#'#.|.|.#.#.#',
#'#-#####-#-#',
#'#.#.#X|.#.#',
#'#-#-#####-#',
#'#.#.|.|.|.#',
#'#-###-###-#',
#'#.|.|.#.|.#',
#'###########']
#
#    source = (2,2)
#    regex = '^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$'
#    graph = buildGraph(source, regex)
#    res = printGraph(graph,source)
#
#    ar = np.array(list(map(list, data)))
#    print(np.all(ar == res))
#    D, P = Dijkstra(graph, source)
#    print(D)
#    maxRoom = max(D.items(), key=op.itemgetter(1))[0]
#    print(maxRoom, D[maxRoom])

#    data =\
# ['#############',
#'#.|.|.|.|.|.#',
#'#-#####-###-#',
#'#.#.|.#.#.#.#',
#'#-#-###-#-#-#',
#'#.#.#.|.#.|.#',
#'#-#-#-#####-#',
#'#.#.#.#X|.#.#',
#'#-#-#-###-#-#',
#'#.|.#.|.#.#.#',
#'###-#-###-#-#',
#'#.|.#.|.|.#.#',
#'#############']
#
#    source = (3,3)
#    regex = '^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$'
#    graph = buildGraph(source, regex)
#    res = printGraph(graph,source)
#
#    ar = np.array(list(map(list, data)))
#    print(np.all(ar == res))
#    D, P = Dijkstra(graph, source)
#    print(D)
#    maxRoom = max(D.items(), key=op.itemgetter(1))[0]
#    print(maxRoom, D[maxRoom])

#    data =\
# ['###############',
#'#.|.|.|.#.|.|.#',
#'#-###-###-#-#-#',
#'#.|.#.|.|.#.#.#',
#'#-#########-#-#',
#'#.#.|.|.|.|.#.#',
#'#-#-#########-#',
#'#.#.#.|X#.|.#.#',
#'###-#-###-#-#-#',
#'#.|.#.#.|.#.|.#',
#'#-###-#####-###',
#'#.|.#.|.|.#.#.#',
#'#-#-#####-#-#-#',
#'#.#.|.|.|.#.|.#',
#'###############']

#    source = (3,3)
#    regex = '^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$'
#    graph = buildGraph(source, regex)
#    res = printGraph(graph,source)
#
#    ar = np.array(list(map(list, data)))
#    print(np.all(ar == res))
#    D, P = Dijkstra(graph, source)
#    print(D)
#    maxRoom = max(D.items(), key=op.itemgetter(1))[0]
#    print(maxRoom, D[maxRoom])


### SOLUTIONS
    regex = parseInput("input.txt")[0][:-1]
    source = (0, 0)

    graph = buildGraph(source, regex)

    D, P = Dijkstra(graph, source)
    maxRoom = max(D.items(), key=op.itemgetter(1))[0]
    print(maxRoom, D[maxRoom])

### 2
    tot = 0
    for k, v in D.items():
        if v >= 1000:
            tot += 1

    print(tot)
