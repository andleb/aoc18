# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 06:01:54 2018

@author: Andrej Leban
"""

import numpy as np

import re


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
            '\s*pos\s*=\s*<\s*([+-]?\d+)\s*,\s*([+-]?\d+)\s*,\s*([+-]?\d+)\s*>\s*'
                ',\s*r\s*=\s*([+-]?\d+)\s*', line).groups()
            samples.append(tuple(map(int, (x, y, z, r))))

    return samples


def mht(a):
    return np.round(np.sum(np.abs(a)))


def combinations_recursive_inner(n, buf, gaps, sm, accum):
    if gaps == 0:
        accum.append(buf)
    else:
        for x in range(-n, n + 1):
            if sm + abs(x) + (gaps - 1) * n < n:
                continue
            if not sm + abs(x) > n:
                combinations_recursive_inner(n, buf + [x], gaps - 1, sm + abs(x), accum)


def combinations_recursive(n, npoints=3):
    accum = []
    combinations_recursive_inner(n, [], npoints, 0, accum)
    return np.array(accum)


def bisect(samples):

    xs = samples[:, 0]
    ys = samples[:, 0]
    zs = samples[:, 0]

    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    minz, maxz = min(zs), max(zs)
    dx = maxx - minx
    dx = dx // 2
    dy = maxy - miny
    dy = dy // 2
    dz = maxz - minz
    dz = dz // 2

    highx = maxx
    lowx = minx
    highy = maxy
    lowy = miny
    highz = maxz
    lowz = minz

    best_count = 0
    best_dist = 1e128
    bestpt = None
    neighs = combinations_recursive(3)
    neighs = neighs[~np.any(np.abs(neighs) > 1, axis=1)]

    while dx > 1 or dy > 1 or dz > 1:

        d = np.array([dx, dy, dz])
        midpt = np.array([(highx + lowx) // 2, (highy + lowy) // 2,
                          (highz + lowz) // 2])
        radbox = np.sum(d // 2)

        best_count = 0
        best_dist = 1e128
        bestpt = None
        for n in neighs:
            count = 0
            pt = midpt + d * n

            for robot in samples:
                xb, yb, zb, rb = robot
                if mht(pt - robot[:3]) <= (rb + radbox):
                    count += 1

            tiebreak = (count == best_count and mht(pt) < best_dist)
            if count > best_count or tiebreak:
                best_count = count
                best_dist = mht(pt)
                bestpt = pt

        lowx, lowy, lowz = bestpt - d
        highx, highy, highz = bestpt + d
        dx = dx // 2
        dy = dy // 2
        dz = dz // 2

    midpt = np.array([(highx + lowx) // 2, (highy + lowy) // 2,
                      (highz+lowz) // 2])
    return midpt


if __name__ == "__main__":

    data = parseInput("input.txt")

### EXAMPLES
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

### 1
    ssam = sorted(samples, key=lambda t: -t[3])
    r = ssam[0][3]

    coors = np.array([t[:3] for t in ssam])

    coorsn = coors - coors[0]
    dists = np.sum(np.vectorize(abs)(coorsn), axis=1)
    print(np.sum(dists <= r))
    print('\n')

### 2

    #get number of other bots in range of bot
    samples = np.array(samples)
    pt = bisect(samples)
    print(pt, mht(pt))


### previus algo, correct but too slow

#    crs = []
#    inrang = []
#    for i, robot in enumerate(samples):
#        # ignore self? NO!
#        coorsn = samples[:, :3] - robot[:3]
#        crs.append(coorsn)
#        dists = np.sum(np.vectorize(abs)(coorsn), axis=1)
#
#        cmbdist = (robot[3] + samples[:, 3])
#        cmbdist[i] = robot[3]
#
#        inrang.append((i, np.sum(dists <= cmbdist), samples[dists <= cmbdist]))
#
#    inrang = sorted(inrang, key=lambda x: -x[1])
#
#    # only check the most likely bots
#    # get the point in range of most others
#
#    maxR = inrang[0][1]
#    i = 0
#    res = []
#
#    # all diffs to +-2 manhattan neighs
#    neighbors = np.concatenate((combinations_recursive(1),
#                               combinations_recursive(2)))
#    neighborsbp = np.concatenate((neighbors,
#                                 combinations_recursive(3)))
#
#    while inrang[i][1] == maxR:
#
#        j = inrang[i][0]
#        robot = samples[j]
#        x,y,z,r = robot
#        othrs = np.concatenate((inrang[i][2][:j], inrang[i][2][j+1:]))
#
#        # normalized others
#        # self excluded!
#        othrsn = np.zeros(othrs.shape, dtype=int)
#        othrsn[:,:3] = (othrs[:, :3] - robot[:3]).astype(int)
#        othrsn[:,3] = othrs[:, 3]
#
#        pts = {}
#        orig = np.array([x, y, z])
#
#        for robotO in othrsn:
#            # radical line
#
#
#
#            b = robotO[:3]
##            print(robotO)
#            # robot is in 0,0,0
#            direc = b
#            rb = robotO[3]
#            siz = np.sum(np.abs(direc))
#
#            # boundary is capped at the radius or at the other robot
#            bp = np.round(min(mht(b), r) * direc/siz).astype(int)
#
#            # boundary outside the ranges
#            if rb - mht(bp-b) < 0 or mht(bp) > r:
#
#                #check neighbours up to 3 away
#                for (k,l,m) in neighborsbp:
#                    neigh = bp + (k,l,m)
#                    if mht(neigh-b) <= rb and mht(neigh) <= r:
#                        bp = neigh
#                        break
#
#            # find commonpoints from (potentialy new) boundary point
#            if rb - mht(bp-b) >= 0 and mht(bp) <= r:
#                commonpts = {tuple(bp)}
#                queue = coll.deque([bp])
#
#                while queue:
#                    pt = queue.pop()
#                                #up to 2 away
#                    for (k,l,m) in neighbors:
#                        neigh = pt + (k,l,m)
##                        print(neigh)
#                        if mht(neigh-b) <= rb and mht(neigh) <= r:
#                            if tuple(neigh) not in commonpts:
#                                queue.append(neigh)
#                                commonpts.add(tuple(neigh))
#
##                print(robot, orig+b, commonpts)
#
#                for x,y,z in commonpts:
#                    try:
#                        pts[tuple(orig + (x, y, z))] += 1
#                    except KeyError:
#                        pts[tuple(orig + (x, y, z))] = 1
#
#
#        # add self
#        for pt in pts.keys():
#            pts[pt] += 1
#
#
#        pts2 = sorted(pts.items(), key=lambda t: (-t[1], t[0]))
#        maxpt = pts2[0]
#        print(maxpt)
#        distmaxpt = np.sum(np.vectorize(abs)(maxpt[0]))
#        print(distmaxpt)
#        print('\n\n')
##        res.append((i, maxpt, pts2))
#        res.append((i, maxpt, pts2))
#
#        i += 1


#print(sorted([x[1] for x in res], key=lambda x: -x[0]))



### brute force
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


