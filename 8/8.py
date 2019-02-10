# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 07:02:47 2018

@author: Andrej Leban
"""

def parseInput(inp):
    data = []
    with open(inp, 'r') as f:
        for line in f:
            data.append(line)

    return data

tot = 0

def value(node):
    global tot

    if not len(tree[node][3]):
        tot += sum(tree[node][1])
    else:
        for mdInd in tree[node][1]:
            try:
                child = tree[node][3][mdInd-1]
                value(child)
            except IndexError:
                pass

if __name__ == "__main__":

    data = parseInput("input.txt")
    data = data[0].split(" ")
    data[-1] = data[-1][:-1]

#    data = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'
#    data = data.split(" ")

    data = list(map(int,data))

    tree = {}
    i = 0
    node = 0
    parent = None

    while i < len(data):

        nChild = data[i]
        nMd = data[i+1]
        tree[node] = [(nChild, nMd), [], parent, []]

        if parent is not None:
            tree[parent][3].append(node)

        i += 2

        if nChild:
            parent = node
            node += 1
            continue

        oldNode = node
        while nChild  == len(tree[node][3]):

            nMd = tree[node][0][1]
            parent = tree[node][2]

            tree[node][1].extend(data[i:i+nMd])
            i += nMd

            node = parent
            if node is None:
                break
            nChild = tree[node][0][0]

        node = oldNode + 1

    for k,v in tree.items():
        if v[0][1] != len(v[1]):
            print("error", k, v)
        break

    mdsum = 0
    for k,v in tree.items():
#        print(k, v)
        mdsum += sum(v[1])

    print(mdsum)

    value(0)
    print(tot)

