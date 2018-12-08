# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 07:02:47 2018

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

if __name__ == "__main__":

#    data = parseInput("input.txt")
#    data = data[0].split(" ")
#    data[-1] = data[-1][:-1]

    data = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'
    data = data.split(" ")

    data = list(map(int,data))

#def buildTree(data):

    tree = {}
    i = 0
    node = 0
    parent = None

    while i < len(data)-1:

        nChild = data[i]
        nMd = data[i+1]
        tree[node] = [(nChild, nMd), [], parent, []]

        if parent is not None:
            tree[parent][3].append(node)

        if nChild:
            parent = node

        node += 1
        i += 2
        if i >= len(data) - 2:
            break

        nChild = data[i]
        nMd = data[i+1]
        tree[node] = [(nChild, nMd), [], parent, []]

        tree[parent][3].append(node)

        i += 2

        if nChild:
            parent = node
            node += 1
        else:
            tree[node][1].extend(data[i:i+nMd])
#            print(tree[node])

            i += nMd

            oldNode = node

            #last child, recursively add metadata
            while (tree[parent][0][0] == len(tree[parent][3])\
                and node in tree[parent][3]):
#                and tree[parent][3][-1] == node):

                node = parent
                nMd = tree[node][0][1]

                tree[node][1].extend(data[i:i+nMd])

                i += nMd
                parent = tree[node][2]
                print(parent)
                print("")

                # root
                if tree[parent][2] is None:
                    nMd = tree[parent][0][1]
                    tree[parent][1].extend(data[i:i+nMd])
                    i += nMd
                    break

            node = oldNode + 1

#    return tree, i


#    tree, i = buildTree(data)
#    print(tree)


    for k,v in tree.items():
        if v[0][1] != len(v[1]):
            print("error", k, v)
        break

    mdsum = 0
    for k,v in tree.items():
#        print(k, v)
        mdsum += sum(v[1])

    print(mdsum)



















#    a = np.array(list(map(int,data)))
