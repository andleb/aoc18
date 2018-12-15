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
    #FIXME: bug in buildgraph
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


def updateInvariants(graph, goblins, elves, node=None):

    goblins = sorted(goblins, key=lambda x: x[0])
    elves = sorted(elves, key=lambda x: x[0])

    graphNoC = copy.deepcopy(graph)
    for el in goblins + elves:
        for nod, edg in graphNoC.items():
            try:
                del edg[el[0]]
            except KeyError:
                continue

    if node is not None:
        dist, pred = Dijkstra(graphNoC, node)
        del dist[node]
        return graphNoC, goblins, elves, dist, pred

    return graphNoC, goblins, elves

def solve1(data):
    attackP = 3

    graph, goblins, elves = buildGraph(data)
#    D, P = Dijkstra(graph,(1,1))

    n = 0

    while len(goblins) and len(elves):

        graphNoC, goblins, elves = updateInvariants(graph, goblins, elves, node=None)

#        print("\n", n)
#        res = printMaze(graph, goblins, elves)
#        print(goblins)
#        print(elves)

#        initOrdering = sorted(goblins + elves, key=lambda x: x[0])
#        for i, c in enumerate(initOrdering):
#        for i, c in enumerate(sorted(goblins + elves, key=lambda x: x[0])):
        ordering = coll.deque(sorted(goblins + elves, key=lambda x: x[0]))

#        for c in ordering:
        while len(ordering):
#            if c not in (sorted(goblins + elves, key=lambda x: x[0])):
#                continue
            if not len(goblins) or not len(elves):
                print("exiting early")
                break

            c = ordering.popleft()
            node = c[0]
            dist, pred = Dijkstra(graphNoC, node)
            del dist[node]

            range_targets = []

            #goblin elf switch
            gob = c[0] in [g[0] for g in goblins]
#
#            if gob:
#                friends = goblins
#                enemies = elves
#            else:
#                friends = elves
#                enemies = goblins

#            for e in enemies:
            for e in (elves if gob else goblins):
                range_targets.extend([t for t in graphNoC[e[0]].keys()])

            # are we already next to an enemy?
            adjacentEn = [neigh for neigh in graph[node] if neigh in\
                          [t[0] for t in (elves if gob else goblins)]]
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
#                    indF = [f[0] for f in friends].index(node)
                    indF = [f[0] for f in (goblins if gob else elves)].index(node)
                    node = path[1]
                    hp = (goblins if gob else elves)[indF][1]

                    #NOTE: move, update data here
                    (goblins if gob else elves)[indF] = (node, hp)

                    graphNoC, goblins, elves = updateInvariants(graph, goblins, elves)

                    #update range_targets !
                    # check for new_node below instead
                    range_targets = []
                    for e in (elves if gob else goblins):
                        range_targets.extend([t for t in graphNoC[e[0]].keys()])

                    adjacentEn = [neigh for neigh in graph[node] if neigh in\
                          [t[0] for t in (elves if gob else goblins)]]
                    if len(adjacentEn):
                        range_targets.append(node)

            #Attack
            if node in range_targets:
                                                        #NOTE: consider combatants as well here
                targets = sorted([enemy for enemy in (elves if gob else goblins)\
                                  if enemy[0] in graph[node]],
                       key=lambda enemy: (enemy[1], enemy[0]))
                target = targets[0]

                #attack the target
                indT = (elves if gob else goblins).index(target)
                newHP =  (elves if gob else goblins)[indT][1] - attackP
                if newHP <= 0:
                    #NOTE: remove, update data here
                    (elves if gob else goblins).pop(indT)
                    try:
                        ordering.remove(target)
                    except ValueError:
                        pass

                    if not len((elves if gob else goblins)):
                        print("exiting early")
                        break
                    else:
                        graphNoC, goblins, elves = updateInvariants(graph, goblins, elves)
                else:
                    (elves if gob else goblins)[indT] = (target[0], newHP)

            #update loop invariant
#            ordering = sorted(goblins + elves, key=lambda x: x[0])

#        goblins = sorted(goblins, key=lambda x: x[0])
#        elves = sorted(elves, key=lambda x: x[0])

        lg = len(goblins)
        le = len(elves)

#        print(n, i, len(initOrdering))
        # what qualifies for a full round - all creatures have taken their turn
#        if (i == len(initOrdering) - 1) or (lg and le):
        if (lg and le) or not len(ordering):
            n += 1



    print("\n", n)
    printMaze(graph, goblins, elves)
    print(goblins)
    print(elves)

    sumhp = sum([g[1] for g in (goblins if len(goblins) else elves)])
    print(n, sumhp, sumhp*n)

    return n, sumhp, sumhp*n, elves, goblins

def solve2(data, attackE, attackG=3):

    graph, goblins, elves = buildGraph(data)
#    D, P = Dijkstra(graph,(1,1))

    n = 0

    while len(goblins) and len(elves):

        graphNoC, goblins, elves = updateInvariants(graph, goblins, elves, node=None)

        ordering = coll.deque(sorted(goblins + elves, key=lambda x: x[0]))

#        for c in ordering:
        while len(ordering):
#            if c not in (sorted(goblins + elves, key=lambda x: x[0])):
#                continue
            if not len(goblins) or not len(elves):
                print("exiting early")
                break

            c = ordering.popleft()
            node = c[0]
            dist, pred = Dijkstra(graphNoC, node)
            del dist[node]

            range_targets = []

            #goblin elf switch
            gob = c[0] in [g[0] for g in goblins]

#            for e in enemies:
            for e in (elves if gob else goblins):
                range_targets.extend([t for t in graphNoC[e[0]].keys()])

            # are we already next to an enemy?
            adjacentEn = [neigh for neigh in graph[node] if neigh in\
                          [t[0] for t in (elves if gob else goblins)]]
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

                    # take step
#                    indF = [f[0] for f in friends].index(node)
                    indF = [f[0] for f in (goblins if gob else elves)].index(node)
                    node = path[1]
                    hp = (goblins if gob else elves)[indF][1]

                    #NOTE: move, update data here
                    (goblins if gob else elves)[indF] = (node, hp)

                    graphNoC, goblins, elves = updateInvariants(graph, goblins, elves)

                    #update range_targets !
                    # check for new_node below instead
                    range_targets = []
                    for e in (elves if gob else goblins):
                        range_targets.extend([t for t in graphNoC[e[0]].keys()])

                    adjacentEn = [neigh for neigh in graph[node] if neigh in\
                          [t[0] for t in (elves if gob else goblins)]]
                    if len(adjacentEn):
                        range_targets.append(node)

            #Attack
            if node in range_targets:
                                                        #NOTE: consider combatants as well here
                targets = sorted([enemy for enemy in (elves if gob else goblins)\
                                  if enemy[0] in graph[node]],
                       key=lambda enemy: (enemy[1], enemy[0]))
                target = targets[0]

                #attack the target
                attack = attackG if gob else attackE

                indT = (elves if gob else goblins).index(target)
                newHP =  (elves if gob else goblins)[indT][1] - attack
                if newHP <= 0:
                    if gob:
                        print("elf died")
                        return -1
                    else:
                        #NOTE: remove, update data here
                        goblins.pop(indT)

                    try:
                        ordering.remove(target)
                    except ValueError:
                        pass

                    if not len((elves if gob else goblins)):
                        print("exiting early")
                        break
                    else:
                        graphNoC, goblins, elves = updateInvariants(graph, goblins, elves)
                else:
                    (elves if gob else goblins)[indT] = (target[0], newHP)


        lg = len(goblins)
        le = len(elves)

        if (lg and le) or not len(ordering):
            n += 1



    print("\n", n)
    printMaze(graph, goblins, elves)
    print(goblins)
    print(elves)

    sumhp = sum([g[1] for g in (goblins if len(goblins) else elves)])
    return (attackE, n, sumhp, sumhp*n, elves, goblins)



if __name__ == "__main__":

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

### first

#OK
#    data = ['#######',
#'#.G...#',
#'#...EG#',
#'#.#.#G#',
#'#..G#E#',
#'#.....#',
#'#######']

### extra debug

#OK
#    data = ['#######',
#'#G..#E#',
#'#E#E.E#',
#'#G.##.#',
#'#...#E#',
#'#...E.#',
#'#######']

#OK
#    data =\
#['#######',
#'#E..EG#',
#'#.#G.E#',
#'#E.##E#',
#'#G..#.#',
#'#..E#.#',
#'#######']

#OK
#    data = \
#['#######',
#'#E.G#.#',
#'#.#G..#',
#'#G.#.G#',
#'#G..#.#',
#'#...E.#',
#'#######']

#    data = \
#['#######',
#'#.E...#',
#'#.#..G#',
#'#.###.#',
#'#E#G#G#',
#'#...#G#',
#'#######']

#OK
#    data = \
#['#########',
#'#G......#',
#'#.E.#...#',
#'#..##..G#',
#'#...##..#',
#'#...#...#',
#'#.G...G.#',
#'#.....G.#',
#'#########']

#    graph, goblins, elves = buildGraph(data)
#    res = printMaze(graph, goblins, elves)

#    n, sumhp, sumhpn, elves, goblins = solve1(data)

    for attackE in range(4,1000):
        print(attackE)
        ret = solve2(data, attackE)
        if ret != -1:
            if len(ret[-2]) > len(ret[-1]):
#                print(ret)
                print(attackE)
                break



