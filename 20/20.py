# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 20:51:57 2018

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


def printGraph(graph, source):

    yedges = set()
    for node, edges in graph.items():
        yedges |= {frozenset([node, ed]) for ed in edges if ed[0] != node[0]}

    xedges = set()
    for node, edges in graph.items():
        xedges |= {frozenset([node, ed]) for ed in edges if ed[1] != node[1]}

    maxY = 2*(max(graph, key=lambda t:t[0], default=(1,1))[0]+1) + 1
    maxX = 2*(max(graph, key=lambda t:t[1], default=(1,1))[1]+1) + 1


    res = np.chararray((maxY, maxX), itemsize=1, unicode=True)
    res[:] = '#'

    for node, edges in graph.items():

        res[2*node[0]+1, 2*node[1]+1] = '.'
        print(node, edges)

        for edge in edges:
            edge = min(edge, node)

            if {edge, node} in xedges:
                res[2*edge[0]+1, 2*edge[1]+2] = '|'
            elif {edge, node} in yedges:
                res[2*edge[0]+2, 2*edge[1]+1] = '--'

    res[2*source[0]+1, 2*source[1]+1] = 'X'

    print(res)
    return res


def getEdge(node, c):
    dic = {
            'N': (-1,0),
            'E': (0,1),
            'S': (1,0),
            'W': (0,-1),
            }

    diff = dic[c]
    return (node[0] + diff[0], node[1] + diff[1])


def buildGraph(source,regex):

    #undirected, weights are 1
    graph = {source: set()}
    node = source
    sources = coll.deque()

    print(source)
    print(regex)
#    for c in regex[1:-1]:
#        print(node)
#        node = getEdge(node, c)
#    print(node)


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

        #follow the edge
        node = edge

    return graph


if __name__ == "__main__":

#    regex = parseInput("input.txt")

#    graph1 = {
#    (2,2):[(2,1)],
#    (2,1):[(1,1)],
#    (1,1):[(1,2)],
#    (1,2):[(1,1)]}
#
#    data =\
#['#####',
#'#.|.#',
#'#-###',
#'#.|X#',
#'#####']

#    source = (1,1)
#    regex = '^WNE$'
#    printGraph(graph1, source)


#    source = (2,2)
#    regex = '^ENWWW(NEEE|SSE(EE|N))$'
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

