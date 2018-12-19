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
#def ip(inp, inst):
#    global g_ip
#
#    g_ip = inst[0]
#
#    return g_ip

def parseInput(inp):
    data = []
    with open(inp, 'r') as f:
        for line in f:
            data.append(line)

    return data

def addr(inp, inst):
    inp[inst[2]] = inp[inst[0]] + inp[inst[1]]

def addi(inp, inst):
    inp[inst[2]] = inp[inst[0]] + inst[1]

def mulr(inp, inst):
    inp[inst[2]] = inp[inst[0]] * inp[inst[1]]

def muli(inp, inst):
    inp[inst[2]] = inp[inst[0]] * inst[1]

def banr(inp, inst):
    inp[inst[2]] = inp[inst[0]] & inp[inst[1]]

def bani(inp, inst):
    inp[inst[2]] = inp[inst[0]] & inst[1]

def borr(inp, inst):
    a, b, c = inst
    inp[inst[2]] = inp[inst[0]] | inp[inst[1]]

def bori(inp, inst):
    a, b, c = inst
    inp[inst[2]] = inp[inst[0]] | inst[1]

def setr(inp, inst):
    inp[inst[2]] = inp[inst[0]]

def seti(inp, inst):
    inp[inst[2]] = inst[0]

def gtir(inp, inst):
    inp[inst[2]] = int(inst[0] > inp[inst[1]])

def gtri(inp, inst):
    inp[inst[2]] = int(inp[inst[0]] > inst[1])

def gtrr(inp, inst):
    inp[inst[2]] = int(inp[inst[0]] > inp[inst[1]])

def eqir(inp, inst):
    inp[inst[2]] = int(inst[0] == inp[inst[1]])

def eqri(inp, inst):
    inp[inst[2]] = int(inp[inst[0]] == inst[1])

def eqrr(inp, inst):
    inp[inst[2]] = int(inp[inst[0]] == inp[inst[1]])

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


def divisors(num):
    ret = []
    for x in range (1, num + 1):
        if (num % x) == 0 :
            ret.append(x)
    return ret

if __name__ == "__main__":
#    global g_ip

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

    registers = [0,0,0,0,0,0]

    g_ip = 3
    valip = 0

    niter = 0

    hist = []

    while valip in range(0, len(program)):
        op, a, b, c = program[valip]

#        ipbef = valip
        registers[g_ip] = valip
        ops[op](registers, (a,b,c))
        valip = registers[g_ip]
        valip += 1

        #opt
#        print(g_ip, 'ip=', ipbef , registers[g_ip], op, a, b, c, registers)
#        registers[g_ip] += 1


        niter += 1
        if not niter % 10:
            print(niter, g_ip, 'ip=', registers[g_ip], op, a, b, c,registers, )
            hist.append(registers)





