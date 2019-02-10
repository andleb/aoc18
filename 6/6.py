# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 05:43:55 2018

@author: Andrej Leban
"""

import numpy as np

def parseInput(inp):
    data = []
    with open(inp, 'r') as f:
        for line in f:
            data.append(line)

    return data


if __name__ == "__main__":

    data = parseInput("input.txt")

    coors = []
    for line in data:
        coors.append(tuple(map(int, line.split(", "))))

#    coors = [ (1, 1),
#        (1, 6),
#        (8, 3),
#        (3, 4),
#        (5, 5),
#        (8, 9)]

    sx = sorted(coors, key=lambda t: t[0])
    sy = sorted(coors, key=lambda t: t[1])

    offsetx, sizx = sx[0][0], sx[-1][0] - sx[0][0] + 1
    offsety, sizy = sy[0][1], sy[-1][1] - sy[0][1] + 1


    #brute force

    mat = np.ones((sizy, sizx))
    mat *= -1
#    print(mat)

    coors2 = list(map(lambda t: (t[0] - offsetx, t[1] - offsety), coors))

    for x in range(sizx):
        for y in range(sizy):
#            print(x,y)
            minp = 1e16
            iMin = -1
            nTies = 0
            for i, (cx, cy) in enumerate(coors2):
#                print(x,y, i, cx, cy)
                newMin = abs(cx - x) + abs(cy - y)
                if newMin < minp:
                    minp = newMin
                    iMin = i
                    nTies = 0

                #tiebreak:
                elif newMin == minp:
#                    minp = 1e16
#                    iMin = -1
                    nTies += 1

            mat[y][x] = iMin if not nTies else -1

    bound = set((-1,)) | set(mat[0][:]) | set(mat[-1][:]) | set(mat[:][0]) | set(mat[:][-1])

    hist = np.zeros((len(coors2)+1,))

    for x in range(sizx):
        for y in range(sizy):
#            print(mat[x][y])
            hist[int(mat[y][x])] += 1

    hist = hist[:-1]

    maxI = -1
    ordr = []
    for m in np.argsort(hist)[::-1]:
        if m not in bound:
            ordr.append(m)

    # size
    print(hist[ordr[0]])

    matS = np.zeros((sizy, sizx))

    # region
    for x in range(sizx):
        for y in range(sizy):
            for i, (cx, cy) in enumerate(coors2):
                matS[y][x] += abs(cx - x) + abs(cy - y)

    print(len(matS[matS < 10000]))










