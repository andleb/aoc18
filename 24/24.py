# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 21:10:34 2018

@author: Andrej Leban
"""

import copy

from recordtype import recordtype

import re

import numpy as np


Group = recordtype('Group', ['typ', 'n', 'HP', 'AT_DAM', 'AT_TYPE', 'INIT', 'SPECIAL'])


def parseData(data):

    imm, inf = [], []
    immSwitch = True
    regex = re.compile(r"(\d+) units each with (\d+) hit points (\([^)]*\) )?"
                      r"with an attack that does (\d+) (\w+) damage at initiative (\d+)")
    for line in data:
        if line == "\n" or line == "":
            continue

        try:
            re.search('.*Immune System:.*', line).groups()
            current = imm
            immSwitch = True
            continue
        except AttributeError:
            pass

        try:
            re.search('.*Infection:.*', line).groups()
            current = inf
            immSwitch = False
            continue
        except AttributeError:
            pass

        try:
            groups = re.search(regex, line).groups()
        except AttributeError:
            pass

        spec = None
        if len(groups) == 6:
            un, hp, spec, at, attyp, init = groups
        elif len(groups) == 5:
            un, hp, at, attyp, init = groups
        else:
            raise RuntimeError

        dicspec = {}
        if spec is not None:
            try:
                weaks = re.search('weak to ([\w, \, \s]*)[;,\)]+', spec).groups()
                weaks = weaks[0].split(", ")

                for w in weaks:
                    dicspec[w] = 'weak'
            except AttributeError:
                pass

            try:
                immunes = re.search('immune to ([\w, \, \s]*)[;,\)]+', spec).groups()
                immunes = immunes[0].split(", ")

                for i in immunes:
                    dicspec[i] = 'imm'
            except AttributeError:
                pass

        current.append(
                Group(typ='imm' if immSwitch else 'inf',
                      n=int(un), HP=int(hp), AT_DAM=int(at), AT_TYPE=attyp,
                      INIT=int(init), SPECIAL=dicspec))

    return imm, inf


def effPower(group):
    return group.n  * group.AT_DAM


def calcDam(g, other):
    dam = effPower(g)

    # imm, weak
    try:
        spec = other.SPECIAL[g.AT_TYPE]
        if spec == 'imm':
            dam = 0
        elif spec == 'weak':
            dam *= 2
        else:
            raise RuntimeError
    except KeyError:
        pass

    return dam


def alive(imm):
    sm = 0
    for g in imm:
        sm += g.n
    return sm


def solve1(imm, inf, boost=0):
    itr = 0

    if boost > 0:
        for im in imm:
            im.AT_DAM += boost

    while len(inf) and len(imm):

        groups = sorted(imm + inf, key=lambda g: (-effPower(g), -g.INIT))

        # selection phase
        order = []
        ignoredimm = set()
        ignoredinf = set()

        for g in groups:
            ind, best_dam, best_pwr, best_init = 0, 0, 0, 0
            immB = g.typ == 'imm'
            i = imm.index(g) if immB else inf.index(g)
            othrs = inf if immB else imm
            skipped = True

            for j, gother in enumerate(othrs):
                if j in (ignoredinf if immB else ignoredimm):
                    continue

                dam = calcDam(g, gother)
                # If it cannot deal any defending groups damage, it does not choose a target.
                if dam <= 0:
                    continue

                skipped = False
                if dam > best_dam:
                    ind = j
                    best_dam = dam
                    best_pwr = effPower(gother)
                    best_init = gother.INIT
                elif dam == best_dam:
                    if effPower(gother) > best_pwr:
                        ind = j
                        best_dam = dam
                        best_pwr = effPower(gother)
                        best_init = gother.INIT
                    elif effPower(gother) == best_pwr:
                        if gother.INIT > best_init:
                            ind = j
                            best_dam = dam
                            best_pwr = effPower(gother)
                            best_init = gother.INIT

            # select
            if not skipped:
                order.append((g, othrs[ind], i, ind, dam))
                if immB:
                    ignoredinf.add(ind)
                else:
                    ignoredimm.add(ind)

        # attack phase
        orderat = sorted(order, key=lambda t: -t[0].INIT)
        damage_done = False

        for g, enemy, i, j, dam in orderat:

            if enemy.n <= 0:
                # should have been cleaned up!
                raise RuntimeError
            if g.n <= 0:
                continue

            immB = g.typ == 'imm'
            prevn = enemy.n

            dam = calcDam(g, enemy)

            newn = int(np.ceil((enemy.n * enemy.HP - dam) / enemy.HP))

            if newn != prevn:
                damage_done = True

            if immB:
                inf[j].n = newn
            else:
                imm[j].n = newn

        if not damage_done and itr > 10000:
            return itr, imm, inf

        # cleanup removed
        i = 0
        while i < len(imm):
            if imm[i].n <= 0:
                g = imm.pop(i)
            else:
                i += 1
        i = 0
        while i < len(inf):
            if inf[i].n <= 0:
                g = inf.pop(i)
            else:
                i += 1

        itr += 1

    return itr, imm, inf


if __name__ == "__main__":

#    data = [\
#'Immune System:',
#'17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2',
#'989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3',
#'Infection:',
#'801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1',
#'4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4']

    data = [\
'Immune System:',
'4081 units each with 8009 hit points (immune to slashing, radiation; weak to bludgeoning, cold) with an attack that does 17 fire damage at initiative 7',
'2599 units each with 11625 hit points with an attack that does 36 bludgeoning damage at initiative 17',
'4232 units each with 4848 hit points (weak to slashing) with an attack that does 11 bludgeoning damage at initiative 13',
'2192 units each with 8410 hit points (immune to fire, radiation; weak to cold) with an attack that does 36 bludgeoning damage at initiative 18',
'4040 units each with 8260 hit points (immune to cold) with an attack that does 17 bludgeoning damage at initiative 20',
'1224 units each with 4983 hit points (immune to bludgeoning, cold, slashing, fire) with an attack that does 37 radiation damage at initiative 6',
'1462 units each with 6747 hit points with an attack that does 41 bludgeoning damage at initiative 10',
'815 units each with 2261 hit points (weak to cold) with an attack that does 22 cold damage at initiative 19',
'2129 units each with 1138 hit points (weak to radiation, cold) with an attack that does 5 bludgeoning damage at initiative 3',
'1836 units each with 8018 hit points (immune to radiation) with an attack that does 37 slashing damage at initiative 15',
'Infection:',
'909 units each with 34180 hit points (weak to slashing, bludgeoning) with an attack that does 72 bludgeoning damage at initiative 4',
'908 units each with 57557 hit points (weak to bludgeoning) with an attack that does 96 fire damage at initiative 14',
'65 units each with 32784 hit points (weak to cold; immune to bludgeoning) with an attack that does 957 fire damage at initiative 2',
'5427 units each with 50754 hit points with an attack that does 14 radiation damage at initiative 12',
'3788 units each with 27222 hit points (immune to cold, bludgeoning) with an attack that does 14 slashing damage at initiative 16',
'7704 units each with 14742 hit points (immune to cold) with an attack that does 3 fire damage at initiative 1',
'5428 units each with 51701 hit points (weak to fire) with an attack that does 14 fire damage at initiative 9',
'3271 units each with 32145 hit points (weak to bludgeoning, radiation) with an attack that does 19 bludgeoning damage at initiative 8',
'99 units each with 49137 hit points with an attack that does 855 fire damage at initiative 5',
'398 units each with 29275 hit points (weak to fire; immune to slashing) with an attack that does 137 cold damage at initiative 11']


    imm, inf = parseData(data)

    niter, imm2, inf2 = solve1(copy.deepcopy(imm), copy.deepcopy(inf), boost=0)

    sm = 0
    for g in inf2 + imm2:
        sm += g.n

    print(sm)
    print('\n')

#### 2
    boost = 1000000
    prevboost = boost
    limm = 1

    while limm and boost > 1:
        niter, imm2, inf2 = solve1(copy.deepcopy(imm), copy.deepcopy(inf), boost=boost)
        print(boost, len(imm2), len(inf2), alive(imm2))
        limm = len(imm2)
        if limm > 0:
            prevboost = boost
            boost //= 2
        else:
            boost = prevboost

    linf = 1
    while linf:
        niter, imm2, inf2 = solve1(copy.deepcopy(imm), copy.deepcopy(inf), boost=boost)
        print(boost, len(imm2), len(inf2), alive(imm2))
        linf = len(inf2)
        if linf > 0:
            prevboost = boost
            boost += 1
        else:
            break

    niter, imm2, inf2 = solve1(copy.deepcopy(imm), copy.deepcopy(inf), boost=boost)

    print(alive(imm2))
    print('\n')
