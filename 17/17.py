# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 22:19:34 2018

@author: Andrej Leban
"""

import copy
import itertools as it
import functools as ft
import collections as coll
import pickle

import sortedcontainers as sc
from blist import blist

import re

#re.search('@ (\d+),(\d+)', item).groups()))

#TODO:
#   sets  OK
#   extend in x infinitely   OK
#       build graph on the fly   OK
#   recurse sources, prevRest at the end - now stacks(deque) OK


#
#   edges = graph[node].copy()
#
#KeyError: (97, 528)



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

def parseInputClay(inp):
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

    return clay, sizY, sizX

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


# FIXME:
def printGraph(graph, clay, source, visited={}, rest={}):
    maxY = max((max(graph, key=lambda t:t[0], default=(1,1))[0]+1,
                max(visited, key=lambda t:t[0], default=(1,1))[0]+1,
                max(rest, key=lambda t:t[0], default=(1,1))[0]+1))
    maxX = max((max(graph, key=lambda t:t[1], default=(1,1))[1]+1,
                max(visited, key=lambda t:t[1], default=(1,1))[1]+1,
                max(rest, key=lambda t:t[1], default=(1,1))[1]+1))

    res = np.chararray((maxY, maxX), itemsize=1, unicode=True)
    res[:] = '.'
#    for node, edges in graph.items():
##        print(node, edges)
#        for edge in edges.keys():
##            print(edge)
#            res[edge[0], edge[1]] = '.'

    clayS = sorted(clay, key=lambda t:(t[0], t[1]))

    for cl in clayS:
        if cl[0] < maxY and cl[1] < maxX:
            res[cl[0], cl[1]] = '#'
        elif cl[0] > maxY:
            break

    for vis in visited:
        try:
            res[vis] = '|'
        except:
            pass

    for r in rest:
        try:
            res[r] = '~'
        except:
            pass

    res[source] = '+'

    print(res)
    return res


def discoverNeigh(graph, clay, rest, node, sizY):
    try:
        graph[node]
    except KeyError:
        graph[node] = {}

    for (k,l) in [(0,-1), (0,1), (1,0)]:
            neigh = (node[0]+k, node[1]+l)
            if neigh not in (clay | rest) and node[0] < sizY:
                try:
                    graph[node][neigh]
                except KeyError:
                    graph[node][neigh] = 1


def visitBFS(graph, clay, rest, visited, queue, sizY):

    while len(queue):
        node = queue.popleft()
        discoverNeigh(graph, clay, rest, node, sizY)

        edges = graph[node].copy()
        candidates = [edg for edg in edges]
        candidates = sorted(candidates, key=lambda x:(x[0],-x[1]), reverse=True)
        #always down
        if len(candidates) and candidates[0][0] > node[0]:
            candidates = candidates[:1]

        for child in candidates:
            if child in visited:
                candidates.remove(child)

        queue.clear()
        queue.extend(candidates)

        visited.add(node)

    return node

if __name__ == "__main__":

    pass

##    try:
##        data = pickle.load(open('data', 'rb'))
##    except:
##       data = parseInput("input.txt")
##        pickle.dump(data, open('data', 'wb'))
#
#    data = parseInput("input.txt")

    clay, sizY, sizX = parseInputClay("input.txt")
    sourceO = (0, 500)

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
#                clay.add((i,j))
#
#    sizY = max(clay, key=lambda t: t[0])[0]
#    sizX = max(clay, key=lambda t: t[1])[1]
#    sourceO = (0, (sizX) // 2)


    graph = {}

    rest = set()
    visitedPrev = set()

    sources = coll.deque([sourceO])
    seenSources = set([sourceO])
                        #NOTE: placeholder for origin source
    prevRest = coll.deque([None])

    #build graph as you go
    discoverNeigh(graph, clay, rest, sources[-1], sizY)
#    #remove left/right at the source
#    graph[sourceO] = {(sourceO[0]+1, sourceO[1]): 1}

    n = 0
    while n < 50 and len(sources):
        print('\n')
        print(n, len(visitedPrev), len(visited), len(rest))
        res = printGraph(graph, clay, sources[-1], visited, rest)
        print('\n')


        queue = coll.deque([sources[-1]])
        visited = visitedPrev.copy()

        node = visitBFS(graph, clay, rest, visited, queue, sizY)

        # rest - came to stop not at boundary
        if node[0] not in [0, sizY] and node[1] not in [0, sizX]:
        # start another bfs to see if a lower node can be found
#            print("rest candidate", node)
            visitedR = set()

            #TODO: break early
            queue = coll.deque([node])
            nodeR = visitBFS(graph, clay, rest, visitedR, queue, sizY)
#            res = printGraph(graph, clay, nodeR, visitedR, rest)

            if nodeR[0] == node[0]:
#                print("rest:", node)
                visitedR.add(node)
                rest |= visitedR
                prevRest.extend(visitedR)

                # rest nodes are invisible in the graph
                for nd, ed in graph.items():
                    for restNode in visitedR:
                        try:
                            del ed[restNode]
                        except KeyError:
                            continue

                for restNode in visitedR:
                    try:
                        del graph[node]
                    except KeyError:
                            continue

            # filled reservoir: water can be taken to start flowing from here
            else:
                if node not in seenSources:
                    sources.append(node)
                    seenSources.add(node)
                else:
                    sources.pop()
#                sources.append((prevRest[-1][0]-1, prevRest[-1][1]))
                visitedPrev |= set([v for v in visited if v[0] < node[0]])
#                print(source, visitedPrev)

        # reached the boundary - set new source, try all paths
        else:
            # new source- last visited next to rest and with somewhere to go
            # prevvisited - visited + current source

            visitedPrev |= visited

            newSource = (prevRest[-1][0]-1, prevRest[-1][1])
            if newSource not in seenSources:
                sources.append(newSource)
                seenSources.add(newSource)
                discoverNeigh(graph, clay, rest, sources[-1], sizY)

            #all paths exhausted?
            if set(graph[sources[-1]].keys()).issubset(visitedPrev)\
                or len(sources) == 1:
                sources.pop()




#            while len(sources) > 1:
#                visitedPrev |= visited
#                visitedPrev.add(sources[-1])
#
##                sources.append = (prevRest[0]-1, prevRest[1])
#                source = sources.pop()
#
#                paths = sorted([n for n in graph[source] if n not in visitedPrev],
#                               key=lambda x:(x[0],-x[1]), reverse=True)
#
#                if len(paths) and paths[0][0] > source[0]:
#                            paths = paths[:1]
#
#                while len(paths):
#                    queueEnd = coll.deque([source])
#                    visitedEnd = visitedPrev
#
#                    while len(queueEnd):
#                        nodeEnd = queueEnd.popleft()
#                        discoverNeigh(graph, clay, rest, nodeEnd, sizY)
#
#                        candidatesEnd = graph[nodeEnd].copy()
#                        candidatesEnd = sorted(candidatesEnd, key=lambda x:(x[0],-x[1]), reverse=True)
#                        #always down
#                        if len(candidatesEnd) and candidatesEnd[0][0] > nodeEnd[0]:
#                            candidatesEnd = candidatesEnd[:1]
#
#                        for childEnd in candidatesEnd:
#                            if childEnd in visitedEnd:
#                                candidatesEnd.remove(childEnd)
#
#                        queueEnd.clear()
#                        queueEnd.extend(candidatesEnd)
#                        visitedEnd.add(nodeEnd)
#
#                    visitedPrev |= visitedEnd
#                    paths = sorted([n for n in graph[source] if n not in visitedPrev],
#                                   key=lambda x:(x[0],-x[1]), reverse=True)
#
#
#                visited |= visitedPrev
##                print('\n')
##                res = printGraph(graph, clay, source, visited, rest)
##                print('\n')
#
#            break

        n += 1
#        if not n % 100:

    print('\n')
    print('\n')
    res = printGraph(graph, clay, sourceO, visited, rest)

    # compensate for source
    #FIXME: compensate for the y dist between source and first clay in y
    print(len(visited) + len(rest) - 1)
