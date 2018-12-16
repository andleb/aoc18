# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 06:03:46 2018

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
            data.append(line)

    return data


def getSamples(data):
    inp, inst, outp = None, None, None
    samples = []

    for line in data:
        try:
            inp = re.search('Before:\s*\[(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\]\s*', line).groups()
        except:
            pass
        try:
            inst = re.search('(\d+)\s*(\d+)\s*(\d+)\s*(\d+)\s*', line).groups()
        except:
            pass
        try:
            outp = re.search('After:\s*\[(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\]\s*', line).groups()
        except:
            pass

        if inp is not None and inst is not None and outp is not None:
            samples.append(( tuple(map(int,inp)), tuple(map(int,inst)), tuple(map(int,outp))))
#            print(samples[-1])
            inp, inst, outp = None, None, None

    return samples

def addr(inp, inst):
    op, a, b, c = inst
    outp = list(inp)
    outp[c] = inp[a] + inp[b]
    return tuple(outp)

def addi(inp, inst):
    op, a, b, c = inst
    outp = list(inp)
    outp[c] = inp[a] + b
    return tuple(outp)

def mulr(inp, inst):
    op, a, b, c = inst
    outp = list(inp)
    outp[c] = inp[a] * inp[b]
    return tuple(outp)

def muli(inp, inst):
    op, a, b, c = inst
    outp = list(inp)
    outp[c] = inp[a] * b
    return tuple(outp)

def banr(inp, inst):
    op, a, b, c = inst
    outp = list(inp)
    outp[c] = inp[a] & inp[b]
    return tuple(outp)

def bani(inp, inst):
    op, a, b, c = inst
    outp = list(inp)
    outp[c] = inp[a] & b
    return tuple(outp)

def borr(inp, inst):
    op, a, b, c = inst
    outp = list(inp)
    outp[c] = inp[a] | inp[b]
    return tuple(outp)

def bori(inp, inst):
    op, a, b, c = inst
    outp = list(inp)
    outp[c] = inp[a] | b
    return tuple(outp)

def setr(inp, inst):
    op, a, b, c = inst
    outp = list(inp)
    outp[c] = inp[a]
    return tuple(outp)

def seti(inp, inst):
    op, a, b, c = inst
    outp = list(inp)
    outp[c] = a
    return tuple(outp)

def gtir(inp, inst):
    op, a, b, c = inst
    outp = list(inp)
    outp[c] = a > inp[b]
    return tuple(outp)

def gtri(inp, inst):
    op, a, b, c = inst
    outp = list(inp)
    outp[c] = inp[a] > b
    return tuple(outp)

def gtrr(inp, inst):
    op, a, b, c = inst
    outp = list(inp)
    outp[c] = inp[a] > inp[b]
    return tuple(outp)

def eqir(inp, inst):
    op, a, b, c = inst
    outp = list(inp)
    outp[c] = a == inp[b]
    return tuple(outp)

def eqri(inp, inst):
    op, a, b, c = inst
    outp = list(inp)
    outp[c] = inp[a] == b
    return tuple(outp)

def eqrr(inp, inst):
    op, a, b, c = inst
    outp = list(inp)
    outp[c] = inp[a] == inp[b]
    return tuple(outp)

ops = {
       'addr': addr,
       'addi': addi,
       'mulr': mulr,
       'muli': muli,
       'banr': banr,
       'bani': bani,
       'borr': borr,
       'bori': bori,
       'setr': setr,
       'seti': seti,
       'gtir': gtir,
       'gtri': gtri,
       'gtrr': gtrr,
       'eqir': eqir,
       'eqri': eqri,
       'eqrr': eqrr
       }



if __name__ == "__main__":

    data = parseInput("input.txt")

    samp = getSamples(data)

    nThree = []

    for s in samp:
        matches = []
        inp, inst, outp = s

        for opcode, op in ops.items():
#            print(opcode, inp, inst, outp, op(inp, inst), outp == op(inp, inst))
            if outp == op(inp, inst):
                matches.append(opcode)

        if len(matches) >=3:
            nThree.append([(s, matches)])

#    print(nThree)
    print(len(nThree))

