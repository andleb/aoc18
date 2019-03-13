# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 22:19:34 2018

@author: Andrej Leban
"""

import collections as coll

import re

import numpy as np


def parseInputClay(inp):
    clay = set()

    with open(inp, 'r') as f:
        for line in f:
            # remove newlines
            line = line[:-1]

            try:
                x, ys, ye = tuple(map(int, re.search('\.*x=(\d+)\s*,\s*y=(\d+)\.\.(\d+).*',
                                                     line).groups()))
                for y in range(ys, ye + 1):
                    clay.add((y, x))
                continue
            except AttributeError:
                pass
            try:
                y, xs, xe = tuple(map(int, re.search('\.*y=(\d+)\s*,\s*x=(\d+)\.\.(\d+).*',
                                                     line).groups()))
                for x in range(xs, xe + 1):
                    clay.add((y, x))
                continue
            except AttributeError:
                pass

    minY = min(clay, key=lambda t: t[0])[0]
    sizY = max(clay, key=lambda t: t[0])[0]
    sizX = max(clay, key=lambda t: t[1])[1]

    return clay, minY, sizY, sizX


def buildGraph(data):
    graph = {}

    for i in range(0, len(data)):
        for j in range(0, len(data[i])):
            for (k, l) in [(0, -1), (0, 1), (1, 0)]:
                if i + k >= len(data) or j + l >= len(data[i]) or\
                        i + k < 0 or j + l < 0:
                    continue

                if data[i + k][j + l] != '#':
                    try:
                        graph[(i, j)][(i + k, j + l)] = 1
                    except KeyError:
                        graph[(i, j)] = {(i + k, j + l): 1}

    source = (0, (len(data[0]) - 1) // 2)
    return graph, source


def printGraph(graph, clay, source, visited={}, rest={}):
    maxY = max((max(graph, key=lambda t: t[0], default=(1, 1))[0] + 1,
                max(visited, key=lambda t: t[0], default=(1, 1))[0] + 1,
                max(rest, key=lambda t: t[0], default=(1, 1))[0] + 1))
    maxX = max((max(graph, key=lambda t: t[1], default=(1, 1))[1] + 1,
                max(visited, key=lambda t: t[1], default=(1, 1))[1] + 1,
                max(rest, key=lambda t: t[1], default=(1, 1))[1] + 1))

    res = np.chararray((maxY + 1, maxX + 1), itemsize=1, unicode=True)

    res[:] = '.'

    clayS = sorted(clay, key=lambda t: (t[0], t[1]))

    for cl in clayS:
        if cl[0] < (maxY + 1) and cl[1] < (maxX + 1):
            res[cl[0], cl[1]] = '#'
        elif cl[0] > maxY:
            break

    for vis in visited:
        try:
            res[vis] = '|'
        except KeyError:
            pass

    for r in rest:
        try:
            res[r] = '~'
        except KeyError:
            pass

    res[source] = '+'

#    print(res)

    return res


def discoverNeigh(graph, clay, rest, node, sizY):
    try:
        graph[node]
    except KeyError:
        graph[node] = {}

    for (k, l) in [(0, -1), (0, 1), (1, 0)]:
            neigh = (node[0] + k, node[1] + l)
            if neigh not in (clay | rest) and node[0] < sizY:
                try:
                    graph[node][neigh]
                except KeyError:
                    graph[node][neigh] = 1


def visitBFS(graph, clay, rest, visited, queue, sizY):

    origSource = queue[0]
    newSource = None

    while len(queue):
        node = queue.popleft()
        discoverNeigh(graph, clay, rest, node, sizY)

        edges = graph[node].copy()
        candidates = [edg for edg in edges]
        candidates = sorted(candidates, key=lambda x: (x[0], -x[1]),
                            reverse=True)

        # always down or spill
        if len(candidates) and candidates[0][0] > node[0]:
            candidates = candidates[:1]
        # go left/right - spillover candidate
        elif newSource is None and\
            node[0] != origSource[0] and\
                len(candidates) and candidates[0][0] == node[0]:
            newSource = node

        for child in candidates:
            if child in visited:
                candidates.remove(child)

        queue.clear()
        queue.extend(candidates)
#        queue.extendleft(candidates[::-1])

        visited.add(node)

    return node, newSource


def waterfall(graph, clay, rest, visited, sources):
    print("\n")
    print(sources)
    print("\n")

    n = 0
    sourceO = sources[0]
    if sourceO[0] == 673:
        pass

    visitedPrev = visited.copy()
    seenSources = set(sources.copy())
                        # NOTE: placeholder for origin source
    prevRest = coll.deque(list(rest))

    while len(sources):

        queue = coll.deque([sources[-1]])
        visitedNew = visitedPrev.copy()

        # Spillover: new source
        node, newSource = visitBFS(graph, clay, rest, visitedNew, queue, sizY)

        ## rest - came to stop not at boundary or above a visited path
        if node[0] not in [minY, sizY] and (node[0] + 1, node[1]) not in visitedPrev:

            visitedR = set()

            queue = coll.deque([node])
            # start another bfs from the found node to see if a lower node can be found
            nodeR, _ = visitBFS(graph, clay, rest, visitedR, queue, sizY)

            if nodeR[0] == node[0]:
                visitedR.add(node)
                rest |= visitedR
                prevRest.extend([v for v in visitedR if v not in prevRest])

                # not in the process of filling the reservoir
                if newSource is not None and newSource != sources[-1] and\
                        len(visitedNew - rest):

                    # new source must be above rest and have visited to right or left
                    if (newSource[0] + 1, newSource[1]) in rest and\
                        ((newSource[0], newSource[1] + 1) in (visitedNew - rest) or
                            (newSource[0], newSource[1] - 1) in (visitedNew - rest)):

                        sources.append(newSource)
                        seenSources.add(node)
                        visitedPrev |= set([v for v in visitedNew if v[0] < newSource[0]])

                # rest nodes are invisible in the graph, so delete them
                for nd, ed in graph.items():
                    for restNode in visitedR:
                        try:
                            del ed[restNode]
                        except KeyError:
                            continue

                for restNode in visitedR:
                    try:
                        del graph[restNode]
                    except KeyError:
                            continue

                # case when source gets swamped
                # move source one up
                if sources[-1][0] == nodeR[0]:
                    sources[-1] = (sources[-1][0] - 1, sources[-1][1])

            # filled reservoir: water can be taken to start flowing from here
            else:
                if node not in seenSources and node[0] != sources[-1][0]:
                    # left
                    newnode = (node[0], node[1]-1)
                    while newnode in visitedNew:
                        visitedPrev.add(node)
                        node = newnode
                        newnode = (newnode[0], newnode[1]-1)
                    # right
                    else:
                        newnode = (node[0], node[1]+1)
                        while newnode in visitedNew:
                            visitedPrev.add(node)
                            node = newnode
                            newnode = (newnode[0], newnode[1]+1)

                    sources.append(node)
                    seenSources.add(node)

                elif ((sources[-1][0], sources[-1][1] + 1) in visitedNew and
                        (sources[-1][0], sources[-1][1] - 1) in visitedNew) or\
                      (sources[-1][0] + 1, sources[-1][1]) in visitedNew:

                    # only pop if nowhere to go
                    sources.pop()

                elif len(sources) == 1:
                    sources.pop()

                visitedPrev |= set([v for v in visitedNew if v[0] <= node[0]])

        ## reached the boundary - set new source, try all paths
        else:
            # new source- last visited next to rest and with somewhere to go
            # prevvisited - visited + current source

            visitedPrev |= visitedNew

            # NOTE: same as in case when filling
            # new source must be above rest and have visited to right or left
            if newSource is not None and newSource != sources[-1] and\
                    len(visitedNew - rest):
                if (newSource[0] + 1, newSource[1]) in rest and\
                    ((newSource[0], newSource[1] + 1) in (visitedNew - rest) or
                        (newSource[0], newSource[1] - 1) in (visitedNew - rest)):

                    sources.append(newSource)
                    visitedPrev |= set([v for v in visitedNew if v[0] <
                                        newSource[0]])

            # all paths exhausted?
            if set(graph[sources[-1]].keys()).issubset(visitedPrev)\
                    or len(sources) == 1:
                sources.pop()

        if node[0] >= sizY:
            break

        n += 1
        if not n % 50:
            print(n, len(visitedPrev), len(visitedNew), len(rest))
#            res = printGraph(graph, clay, sourceO, visitedPrev, rest)
#            np.savetxt("res.txt", res, fmt='%c', delimiter="", newline="\n")

    visited |= visitedPrev
#    res = printGraph(graph, clay, sourceO, visited, rest)
#    np.savetxt("res.txt", res, fmt='%c', delimiter="", newline="\n")

    return sources


if __name__ == "__main__":

### EXAMPLE
#    data = ['......+.......',
#'............#.',
#'.#..#.......#.',
#'.#..#..#......',
#'.#..#..#......',
#'.#.....#......',
#'.#.....#......',
#'.#######......',
#'..............',
#'..............',
#'....#.....#...',
#'....#.....#...',
#'....#.....#...',
#'....#######...']
#
#    clay = set()
#    for i, line in enumerate(data):
#        for j, c in enumerate(line):
#            if c == "#":
#                clay.add((i, j))
#
#    minY = min(clay, key=lambda t: t[0])[0]
#    sizY = max(clay, key=lambda t: t[0])[0]
#    sizX = max(clay, key=lambda t: t[1])[1]
#    sourceO = (0, (sizX) // 2)

    clay, minY, sizY, sizX = parseInputClay("input.txt")
    # the source is always at 0
    minY = min(minY, 0)
    sourceO = (minY, 500)

    graph = {}
    rest = set()
    visitedPrev = set()
    visited = set()

    sources = coll.deque([sourceO])

    # build graph as you go
    discoverNeigh(graph, clay, rest, sources[-1], sizY)

    # this will recurse - start from last known source
    # all the properties are mutables, so they get shared
    while len(sources):
        newSources = waterfall(graph, clay, rest, visited, [sources[-1]])
        if len(newSources) and newSources[-1] != sources[-1]:
            sources.extend([s for s in newSources if s not in sources])
        else:
            sources.pop()

    print('\n')
    print('\n')
    res = printGraph(graph, clay, sourceO, visited, rest)
#    res = printGraph(graph, clay, sources[-1], visited, rest)
    np.savetxt("res.txt", res, fmt='%c', delimiter="", newline="\n")

### FIRST.
    # compensates for source
    print(len(visited) + len(rest) - 1)

### SECOND
    print(len(rest))
