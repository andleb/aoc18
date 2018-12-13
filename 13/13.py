# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 05:22:19 2018

@author: Andrej Leban
"""

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


sym2Int = { '-': 0,
      '|': 1,
      '/': 2,
      '\\': 3,
      '+': 4
        }




if __name__ == "__main__":

    data = parseInput("input.txt")

#    data =[
#r"/->-\        ",
#r"|   |  /----\\",
#r"| /-+--+-\  |",
#r"| | |  | v  |",
#r"\-+-/  \-+--/",
#r"  \------/   "]

#    data = [
#r'/>-<\  ',
#r'|   |  ',
#"| /<+-\\",
#r'| | | v',
#r'\>+</ |',
#r'  |   ^',
#r'  \<->/']


    N = len(data[0])
    M = len(data)

    grid = np.ones((M, N))*-1

    carts = []

    for i in range(M):
        for j in range(N):
            try:
                grid[i,j] = sym2Int[data[i][j]]
            except KeyError:
                #TODO: determine underlying track
                if data[i][j] == '>':
                    carts.append([(i, j), (i, j-1), 0])
                elif data[i][j] == '<':
                    carts.append([(i, j), (i, j+1), 0])
                elif data[i][j] == '^':
                    carts.append([(i, j), (i+1, j), 0])
                elif data[i][j] == 'v':
                    carts.append([(i, j), (i-1, j), 0])
                else:
                    pass

    for cart in carts:
        i,j = cart[0]
        print(cart)

        up = int(grid[max(i-1,0),j] >= 0)
        down = int(grid[min(i+1, M-1),j] >= 0)
        right = int(grid[i,max(j-1,0)] >= 0)
        left = int(grid[i,min(j+1,N-1)] >= 0)

#        if grid[i+1,j] >= 0 and grid[i,j+1] >= 0 and grid[i-1,j] >= 0 and grid[i,j-1] >= 0:
        if up + down + left + right >= 3 and\
            ((grid[i+1,j] == grid[i-1,j] and grid[i+1,j] >= 0) or\
             (grid[i,j+1] == grid[i,j-1]) and grid[i,j+1] >= 0):

            if (grid[i-1,j] == 1 and grid[i+1,j] == 1)\
                and ((grid[i,j+1] >= 0 and grid[i,j+1] != 1)\
                     or (grid[i,j-1] >= 0 and grid[i,j-1] != 1)):
                grid[i,j] = 4
                continue

            elif (grid[i,j+1] == 0 and grid[i,j-1] == 0)\
                and ((grid[i-1,j] >= 0 and grid[i-1,j] != 0) or\
                     (grid[i+1,j] >= 0 and grid[i+1,j] != 0)):

                grid[i,j] = 4
                continue
            elif (grid[i-1,j] + grid[i+1,j] + grid[i,j+1] + grid[i,j-1]) > 4 and\
                (grid[i-1,j] != 1 or grid[i+1,j] != 1 or grid[i,j+1] != 1 or grid[i,j-1] != 1):
                grid[i,j] = 4
                continue
            else:
                pass

        if data[i][j] == '>' or data[i][j] == '<':
            if (not i or grid[i-1,j] < 0 ) and (i==M-1 or grid[i+1,j] < 0):
                grid[i,j] = 0
                continue
            elif (grid[i-1,j] < 0 or not i) and (grid[i,j+1] < 0 or j==N-1) and (grid[i+1, j] == 1 or i==M-1):
                grid[i,j] = 3
                continue
            elif (grid[i+1,j] < 0 or i==M-1) and (grid[i,j+1] < 0 or j==N-1) and (grid[i-1, j] == 1 or not i) :
                grid[i,j] = 2
                continue
            else:
                grid[i,j] = 0
                continue
        elif data[i][j] == '^' or data[i][j] == 'v':
            if ( j==N-1 or grid[i,j+1] < 0) and (grid[i,j-1] < 0 or not j):
                grid[i,j] = 1
                continue
            elif (grid[i,j-1] < 0 or not j) and (grid[i-1,j] < 0 or not i) and (grid[i, j+1] == 0 or j==N-1):
                grid[i,j] = 2
                continue
            elif (grid[i-1,j] < 0 or not i) and (grid[i,j+1] < 0 or j==N-1) and (grid[i, j-1] == 0 or not j):
                grid[i,j] = 3
                continue
            else:
                grid[i, j] = 1
                continue
        else:
            pass


#    while not np.any([c[0] for c in carts])
    tick = 0
    carts = sorted(carts, key=lambda t: t[0])
    colision = False
    xcol, ycol = -1, -1

#    while tick < 1000 and not colision:
    while tick < 1000000 and len(carts)>1:
        for cart in carts:
            i,j = cart[0]
            previ, prevj = cart[1]

            #straight
            if grid[i,j] == 0:
                if prevj < j:
                    cart[0] = (i, j+1)
                else:
                    cart[0] = (i, j-1)

            if grid[i,j] == 1:
                if previ < i:
                    cart[0] = (i+1, j)
                else:
                    cart[0] = (i-1, j)

            #turn "/"
            if grid[i,j] == 2:
                if previ != i:
                    #right turn
                    if previ<i:
                        cart[0] = (i, j-1)
                    else:
                        cart[0] = (i, j+1)
                else:
                    if prevj<j:
                        cart[0] = (i-1, j)
                    else:
                        cart[0] = (i+1, j)

            #turn "\"
            if grid[i,j] == 3:
                if previ != i:
                    #left turn
                    if previ<i:
                        cart[0] = (i, j+1)
                    else:
                        cart[0] = (i, j-1)
                else:
                    if prevj<j:
                        cart[0] = (i+1, j)
                    else:
                        cart[0] = (i-1, j)

            #intersec
            if grid[i,j] == 4:
                lastI = cart[2]
                #left
                if lastI % 3 == 0:
                    if previ != i:
                        newI = i
                        newJ = j-1 if previ>i else j+1
                    else:
                        newJ = j
                        newI = i-1 if prevj<j else i+1
                    cart[0] = (newI, newJ)
                #straight
                elif lastI % 3 == 1:
                    if previ != i:
                        newJ = j
                        newI = i+1 if previ<i else i-1
                    else:
                        newI = i
                        newJ = j-1 if prevj>j else j+1
                    cart[0] = (newI, newJ)
                #right
                elif lastI % 3 == 2:
                    if previ != i:
                        newI = i
                        newJ = j-1 if previ<i else j+1
                    else:
                        newJ = j
                        newI = i+1 if prevj<j else i-1
                    cart[0] = (newI, newJ)

                cart[2] += 1

            cart[1] = (i,j)
            if cart[1] == cart[0]:
#                print("error!")
                pass

        grid2 = np.copy(grid)
        carts = sorted(carts, key=lambda t: t[0])
        removed = []
        for k in range(0, len(carts)-1):
            grid2[carts[k][0][0], carts[k][0][1]] = 100
            if carts[k][0] == carts[k+1][0]:
                colision = True
                xcol, ycol = carts[k][0][1], carts[k][0][0]
                removed.append(k)
                removed.append(k+1)

        carts2 = []
        for k, cart in enumerate(carts):
            if k not in removed:
                carts2.append(cart)
        carts = carts2

        grid2[carts[-1][0][0],carts[-1][0][1]] = 100

#        print('\n')
#        print(grid2)
#        print('\n')

        tick += 1


    print(carts)
#    print(colision, xcol, ycol)
    print(carts[0][0][1], carts[0][0][0])



