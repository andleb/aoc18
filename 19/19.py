# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 05:46:54 2018

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

def ip(inp, inst):
    global g_ip

    g_ip = inst[0]

    return g_ip

def parseInput(inp):
    data = []
    with open(inp, 'r') as f:
        for line in f:
            data.append(line)

    return data

def addr(inp, inst):
    a, b, c = inst
    outp = list(inp)
    outp[c] = inp[a] + inp[b]
    return outp

def addi(inp, inst):
    a, b, c = inst
    outp = list(inp)
    outp[c] = inp[a] + b
    return outp

def mulr(inp, inst):
    a, b, c = inst
    outp = list(inp)
    outp[c] = inp[a] * inp[b]
    return outp

def muli(inp, inst):
    a, b, c = inst
    outp = list(inp)
    outp[c] = inp[a] * b
    return outp

def banr(inp, inst):
    a, b, c = inst
    outp = list(inp)
    outp[c] = inp[a] & inp[b]
    return outp

def bani(inp, inst):
    a, b, c = inst
    outp = list(inp)
    outp[c] = inp[a] & b
    return outp

def borr(inp, inst):
    a, b, c = inst
    outp = list(inp)
    outp[c] = inp[a] | inp[b]
    return outp

def bori(inp, inst):
    a, b, c = inst
    outp = list(inp)
    outp[c] = inp[a] | b
    return outp

def setr(inp, inst):
    a, b, c = inst
    outp = list(inp)
    outp[c] = inp[a]
    return outp

def seti(inp, inst):
    a, b, c = inst
    outp = list(inp)
    outp[c] = a
    return outp

def gtir(inp, inst):
    a, b, c = inst
    outp = list(inp)
    outp[c] = int(a > inp[b])
    return outp

def gtri(inp, inst):
    a, b, c = inst
    outp = list(inp)
    outp[c] = int(inp[a] > b)
    return outp

def gtrr(inp, inst):
    a, b, c = inst
    outp = list(inp)
    outp[c] = int(inp[a] > inp[b])
    return outp

def eqir(inp, inst):
    a, b, c = inst
    outp = list(inp)
    outp[c] = int(a == inp[b])
    return outp

def eqri(inp, inst):
    a, b, c = inst
    outp = list(inp)
    outp[c] = int(inp[a] == b)
    return outp

def eqrr(inp, inst):
    a, b, c = inst
    outp = list(inp)
    outp[c] = int(inp[a] == inp[b])
    return outp


ops = {
       '#ip': ip,
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


def getProgram(data):
    program = []

    for line in data:
        try:
            op, a, b, c = re.search('(\w+)\s*(\d+)\s*(\d+)\s*(\d+)\s*', line).groups()
            program.append((op, ) + tuple(map(int, (a,b,c))))
        except:
            op, ipP = re.search('(#\w+)\s*(\d+)\s*', line).groups()
            program.append((op, ) + tuple(map(int, (ipP, ))) + (0,0,))

    return program


if __name__ == "__main__":
    global g_ip

    data = parseInput("input.txt")

#'#ip 0',
#    data = [\
#'seti 5 0 1',
#'seti 6 0 2',
#'addi 0 1 0',
#'addr 1 2 3',
#'setr 1 0 0',
#'seti 8 0 4',
#'seti 9 0 5']

    program = getProgram(data)

    registers = [1,0,0,0,0,0]
    newregisters = [1,0,0,0,0,0]

#    nipchanges = 0
    g_ip = 3
    valip = 0

    niter = 0

    while valip in range(0, len(program)):
        op, a, b, c = program[valip]

#        if op == '#ip':
#            ops[op](registers, (a,b,c))
##            print(g_ip, 'ip=', registers[g_ip], nipchanges)
##            nipchanges += 1
#        else:

        ipbef = valip
        registers[g_ip] = valip
        newregisters = ops[op](registers, (a,b,c))
        valip = newregisters[g_ip]
        valip += 1
        newregisters[g_ip] += 1
#        print(g_ip, 'ip=', ipbef , newregisters[g_ip], registers, op, a, b, c, newregisters)

        registers = newregisters.copy()
#            registers[g_ip] += 1

        niter += 1
        if not niter % 100000:
            print(niter, g_ip, 'ip=', ipbef, registers[g_ip], registers, op, a, b, c, newregisters)





