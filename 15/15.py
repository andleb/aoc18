# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 22:14:09 2018

@author: Andrej Leban
"""

import copy
import itertools as it
import functools as ft
import collections as coll

import sortedcontainers as sc
from blist import blist

from prioritydict import priorityDictionary

import re

#re.search('@ (\d+),(\d+)', item).groups()))

def parseInput(inp):
    data = []
    with open(inp, 'r') as f:
        for line in f:
            data.append(line)

    return data


def buildGraph(data):
    graph = {}
    goblins = []
    elves = []

    for i in range(1, len(data)-1):
        for j in range(1,len(data[i])-1):
            if data[i][j] == 'G':
                goblins.append( ( (i,j), 200))
            if data[i][j] == 'E':
                elves.append( ( (i,j), 200))

            for (k,l) in [(0,-1), (0,1), (-1,0), (1,0)]:
                if data[i+k][j+l] != '#':
                    try:
                        graph[(i,j)][(i+k, j+l)] = 1
                    except KeyError:
                        graph[(i,j)] = {(i+k, j+l): 1}

    return graph, goblins, elves


def Dijkstra(G,start,end=None):

    D = {}	# dictionary of final distances
    P = {}	# dictionary of predecessors
    Q = priorityDictionary()   # est.dist. of non-final vert.
    Q[start] = 0

    for v in Q:
        D[v] = Q[v]
        if v == end:
            break

        for w in G[v]:
             vwLength = D[v] + G[v][w]
             if w in D:
                 if vwLength < D[w]:
                     raise ValueError("Dijkstra: found better path to already-final vertex")
             elif w not in Q or vwLength < Q[w]:
                 Q[w] = vwLength
                 P[w] = v

    return (D,P)


def printMaze(graph, goblins, elves):
    res = np.chararray((max(graph, key=lambda t:t[0])[0]+2,
                        max(graph, key=lambda t:t[1])[1]+2), itemsize=1, unicode=True)
    res[:] = '#'
#    res = np.ndarray((len(graph), len(graph)), dtype=np.string_)
    for node, edges in graph.items():
#        print(node, edges)
        for edge in edges.keys():
#            print(edge)
            res[edge[0], edge[1]] = '.'

    for gob in goblins:
        res[gob[0]] = 'G'# + str(gob[1])

    for elf in elves:
        res[elf[0]] = 'E'# + str(elf[1])

    print(res)
    return res




if __name__ == "__main__":
#    pass

    data = parseInput("input.txt")

#    data = ['#######',
#'#.G.E.#',
#'#E.G.E#',
#'#.G.E.#',
#'#######']

#    data = ['#########',
#'#G..G..G#',
#'#.......#',
#'#.......#',
#'#G..E..G#',
#'#.......#',
#'#.......#',
#'#G..G..G#',
#'#########']

    data = ['#######',
'#.G...#',
'#...EG#',
'#.#.#G#',
'#..G#E#',
'#.....#',
'#######']

#    data = ['#######',
#'#G..#E#',
#'#E#E.E#',
#'#G.##.#',
#'#...#E#',
#'#...E.#',
#'#######',]

    attackP = 3

    graph, goblins, elves = buildGraph(data)
#    D, P = Dijkstra(graph,(1,1))

    n = 0

    while len(goblins) and len(elves):
        goblins = sorted(goblins, key=lambda x: x[0])
        elves = sorted(elves, key=lambda x: x[0])

        print("\n", n)
        res = printMaze(graph, goblins, elves)
        print(goblins)
        print(elves)

        # reading order

        #TODO: do this above and just add/remove edges after each move
        # modify graph by removing the combatants
        graphNoC = copy.deepcopy(graph)
        for c in goblins + elves:
            for node, edges in graphNoC.items():
                try:
                    del edges[c[0]]
                except KeyError:
                    continue


        ngoblins = 0
        nelves = 0

        for i, c in enumerate(sorted(goblins + elves, key=lambda x: x[0])):

            node = c[0]
            dist, pred = Dijkstra(graphNoC, node)
            del dist[node]
            range_targets = []

            #goblin elf switch
            gob = c[0] in [g[0] for g in goblins]

            if gob:
                friends = goblins
                enemies = elves
            else:
                friends = elves
                enemies = goblins

            for e in enemies:
                range_targets.extend([t for t in graphNoC[e[0]].keys()])

            adjacentEn = [neigh for neigh in graph[node] if neigh in\
                          [t[0] for t in enemies]]
            if len(adjacentEn):
                range_targets.append(node)

            if node not in range_targets:
                #Move
                # min orders the results in tiebreak
                dist_range_targets = {k: v for k,v in dist.items() if k in range_targets}

                # move if possible
                if len(dist_range_targets):
                        #tiebreak reading order
                    targetnode = min(dist_range_targets.items(),
                                     key=lambda t: (t[1], t[0]))[0]

                    path = [targetnode]
                    prednode = pred[targetnode]
                    while prednode != node:
                        path.append(prednode)
                        prednode = pred[prednode]
                    path.append(node)
                    path = path[::-1]

                    #take step
                    newnode = path[1]
                    # i for elves compensation
#                    friends[ngoblins if gob else nelves] = (node, c[1])
                    friends[[f[0] for f in friends].index(node)] = (newnode, c[1])

                    # modify graph by removing the combatants
                    #TODO: do this above and just add/remove edges after each move
                    graphNoC = copy.deepcopy(graph)
                    for el in goblins + elves:
                        for nod, edg in graphNoC.items():
                            try:
                                del edg[el[0]]
                            except KeyError:
                                continue

            #Attack
            if node in range_targets:
                                                        #NOTE: consider combatants as well here
                targets = sorted([enemy for enemy in enemies if enemy[0] in graph[node]],
                       key=lambda enemy: (enemy[1], enemy[0]))
                target = targets[0]

                #attack the target
                indT = enemies.index(target)
                newHP =  enemies[indT][1] - attackP
                if newHP <= 0:
                    enemies.pop(indT)
                else:
                    enemies[indT] = (enemies[indT][0], newHP)

            if gob:
                ngoblins += 1
            else:
              nelves += 1

        if len(goblins) and len(elves):
            n += 1

    print("\n", n)
    res = printMaze(graph, goblins, elves)
    print(goblins)
    print(elves)

    sumhp = sum([g[1] for g in (goblins if len(goblins) else elves)])
    print(sumhp*n)
