# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 05:22:19 2018

@author: Andrej Leban
"""

import numpy as np

def parseInput(inp):
    data = []
    with open(inp, 'r') as f:
        for line in f:
            data.append(line[:-1])

    return data


sym2Int = {
      ' ': -1,
      '-': 0,
      '|': 1,
      '/': 2,
      '\\': 3,
      '+': 4
        }


def simulate(data, firstCrash=True):

    N = len(data[0])
    M = len(data)
    grid = np.ones((M, N)) * -1
    carts = []

    for i in range(M):
        for j in range(N):
            try:
                grid[i, j] = sym2Int[data[i][j]]
            except KeyError:
                if data[i][j] == '>':
                    carts.append([(i, j), (i, j - 1), 0])
                elif data[i][j] == '<':
                    carts.append([(i, j), (i, j + 1), 0])
                elif data[i][j] == '^':
                    carts.append([(i, j), (i + 1, j), 0])
                elif data[i][j] == 'v':
                    carts.append([(i, j), (i - 1, j), 0])
                else:
                    pass

    for cart in carts:
        i, j = cart[0]

        if data[i][j] == '>' or data[i][j] == '<':
            grid[i, j] = 0
            continue

        elif data[i][j] == '^' or data[i][j] == 'v':
            grid[i, j] = 1
            continue

        else:
            pass
    for cart in carts:
        i, j = cart[0]
        if grid[i, j] == -1:
            print("error")
    tick = 0
    carts = sorted(carts, key=lambda t: t[0])

    while tick < 100000000 and len(carts) > 1:
        removed = set()
        for k, cart in enumerate(carts):

            if k in removed:
                continue

            i, j = cart[0]
            previ, prevj = cart[1]

            # straight
            # -
            if grid[i, j] == 0:
                if prevj < j:
                    cart[0] = (i, j + 1)
                else:
                    cart[0] = (i, j - 1)

            # |
            if grid[i, j] == 1:
                if previ < i:
                    cart[0] = (i + 1, j)
                else:
                    cart[0] = (i - 1, j)

            # turn "/"
            if grid[i, j] == 2:
                if previ != i:
                    # right turn
                    if previ < i:
                        cart[0] = (i, j - 1)
                    else:
                        cart[0] = (i, j + 1)
                else:
                    # left turn
                    if prevj < j:
                        cart[0] = (i - 1, j)
                    else:
                        cart[0] = (i + 1, j)

            # turn "\"
            if grid[i, j] == 3:
                if previ != i:
                    # left turn
                    if previ < i:
                        cart[0] = (i, j + 1)
                    else:
                        cart[0] = (i, j - 1)
                else:
                    # right turn
                    if prevj < j:
                        cart[0] = (i + 1, j)
                    else:
                        cart[0] = (i - 1, j)

            # intersec
            if grid[i, j] == 4:
                lastI = cart[2]
                # left
                if lastI % 3 == 0:
                    if previ != i:
                        newI = i
                        newJ = j - 1 if previ > i else j + 1
                    else:
                        newJ = j
                        newI = i - 1 if prevj < j else i + 1
                    cart[0] = (newI, newJ)
                # straight
                elif lastI % 3 == 1:
                    if previ != i:
                        newJ = j
                        newI = i + 1 if previ < i else i - 1
                    else:
                        newI = i
                        newJ = j - 1 if prevj > j else j + 1
                    cart[0] = (newI, newJ)
                # right
                elif lastI % 3 == 2:
                    if previ != i:
                        newI = i
                        newJ = j - 1 if previ < i else j + 1
                    else:
                        newJ = j
                        newI = i + 1 if prevj < j else i - 1
                    cart[0] = (newI, newJ)

                cart[2] += 1

            cart[1] = (i, j)
            if cart[1] == cart[0]:
                print("error!")
                pass

            # remove collisions instantly
            collision = False
            for l, cart2 in enumerate(carts):
                if l == k:
                    continue

                if carts[k][0] == carts[l][0] and l not in removed:
                    collision = True
                    if firstCrash:
                        return carts[l]

                    removed.add(l)

            if collision:
                removed.add(k)

        carts2 = []
        for k, cart in enumerate(carts):
            if k not in removed:
                carts2.append(cart)
        carts = carts2
        carts = sorted(carts, key=lambda t: t[0])

        # print(tick, len(carts))
        tick += 1

    return carts


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

    carts = simulate(data, firstCrash=True)
    print(carts)

    carts = simulate(data, firstCrash=False)
    print(carts)




