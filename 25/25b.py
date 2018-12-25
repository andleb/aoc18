# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 05:38:13 2018

@author: Andrej Leban
"""

import copy
import itertools as it
import functools as ft
import collections as coll
import operator

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

def mht(a):
    return int(np.round(np.sum(np.abs(a))))

if __name__ == "__main__":

    inp = parseInput("input.txt")
    data = []

    regex = re.compile(r"\s*([+-]*\d+)\s*,\s*([+-]*\d+)\s*,\s*([+-]*\d+)\s*,\s*([+-]*\d+)\s*")
    for i, line in enumerate(inp):
       groups = re.search(regex, line).groups()
       data.append(np.array(tuple(map(int, groups))))


#    data =[\
#(0,0,0,0),
#(3,0,0,0),
#(0,3,0,0),
#(0,0,3,0),
#(0,0,0,3),
#(0,0,0,6),
#(9,0,0,0),
#(12,0,0,0)]

#    data = [\
#(-1,2,2,0),
#(0,0,2,-2),
#(0,0,0,-2),
#(-1,2,0,0),
#(-2,-2,-2,2),
#(3,0,2,-1),
#(-1,3,2,2),
#(-1,0,-1,0),
#(0,2,1,-2),
#(3,0,0,0)]

#    data = [\
#(1,-1,0,1),
#(2,0,-1,0),
#(3,2,-1,0),
#(0,0,3,1),
#(0,0,-1,-1),
#(2,3,-2,0),
#(-2,2,0,0),
#(2,-2,0,-1),
#(1,-1,0,-1),
#(3,2,0,2)]

#    data = [\
#(1,-1,-1,-2),
#(-2,-2,0,1),
#(0,2,1,3),
#(-2,3,-2,1),
#(0,2,3,-2),
#(-1,-1,1,-2),
#(0,-2,-1,0),
#(-2,2,3,-1),
#(1,2,2,0),
#(-1,-2,0,-2)]

    eps = 3
    minPts = 1

    data = np.array(data)

#    cores = []
#    for i, pt in enumerate(data):
#
#        numNeighs = 0
#
#        for j, othrpt in enumerate(data):
#
#            if i == j:
#                continue
#
#            if mht(othrpt - pt) <= eps:
#                numNeighs += 1
#
#        print(pt, numNeighs)
#        if numNeighs >= minPts:
#            cores.append(pt)

    # find connected components of cores
    ccomp = {}

    for s, source in enumerate(data):
        queue = coll.deque([source])
        seen = set()

        # if in any existing cc, break, else let it discover
        alreadyCC = False
        for ccomps in ccomp.values():
            if tuple(source) in ccomps:
                alreadyCC = True
                break
        if alreadyCC:
            continue

        while queue:
            pt = queue.popleft()


            for i, corePt in enumerate(data):
                if np.all(corePt == pt):
                    continue
                if mht(corePt - pt) <= eps and tuple(corePt) not in seen:
#                    print(pt, corePt, mht(corePt - pt))
                    queue.append(corePt)
                    seen.add(tuple(corePt))

        if len(seen):
            ccomp[tuple(source)] = seen

#    #compact the ccomps:
    clusters = set([frozenset(x) for x in ccomp.values()])
#    print('\n')
##    print(clusters)
#    print(len(clusters))

    #which is not in clusters?
#    clusters2 = clusters.copy()
    outside = []
    for i, pt in enumerate(data):
        found = False
        for cluster in clusters:
            if tuple(pt) in cluster:
                found = True

        if not found:
            outside.append(pt)
            clusters.add(frozenset([tuple(pt)]))

    print('\n')
#    print(outside)
    print(len(data) - sum(list(map(len, clusters))))

    print('\n')
#    print(clusters2)
    print(len(clusters))



    #Assign each non-core point to a nearby cluster

#    for i, pt in enumerate(data):
#
#        if tuple(pt) in ccomp.keys():
#            continue
#
#        nearestCl = None
#        nearestDist = 0
#
#        if mht()
#    for source, clust in ccomp.items():












