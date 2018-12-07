# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 21:27:18 2018

@author: Andrej Leban
"""

import itertools as it
import functools as ft
import collections as coll

import sortedcontainers as sc
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
    root = None

    for line in data:
        par, child = re.search('.* ([A-Z]+) .* ([A-Z]+) .*', line).groups()
        if root is None:
            root = par
        try:
            graph[par].append(child)
        except KeyError:
            graph[par] = [child]

    # empty nodes
    nodes = set()
    for v in graph.values():
        nodes |= set(v)

    miss = nodes - set([k for k in graph.keys()])

    for m in miss:
        graph[m] = []

    return graph, root


def parents(node, graph):
    parents = set()
    for k, v in graph.items():
        if node in v:
            parents.add(k)

    return parents


if __name__ == "__main__":
    data = parseInput("input.txt")

#    data = ['Step C must be finished before step A can begin.',
#            'Step C must be finished before step F can begin.',
#            'Step A must be finished before step B can begin.',
#            'Step A must be finished before step D can begin.',
#            'Step B must be finished before step E can begin.',
#            'Step D must be finished before step E can begin.',
#            'Step F must be finished before step E can begin.']

    graph, root1 = buildGraph(data)

    roots = sc.SortedSet()

    for k in graph.keys():
        pars = parents(k, graph)
#        print(k, pars)
        if len(pars) == 0:
            roots.add(k)

    visited = []

    while len(roots) != 0:
        root = roots.__iter__().__next__()
        roots -= set(root)

        visited.append(root)

        for m in graph[root]:
            graph[root] = graph[root][1:]
            if len(parents(m, graph)) == 0:
                roots.add(m)

    print("".join(visited))

#2:
    graph, root1 = buildGraph(data)
    graph2, _ = buildGraph(data)

    roots = sc.SortedSet()

    for k in graph.keys():
        pars = parents(k, graph)
#        print(k, pars)
        if len(pars) == 0:
            roots.add(k)

    visited = []
    working = {}
    numworkers = 5
    duration = 0

    while len(roots) >= 0:
        if len(working) == 0:
            root = roots.__iter__().__next__()
            roots -= set(root)
            working[root] = ord(root) - 64 + 60

            for m in graph[root]:
                graph[root] = graph[root][1:]
                if len(parents(m, graph)) == 0:
                    roots.add(m)
        else:
            keys = tuple(working.keys())
#            for k, v in working.items():

            for k in keys:
                working[k] = working[k] - 1

                if working[k] <= 0:
                    visited.append(k)
                    del working[k]

#                    print(working, roots, root, visited)

#                    try:
#                        root = roots.__iter__().__next__()
#                    except:
#                        break
#
#                    roots -= set(root)
#                    working[root] = ord(root) - 64
#
#                    for m in graph[root]:
#                        graph[root] = graph[root][1:]
#                        if len(parents(m, graph)) == 0:
#                            roots.add(m)

#            print(working, roots, root, visited)

            i = 0
            itr = roots.__iter__()
            while i < len(roots) and len(working) < numworkers:
                try:
                    fakeroot = itr.__next__()
                except:
                    break

#                print(fakeroot)
                i += 1
#                print(parents(fakeroot, graph2), visited)
                if set(parents(fakeroot, graph2)).issubset(set(visited)):
                    root = fakeroot
                    roots -= set(fakeroot)
                    working[fakeroot] = ord(fakeroot) - 64 + 60
#                    print(working, roots, root, visited)
                    for m in graph[root]:
                        graph[root] = graph[root][1:]
                        if len(parents(m, graph)) == 0:
                            roots.add(m)


        print(working, roots, root, visited, duration, "\n")

        if len(working) <= 0:
#            print(working, roots, root, visited, "\n")
#            visited.append(root)
            break
        else:
            duration += 1

print("".join(visited))
print(duration)

#        root = roots.__iter__().__next__()
#        roots -= set(root)

#        visited.append(root)

#        for m in graph[root]:
#            graph[root] = graph[root][1:]
#            if len(parents(m, graph)) == 0:
#                roots.add(m)




#BFS solution attempt
#    allsols = dict()
#    lsols= []
#
#    for k in graph.keys():
#        print(k)
#        root = k
#
#        visited = []
#        seen = set()
#        queue = sc.SortedSet()
#        queue.add(root)
#
#    #    node = root
#        while len(queue) != 0:
#
#            if len(queue) == 1 and queue[0] == root:
#                node = queue[0]
#                visited.append(node)
#                queue = sc.SortedSet(queue[1:])
#
#                queue.update(graph[node])
#            else:
#                #tiebreakers
#                node = queue[0]
#                visited.append(node)
#
#                queue = sc.SortedSet(queue[1:])
#
#                #only add those that have all the parents visited
#                for n in graph[node]:
#
#                    pars = parents(n, graph)
#                    if pars.issubset(set(visited)):
#                        queue.add(n)
#
#                #remove from queue
#    #            if i == 0:
#    #                queue = sc.SortedSet(queue[i+1:])
#    #            elif i == len(queue)-1:
#    #                queue = sc.SortedSet(queue[:i])
#    #            else:
#    #                queue = sc.SortedSet(queue[:i] + queue[i+1:])
#
#    #            while i < len(queue):
#    #                parents = set()
#    #
#    #                for k, v in graph.items():
#    #                    if node in v:
#    #                        parents.add(k)
#    #
#    #                if (parents.intersection(seen)).issubset(set(visited)):
#    #                    break
#    #                else:
#    #                    i += 1
#
#            seen.add(node)
#            for g in graph[node]:
#                seen.add(g)
#
##        print(visited)
#        lsols.append(visited[:])
#        allsols[k] = visited[:]
#        print(allsols[k])
#
#
##    print("".join(visited))
#    print(allsols)
#
#    list(map(len, lsols))










