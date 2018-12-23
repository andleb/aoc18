# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 06:01:54 2018

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


def getSamples(data):

    samples = []
    for line in data:
            x, y, z, r = re.search(
            '\s*pos\s*=\s*<\s*([+-]?\d+)\s*,\s*([+-]?\d+)\s*,\s*([+-]?\d+)\s*>\s*,\s*r\s*=\s*([+-]?\d+)\s*', line).groups()
            samples.append(tuple(map(int,(x,y,z,r))))

    return samples

def mht(a):
    return int(np.round(np.sum(np.abs(a))))

def combinations_recursive_inner(n, buf, gaps, sm, accum):
  if gaps == 0:
    accum.append(buf)
  else:
    for x in range(-n, n+1):
        if sm + abs(x) + (gaps - 1) * n < n:
            continue
        if not sm + abs(x) > n:
            combinations_recursive_inner(n, buf + [x], gaps - 1, sm + abs(x), accum)

def combinations_recursive(n, npoints=3):
  accum = []
  combinations_recursive_inner(n, [], npoints, 0, accum)
  return np.array(accum)

if __name__ == "__main__":

    data = parseInput("input.txt")

#    data =[\
#'pos=<0,0,0>, r=4',
#'pos=<1,0,0>, r=1',
#'pos=<4,0,0>, r=3',
#'pos=<0,2,0>, r=1',
#'pos=<0,5,0>, r=3',
#'pos=<0,0,3>, r=1',
#'pos=<1,1,1>, r=1',
#'pos=<1,1,2>, r=1',
#'pos=<1,3,1>, r=1']

#    data = [
#'pos=<10,12,12>, r=2',
#'pos=<12,14,12>, r=2',
#'pos=<16,12,12>, r=4',
#'pos=<14,14,14>, r=6',
#'pos=<50,50,50>, r=200',
#'pos=<10,10,10>, r=5']

    samples = getSamples(data)

    #1
#    ssam = sorted(samples, key=lambda t: -t[3])
#    r = ssam[0][3]
#
#    coors = np.array([t[:3] for t in ssam])
#
#    coorsn = coors - coors[0]
#    dists = np.sum(np.vectorize(abs)(coorsn), axis=1)
#    print(np.sum(dists<=r))
#    print('\n')


    #2
#    minX = min(coors, key=lambda t:t[0])[0]
#    minY = min(coors, key=lambda t:t[1])[1]
#    minZ = min(coors, key=lambda t:t[2])[2]
#
#    maxX = max(coors, key=lambda t:t[0])[0]
#    maxY = max(coors, key=lambda t:t[1])[1]
#    maxZ = max(coors, key=lambda t:t[2])[2]

    #get number of other bots in range of bot
    samples = np.array(samples)
    crs = []
    inrang = []
    for i, robot in enumerate(samples):
        # ignore self? NO!
        coorsn = samples[:, :3] - robot[:3]
        crs.append(coorsn)
        dists = np.sum(np.vectorize(abs)(coorsn), axis=1)

        cmbdist = (robot[3] + samples[:, 3])
        cmbdist[i] = robot[3]

        inrang.append((i, np.sum(dists <= cmbdist), samples[dists <= cmbdist]))

    inrang = sorted(inrang, key=lambda x: -x[1])

    # only check the most likely bots
    # get the point in range of most others

    maxR = inrang[0][1]
    i = 0
    res = []

    # all diffs to +-2 manhattan neighs
    neighbors = np.concatenate((combinations_recursive(1),
                               combinations_recursive(2)))
    neighborsbp = np.concatenate((neighbors,
                                 combinations_recursive(3)))

    while inrang[i][1] == maxR:

        j = inrang[i][0]
        robot = samples[j]
        x,y,z,r = robot
        othrs = np.concatenate((inrang[i][2][:j], inrang[i][2][j+1:]))

        # normalized others
        # self excluded!
        othrsn = np.zeros(othrs.shape, dtype=int)
        othrsn[:,:3] = (othrs[:, :3] - robot[:3]).astype(int)
        othrsn[:,3] = othrs[:, 3]

        pts = {}
        orig = np.array([x, y, z])

        for robotO in othrsn:
            b = robotO[:3]
#            print(robotO)
            # robot is in 0,0,0
            direc = b
            rb = robotO[3]
            siz = np.sum(np.abs(direc))

            # boundary is capped at the radius or at the other robot
            bp = np.round(min(mht(b), r) * direc/siz).astype(int)

            # boundary outside the ranges
            if rb - mht(bp-b) < 0 or mht(bp) > r:

                #check neighbours up to 3 away
                for (k,l,m) in neighborsbp:
                    neigh = bp + (k,l,m)
                    if mht(neigh-b) <= rb and mht(neigh) <= r:
                        bp = neigh
                        break

            # find commonpoints from boundary
            if rb - mht(bp-b) >= 0 or mht(bp) <= r:
                commonpts = {tuple(bp)}
                queue = coll.deque([bp])

                while queue:
                    pt = queue.pop()

                    for (k,l,m) in neighbors:
                        neigh = pt + (k,l,m)
#                        print(neigh)
                        if mht(neigh-b) <= rb and mht(neigh) <= r:
                            if tuple(neigh) not in commonpts:
                                queue.append(neigh)
                            commonpts.add(tuple(neigh))

#                print(robot, orig+b, commonpts)
            # walk towards origin while still in range of b
#            while rbp <= rb - mht(bp-b) and (rbp - mht(bp)) <= r:
#                print(robot, pt + b, rbp)
#
#                isoOrig = isoOrigs[abs(mht(bp) - rbp)]
#
#                # points that are same dist from both
#                isob = b[:3] + combinations_recursive(mht(bp-b) + rbp, 3)

#                commonpts = isob[np.all(np.isin(isob, isoOrig), axis=1)]
#                commonpts = set(map(tuple,isob)) & set(map(tuple, isoOrig))

                for x,y,z in commonpts:
                    try:
                        pts[tuple(orig + (x, y, z))] += 1
                    except KeyError:
                        pts[tuple(orig + (x, y, z))] = 1

#                rbp += 1

        # add self
        for pt in pts.keys():
            pts[pt] += 1


        pts2 = sorted(pts.items(), key=lambda t: (-t[1], t[0]))
        maxpt = pts2[0]
        print(maxpt)
        distmaxpt = np.sum(np.vectorize(abs)(maxpt[0]))
        print(distmaxpt)
        print('\n\n')
#        res.append((i, maxpt, pts2))
        res.append((i, maxpt, pts2))

        i += 1


#print(sorted([x[1] for x in res], key=lambda x: -x[0]))


























#brute force
##
#    pts = {}
#
#    for x, y, z, r in ssam:
#
#        try:
#            pts[(x,y,z)] += 1
#        except KeyError:
#            pts[(x,y,z)] = 1
#
#        for dx in range(-r, r+1):
#            for dy in range(-r+abs(dx), r-abs(dx)+1):
#                for dz in range(-r+(abs(dx)+abs(dy)), r-(abs(dx)+abs(dy)) + 1):
#                    try:
#                        pts[(x+dx, y+dy, z+dz)] += 1
#                    except KeyError:
#                        pts[(x+dx, y+dy, z+dz)] = 1
#
#
#    maxpt = max(pts.items(), key=operator.itemgetter(1))
#    print(maxpt)
#    print(maxpt[0])
#    distmaxpt = np.sum(np.vectorize(abs)(maxpt[0]))
#    print(distmaxpt)

