# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 05:41:43 2018

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


def runProgram(registers, program, offset=0, stop=None):

    g_ip = 4
    valip = offset

    niter = 0

#    fakeregs = registers[:4] + [registers[4] + offset] + registers[5:]
    hist = [registers[:]]

    while valip in range(0, len(program) + offset) and\
        (niter < stop if stop is not None else True):

        if valip >= 28:
            pass

        op, a, b, c = program[valip - offset]
        fakeregs = registers[:4] + [registers[4] + offset] + registers[5:]

#        print(niter, program[valip], g_ip, 'ip=', valip, op, a, b, c,registers)
        print(niter, 'ip=', valip+offset, op, a, b, c, fakeregs)
        registers[g_ip] = valip
        ops[op](registers, (a,b,c))
        valip = registers[g_ip]
        valip += 1

        niter += 1
#        if not niter % 10:
        fakeregs = registers[:4] + [registers[4] + offset] + registers[5:]
        hist.append(fakeregs)

    return hist



if __name__ == "__main__":
#    global g_ip

    data = parseInput("input.txt")

#    program = getProgram(data)
#    registers = [0,0,0,0,0,0]
#    offset = 0

#    registers = [0,100,1,1,4,0]
    registers = [100000, 100000000, 13, 1000000, 17, 13]
#    registers = [0,0,0,0,4,255]
    offset = 5
    data = [
               'seti 0 5 3',
               'bori 3 65536 5',
               'seti 5557974 2 3',
               'bani 5 255 2',
               'addr 3 2 3',
               'bani 3 16777215 3',
               'muli 3 65899 3',
               'bani 3 16777215 3',
               'gtir 256 5 2']


#    two = 0
#    five = (two+13)*256
#    registers = [100000, 100000000, two, 1000000, 17, five]
#    offset = 14
#    data = [
#            'addr 2 4 4',
#            'addi 4 1 4',
#            'seti 27 9 4',
#            'seti 0 0 2',
#             'addi 2 1 1',
#             'muli 1 256 1',
#             'gtrr 1 5 1',
#             'addr 1 4 4',
#             'addi 4 1 4',
#             'seti 25 4 4',
#             'addi 2 1 2',
#             'seti 17 6 4',
#             'setr 2 2 5',
#             'seti 7 1 4'
#             ]

    hist = runProgram(registers, getProgram(data), offset=offset, stop=100)
    print(registers)


#    123 & 456
#
#    chr(ord('1') & ord('4'))\
#    + chr(ord('2') & ord('5'))\
#    + chr(ord('3') & ord('6'))








