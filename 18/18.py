# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 06:07:25 2018

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

def parseInput(inp):
    data = []
    with open(inp, 'r') as f:
        for line in f:
            data.append(line[:-1])

    return data

def printGrid(grid):

    res = np.chararray(grid.shape, itemsize=1, unicode=True)
    res[grid==0] = '.'
    res[grid==-1] = '|'
    res[grid==1] = '#'
    print(res)
    return res

sym2Int = {
      '.': 0,
      '|': -1,
      '#': 1,
        }


if __name__ == "__main__":

    data = parseInput("input.txt")

#    data =\
#['.#.#...|#.',
#'.....#|##|',
#'.|..|...#.',
#'..|#.....#',
#'#.#|||#|#|',
#'...#.||...',
#'.|....|...',
#'||...#|.#|',
#'|.||||..|.',
#'...#.|..|.']


    N = len(data[0])
    M = len(data)

    grid = np.zeros((M, N))*-1

    for i in range(M):
        for j in range(N):
            grid[i,j] = sym2Int[data[i][j]]

    n = 0
    rvs = []
    #TODO: edges
    while n < 50000:
#        print('\n', n)
#        printGrid(grid)

        newGrid = grid.copy()

        for i in range(1,M-1):
            for j in range(1,N-1):
                if grid[i,j] == 0:
                    if np.sum(grid[i-1:i+2, j-1:j+2] < 0) >= 3:
                        newGrid[i,j] = -1

                elif grid[i,j] == -1:
                    if np.sum(grid[i-1:i+2, j-1:j+2] > 0) >= 3:
                        newGrid[i,j] = 1

                elif grid[i,j] == 1:
                    if not ((np.sum(grid[i-1:i+2, j-1:j+2] > 0) >= 2)\
                        and (np.sum(grid[i-1:i+2, j-1:j+2] < 0) >= 1)):
                        newGrid[i,j] = 0
                else:
                    raise RuntimeError

        #edge points
        #top band
        i = 0
        for j in range(1, N-1):
            if grid[i,j] == 0:
                if np.sum(grid[i:i+2, j-1:j+2] < 0) >= 3:
                    newGrid[i,j] = -1

            elif grid[i,j] == -1:
                if np.sum(grid[i:i+2, j-1:j+2] > 0) >= 3:
                    newGrid[i,j] = 1

            elif grid[i,j] == 1:
                if not ((np.sum(grid[i:i+2, j-1:j+2] > 0) >= 2)\
                    and (np.sum(grid[i:i+2, j-1:j+2] < 0) >= 1)):
                    newGrid[i,j] = 0
            else:
                raise RuntimeError

        #bottom band
        i = M-1
        for j in range(1, N-1):
            if grid[i,j] == 0:
                if np.sum(grid[i-1:i+1, j-1:j+2] < 0) >= 3:
                    newGrid[i,j] = -1

            elif grid[i,j] == -1:
                if np.sum(grid[i-1:i+1, j-1:j+2] > 0) >= 3:
                    newGrid[i,j] = 1

            elif grid[i,j] == 1:
                if not ((np.sum(grid[i-1:i+1, j-1:j+2] > 0) >= 2)\
                    and (np.sum(grid[i-1:i+1, j-1:j+2] < 0) >= 1)):
                    newGrid[i,j] = 0
            else:
                raise RuntimeError

        #left band
        j = 0
        for i in range(1, M-1):
            if grid[i,j] == 0:
                if np.sum(grid[i-1:i+2, j:j+2] < 0) >= 3:
                    newGrid[i,j] = -1

            elif grid[i,j] == -1:
                if np.sum(grid[i-1:i+2, j:j+2] > 0) >= 3:
                    newGrid[i,j] = 1

            elif grid[i,j] == 1:
                if not ((np.sum(grid[i-1:i+2, j:j+2] > 0) >= 2)\
                    and (np.sum(grid[i-1:i+2, j:j+2] < 0) >= 1)):
                    newGrid[i,j] = 0
            else:
                raise RuntimeError

        #right band
        j = N-1
        for i in range(1, M-1):
            if grid[i,j] == 0:
                if np.sum(grid[i-1:i+2, j-1:j+1] < 0) >= 3:
                    newGrid[i,j] = -1

            elif grid[i,j] == -1:
                if np.sum(grid[i-1:i+2, j-1:j+1] > 0) >= 3:
                    newGrid[i,j] = 1

            elif grid[i,j] == 1:
                if not ((np.sum(grid[i-1:i+2, j-1:j+1] > 0) >= 2)\
                    and (np.sum(grid[i-1:i+2, j-1:j+1] < 0) >= 1)):
                    newGrid[i,j] = 0
            else:
                raise RuntimeError

        #corners
        i, j = 0, 0
        if grid[i,j] == 0:
            if np.sum(grid[i:i+2, j:j+2] < 0) >= 3:
                newGrid[i,j] = -1

        elif grid[i,j] == -1:
            if np.sum(grid[i-1:i+2, j-1:j+1] > 0) >= 3:
                newGrid[i,j] = 1

        elif grid[i,j] == 1:
            if not ((np.sum(grid[i:i+2, j:j+2] > 0) >= 2)\
                and (np.sum(grid[i:i+2, j:j+2] < 0) >= 1)):
                newGrid[i,j] = 0
        else:
            raise RuntimeError

        i, j = 0, N-1
        if grid[i,j] == 0:
            if np.sum(grid[i:i+2, j-1:j+1] < 0) >= 3:
                newGrid[i,j] = -1

        elif grid[i,j] == -1:
            if np.sum(grid[i:i+2, j-1:j+1] > 0) >= 3:
                newGrid[i,j] = 1

        elif grid[i,j] == 1:
            if not ((np.sum(grid[i:i+2, j-1:j+1] > 0) >= 2)\
                and (np.sum(grid[i:i+2, j-1:j+1] < 0) >= 1)):
                newGrid[i,j] = 0
        else:
            raise RuntimeError

        i, j = M-1, 0
        if grid[i,j] == 0:
            if np.sum(grid[i-1:i+1, j:j+2] < 0) >= 3:
                newGrid[i,j] = -1

        elif grid[i,j] == -1:
            if np.sum(grid[i-1:i+1, j:j+2] > 0) >= 3:
                newGrid[i,j] = 1

        elif grid[i,j] == 1:
            if not ((np.sum(grid[i-1:i+1, j:j+2] > 0) >= 2)\
                and (np.sum(grid[i-1:i+1, j:j+2] < 0) >= 1)):
                newGrid[i,j] = 0
        else:
            raise RuntimeError

        i, j = M-1, N-1
        if grid[i,j] == 0:
            if np.sum(grid[i-1:i+1, j-1:j+1] < 0) >= 3:
                newGrid[i,j] = -1

        elif grid[i,j] == -1:
            if np.sum(grid[i-1:i+1, j-1:j+1] > 0) >= 3:
                newGrid[i,j] = 1

        elif grid[i,j] == 1:
            if not ((np.sum(grid[i-1:i+1, j-1:j+1] > 0) >= 2)\
                and (np.sum(grid[i-1:i+1, j-1:j+1] < 0) >= 1)):
                newGrid[i,j] = 0
        else:
            raise RuntimeError

        grid = newGrid.copy()
        rv = np.sum(grid < 0) * np.sum(grid>0)
        rvs.append(rv)
#        if n > 3:
#            print(n, rv, rvs[-3:], rv - rvs[-2])

        n += 1
        if not n % 100:
            print(n)

    print('\n')
#    printGrid(newGrid)
    print('\n', np.sum(grid < 0) * np.sum(grid>0))


    npermin = np.floor((1e9-minstot[0][-1])/per)
    lastmin = minstot[0][-1] + npermin*per
    diffmin = int(1e9 - lastmin)
    ansmin = rvs[minstot[0][-2]:][diffmin]

    npermax = np.floor((1e9-maxestot[0][-1])/per)
    lastmax = maxestot[0][-1] + npermax*per
    diffmax = int(1e9 - lastmax)
    ansmax = rvs[maxestot[0][-2]:][diffmax]

    nperl = (1e9-10000)/per
    lastsame = 9999 + int(nperl*per)






