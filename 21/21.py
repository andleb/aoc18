# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 05:41:43 2018

@author: Andrej Leban
"""

import re


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
            program.append((op, ) + tuple(map(int, (a, b, c))))
        except ValueError:
            op, ipP = re.search('(#\w+)\s*(\d+)\s*', line).groups()
            program.append((op, ) + tuple(map(int, (ipP, ))) + (0, 0, ))

    return program

def runProgram(registers, program, offset=0, stop=None):

    g_ip = 4
    valip = offset

    niter = 0

    hist = [registers[:]]

    while valip in range(0, len(program) + offset) and\
            (niter < stop if stop is not None else True):

        # debugger point
        if valip >= 28:
            pass

        op, a, b, c = program[valip - offset]
        fakeregs = registers[:4] + [registers[4] + offset] + registers[5:]

#        print(niter, program[valip], g_ip, 'ip=', valip, op, a, b, c,registers)
        registers[g_ip] = valip
        ops[op](registers, (a, b, c))
        valip = registers[g_ip]
        valip += 1

        niter += 1
        fakeregs = registers[:4] + [registers[4] + offset] + registers[5:]
        hist.append(fakeregs)

    return hist


if __name__ == "__main__":

    data = parseInput("input.txt")

    program = getProgram(data)
    registers = [0, 0, 0, 0, 0, 0]
    offset = 0

### SIMULATED
# offset allows us to simulate a part chunk of the input program
#    hist = runProgram(registers, getProgram(data), offset=offset, stop=100000)
#    print(registers)

    ### REVERSE ENGINEERED
    a, b, c, d, f = 0, 0, 0, 0, 0
    # the instruction pointer
    ip = 4

    # this is the last instruction
    finished = False
    while not finished:
        f = d | 0x10000
        d = 5557974

        while True:
            c = f & 0xFF
            d += c
            d &= 0xFFFFFF
            d *= 0x1016B
            d &= 0xFFFFFF

            b = int(256 > f)
            if(256 > f):
                # b = int(d == a)
                # if d == 0 it will go out of bounds
                # hence 0 should be d
                print(d)
                finished = True
                break

            c = 0
            while not b:
                b = c + 1
                b *= 0x100
                b = int(b > f)

                if not b:
                    c += 1

            f = c

### PART 2

    count = 0
    res = {}
    finished = False

    while not finished and count < 1e5:
        f = d | 0x10000
        d = 5557974

        while True:
            c = f & 0xFF
            d += c
            d &= 0xFFFFFF
            d *= 0x1016B
            d &= 0xFFFFFF

            b = int(256 > f)
            if(b):
                if d not in res.keys():
#                    print(d)
                    res[d] = count
                break

#            c = 0
#            while not b:
#                b = c + 1
#                b *= 0x100
#                b = int(b > f)
#
#                if not b:
#                    c += 1
#                count += 1
#
#            f = c
            #equal to the above
            f = f // 256
            count += 1

    # using one iteration of each loop as a proxy for instructions
    most_inst = sorted(res.items(), key=lambda kv: -kv[1])
    print(most_inst[0])

