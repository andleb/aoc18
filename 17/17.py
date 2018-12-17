# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 22:19:34 2018

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

#only clay is counted
def parseInput(inp):
    data = []
    clay = set()
    with open(inp, 'r') as f:
        for line in f:
            # remove newlines
            line = line[:-1]

            try:
                x, ys, ye = tuple(map(int, re.search('\.*x=(\d+)\s*,\s*y=(\d+)\.\.(\d+).*', line).groups()))
                for y in range(ys, ye+1):
                    clay.add((y,x))
                continue
            except:
                pass
            try:
                y, xs, xe = tuple(map(int, re.search('\.*y=(\d+)\s*,\s*x=(\d+)\.\.(\d+).*', line).groups()))
                for x in range(xs, xe+1):
                    clay.add((y,x))
                continue
            except:
                pass

    sizY = max(clay, key=lambda t: t[0])[0]
    sizX = max(clay, key=lambda t: t[1])[1]

    for y in range(0, sizY+1):
        line = []
        for x in range(0, sizX+1):
            if (y,x) not in clay:
                line.append('.')
            else:
                line.append('#')
        data.append("".join(line))

    return data


def buildGraph(data):
    graph = {}

    for i in range(0, len(data)):
        for j in range(0,len(data[i])):

            for (k,l) in [(0,-1), (0,1), (1,0)]:
                if i+k >= len(data) or j+l >= len(data[i]) or\
                    i+k < 0 or j+l < 0:
                    continue


#                print(i,j,k,l)
                if data[i+k][j+l] != '#':
                    try:
                        graph[(i,j)][(i+k, j+l)] = 1
                    except KeyError:
                        graph[(i,j)] = {(i+k, j+l):
                            1}

    source = (0, (len(data[0])-1) // 2)
    return graph, source

def printGraph(graph, source, visited=[], rest=[]):
    res = np.chararray((max(graph, key=lambda t:t[0])[0]+1,
                        max(graph, key=lambda t:t[1])[1]+1), itemsize=1, unicode=True)
    res[:] = '#'
    for node, edges in graph.items():
#        print(node, edges)
        for edge in edges.keys():
#            print(edge)
            res[edge[0], edge[1]] = '.'

    for vis in visited:
        res[vis] = '|'

    for r in rest:
        res[r] = '~'

    res[source] = '+'

    print(res)
    return res


if __name__ == "__main__":

    data = parseInput("input.txt")


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
#'....#######...',]

    graphS, sourceO = buildGraph(data)
    sourceO = (0,500)


    graph = copy.deepcopy(graphS)

    sizY = max(graph.keys(), key=lambda t: t[0])[0]
    sizX = max(graph.keys(), key=lambda t: t[1])[1]

    #remove boundary left/right moves
    for x in range(0, sizX):
        try:
            graph[(sizY, x)]
        except KeyError:
            continue

        newEdg = {}
        for edg, wght in graph[(sizY, x)].items():
            if edg[0] != sizY:
                newEdg[edg] = wght
        graph[(sizY, x)] = newEdg



#    res = printGraph(graph, sourceO)

    source = sourceO
    rest = coll.deque()
    visitedPrev = coll.deque()
    prevRest = None
    meta = {source: (None, )}

    n = 0
    while n < 2000:
        queue = coll.deque([source])
        visited = visitedPrev.copy()
#        visited = coll.deque()

        while len(queue):

            node = queue.popleft()
#            print(node, queue, visited)

            candidates = graph[node].copy()

            candidates = sorted(candidates, key=lambda x:(x[0],-x[1]), reverse=True)

            for child in candidates:
                if child in visited:
                    candidates.remove(child)

            queue = coll.deque(candidates)

            visited.append(node)

        # rest - came to stop not at boundary
        if node[0] not in [0, sizY] and node[1] not in [0, sizX]:

            # start another bfs to see if a lower node can be found
#            print("rest candidate", node)

            queueR = coll.deque([node])
            visitedR = coll.deque()

            found = False

            while len(queueR):
                nodeR = queueR.popleft()

                candidatesR = graph[nodeR].copy()
                candidatesR = sorted(candidatesR, key=lambda x:(x[0],-x[1]), reverse=True)

                for childR in candidatesR:
                    if childR in visitedR:
                        candidatesR.remove(childR)

                if len(candidatesR) and candidatesR[0][0] > node[0]:
                    found = True
                    visitedR.append(nodeR)
                    break

                queueR = coll.deque(candidatesR)
                visitedR.append(nodeR)

#            res = printGraph(graph, node, visitedR, rest)

            if not found:
#                print("rest:", node)
                if node not in rest:
                    rest.append(node)
                prevRest = node
                for nd, ed in graph.items():
                    try:
                        del ed[node]
                    except KeyError:
                        continue

                del graph[node]
            else:
                source = node
                visitedPrev += coll.deque([v for v in visited if v[0] < node[0] and v not in visitedPrev])
#                print(source, visitedPrev)

        # reached the boundary - set new source, try all paths
        else:


            # new source- last visited next to rest and with somewhere to go
            # prevvisited - visited + current source
            visitedPrev += (coll.deque([v for v in visited if v not in visitedPrev])
                            + (coll.deque([source]) if source not in visitedPrev else coll.deque()))
            source = (prevRest[0]-1, prevRest[1])

            paths = [n for n in graph[source] if n not in visitedPrev]

            while len(paths):
                queueEnd = coll.deque([source])
                visitedEnd = coll.deque(visitedPrev)

                while len(queueEnd):
                    nodeEnd = queueEnd.popleft()

                    candidatesEnd = graph[nodeEnd].copy()
                    candidatesEnd = sorted(candidatesEnd, key=lambda x:(x[0],-x[1]), reverse=True)

                    for childEnd in candidatesEnd:
                        if childEnd in visitedEnd:
                            candidatesEnd.remove(childEnd)

                    queueEnd = coll.deque(candidatesEnd)
                    visitedEnd.append(nodeEnd)

                visitedPrev += (coll.deque([v for v in visitedEnd if v not in visitedPrev]))
                paths = [n for n in graph[source] if n not in visitedPrev]

            visited += (coll.deque([v for v in visitedPrev if v not in visited]))
            break

        n += 1
#        print('\n')
#        res = printGraph(graph, source, visited, rest)
#        print('\n')


#    res = printGraph(graph, sourceO, visited, rest)
    # compensate for source
    print(len(visited) + len(rest) - 1)







