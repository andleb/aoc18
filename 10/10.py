# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 23:12:30 2018

@author: Andrej Leban
"""

import itertools as it
import functools as ft
import collections as coll

import sortedcontainers as sc
from blist import blist

import re

import scipy.signal
import scipy.sparse
import matplotlib.pyplot as plt

#re.search('@ (\d+),(\d+)', item).groups()))

def parseInput(inp):
    data = []
    with open(inp, 'r') as f:
        for line in f:
            data.append(line)

    return data


def consecutive_ones(sequence):
    def _consecutives():
        for itr in it.repeat(iter(sequence)):
            yield tuple(it.takewhile(lambda p: p == 1,
                                     it.dropwhile(lambda p: p != 1, itr)))
    return it.takewhile(lambda t: len(t), _consecutives())

def sames(sequence):
    def _same():
        for itr in it.repeat(iter(sequence)):
            yield tuple(it.takewhile(lambda p: p == 1,
                                     it.dropwhile(lambda p: p != 1, itr)))
    return it.takewhile(lambda t: len(t), _same())

if __name__ == "__main__":

    data = parseInput("input.txt")

#    data = ["position=< 9,  1> velocity=< 0,  2>",
#            "position=< 7,  0> velocity=<-1,  0>",
#            "position=< 3, -2> velocity=<-1,  1>",
#            "position=< 6, 10> velocity=<-2, -1>",
#            "position=< 2, -4> velocity=< 2,  2>",
#            "position=<-6, 10> velocity=< 2, -2>",
#            "position=< 1,  8> velocity=< 1, -1>",
#            "position=< 1,  7> velocity=< 1,  0>",
#            "position=<-3, 11> velocity=< 1, -2>",
#            "position=< 7,  6> velocity=<-1, -1>",
#            "position=<-2,  3> velocity=< 1,  0>",
#            "position=<-4,  3> velocity=< 2,  0>",
#            "position=<10, -3> velocity=<-1,  1>",
#            "position=< 5, 11> velocity=< 1, -2>",
#            "position=< 4,  7> velocity=< 0, -1>",
#            "position=< 8, -2> velocity=< 0,  1>",
#            "position=<15,  0> velocity=<-2,  0>",
#            "position=< 1,  6> velocity=< 1,  0>",
#            "position=< 8,  9> velocity=< 0, -1>",
#            "position=< 3,  3> velocity=<-1,  1>",
#            "position=< 0,  5> velocity=< 0, -1>",
#            "position=<-2,  2> velocity=< 2,  0>",
#            "position=< 5, -2> velocity=< 1,  2>",
#            "position=< 1,  4> velocity=< 2,  1>",
#            "position=<-2,  7> velocity=< 2, -2>",
#            "position=< 3,  6> velocity=<-1, -1>",
#            "position=< 5,  0> velocity=< 1,  0>",
#            "position=<-6,  0> velocity=< 2,  0>",
#            "position=< 5,  9> velocity=< 1, -2>",
#            "position=<14,  7> velocity=<-2,  0>",
#            "position=<-3,  6> velocity=< 2, -1>"]


    pos = []
    dpos = []

    #init
    for line in data:
#        try:
        y, x, dy, dx = tuple(map(int,
#                     re.search('position=< (\d+),\s*(\d+)>.*velocity=< (\d+),\s*(\d+)>.*',line).\
            re.search('position=<\s*([-,0-9]+)\s*,\s*([-,0-9]+)\s*>.*'
                      'velocity=<\s*([-,0-9]+)\s*,\s*([-,0-9]+)', line).\
                     groups()))
        pos.append((y,x))
        dpos.append((dy,dx))
#        except:
#            pass

    posy = np.array([t[1] for t in pos])
    posx = np.array([t[0] for t in pos])
    dposy = np.array([t[1] for t in dpos])
    dposx = np.array([t[0] for t in dpos])

#    sy = sorted(posy)
#    sx = sorted(posx)
#
#    offsety, sizy = sy[0], sy[-1] - sy[0] + 1
#    offsetx, sizx = sx[0], sx[-1] - sx[0] + 1
#
#    sizyO, sizxO = sizy, sizx
#    offsetyO, offsetxO = offsety, offsetx

#    pic = np.zeros((sizy, sizx))
#    pic = scipy.sparse.csc_matrix((sizy, sizx))

#    for y,x in zip(posy, posx):
#        pic[y-offsety, x-offsetx] = 1
#    print("\n\n\n",pic,"\n\n\n")

#    kernel = np.array([[-1,-1,2,-1,-1],
#                       [-1,-1,2,-1,-1],
#                       [-1,-1,2,-1,-1],
#                       [-1,-1,2,-1,-1],
#                       [-1,-1,2,-1,-1]
#                       ])

#    ret = scipy.signal.fftconvolve(pic, kernel, mode='valid')

#    metric = 0

    res = []
    critLx = 8
    critLy = 8


    i = 0
    while len(res) < 1:
        posy += dposy
        posx += dposx

#        sy = np.array(sorted(posy))
#        sx = np.array(sorted(posx))

#        offsety, sizy = sy[0], sy[-1] - sy[0] + 1
#        offsetx, sizx = sx[0], sx[-1] - sx[0] + 1

#        pic = np.zeros((sizyO, sizxO))
#        pic = scipy.sparse.csc_matrix((sizyO, sizxO))

#        for y,x in zip(posy, posx):
#            try:
#                pic[y-offsetyO, x-offsetxO] = 1
#            except:
#                pass


#        print("\n\n\n",pic,"\n\n\n")

        #line detection
#        ret = scipy.signal.fftconvolve(pic, kernel, mode='valid')
##        plt.imshow(ret)
#        newmetric = sum(ret[ret>0])
#        print(newmetric)
#
#        if newmetric > metric:
#            res.append((newmetric, pic))
#            metric = newmetric

        #y subsequence
#        sy = np.array(sy)
#        sx = np.array(sx)

#        diffy = sy[1:] - sy[:-1]
#        cons = [i for i in consecutive_ones(diffy)]
#        metric = max(list(map(len,cons)))
#        print(metric)


        # same xs, consy
        sor = sorted(zip(posx, posy))
        x = [t[0] for t in sor]
        y = [t[1] for t in sor]

        # seqs with same x
        samesx = sorted([list(l) for _,l in \
                         it.groupby(enumerate(x), key=lambda x:x[1])])

        #those that are over 3 long
        crit = list(filter(lambda x: len(x)>=critLx, samesx))
#        print(len(crit))

        #find consecutive ys
        # candidates
        succCands = []
        for cand in crit:
            ys = y[cand[0][0]:cand[-1][0]+1]
#                print(ys)
            ylen = 1
            ylens = []

            yprev = ys[0]
            succ = True

            for j in range(1, len(ys)):
                #ignore duplicates:
                if ys[j] == yprev:
                    continue

                if ys[j] - yprev == 1:
                    ylen += 1
                    yprev = ys[j]
                    continue
                else:
                    ylens.append(ylen)
                    ylen = 1
                    yprev = ys[j]

            ylens.append(ylen)

            succY = list(filter(lambda x: x >= critLy, ylens))
            if len(succY):
                succCands.append(cand)

        if len(succCands):
            print("found")
            res.append((i,succCands,sor))

        i += 1
        if not i % 100000:
            print(i)

#map(lambda x:x[0][0], # obtain the index of the first element
#    sorted([list(l) for _,l in itertools.groupby(enumerate(x), key=lambda x:x[1])],
#                 # create tuples with their indices
#        # group in value, not on index
#           key=lambda l: -len(l)))



    sor = res[0][2]
    sx, sy = zip(*sor)
    sy = sorted(sy)

    offsety, sizy = sy[0], sy[-1] - sy[0] + 1
    offsetx, sizx = sx[0], sx[-1] - sx[0] + 1

    pic = np.zeros((sizy, sizx))
    for x, y in res[0][2]:
        try:
            pic[y-offsety, x-offsetx] = 1
        except:
            pass
#
    print("\n\n\n",pic,"\n\n\n")







