# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 05:47:28 2018

@author: Andrej Leban
"""

import collections as coll


def mix(r1, r2):
    s = r1+r2
    a = s // 10
    b = s % 10
    if a:
        return a, b
    else:
        return (b,)


after = 320851


def solve(scoreBoard, n, first=False):

    found = False

    #    compare = coll.deque([5,1,5,8,9])
    #    compare = coll.deque([0,1,2,4,5])
    #    compare = coll.deque([9,2,5,1,0])
    #    compare = coll.deque([5,9,4,1,4])
    compare = coll.deque([3, 2, 0, 8, 5, 1])
    lenS = len(compare)
    prev = lenS
    tally = coll.deque(scoreboard)

    while not found:
        scoreboard.extend(mix(*(elf[1] for elf in elves)))

        for i, elf in enumerate(elves):
            adv = 1 + elf[1]
            newpos = (elf[0] + adv) % len(scoreboard)
            elves[i] = (newpos,
                        scoreboard[newpos])

        #        print(scoreboard, elves)
        if len(scoreboard) < lenS:
            tally.extend(scoreboard[-nelves:])
        elif len(tally) < lenS:
            tally.append(scoreboard[prev - 1])

        checked = 0
        for k in range(prev, len(scoreboard)):
            if tally == compare:
                #                print(k - lenS)
                found = True
                break

            tally.append(scoreboard[k])
            if len(tally) > lenS:
                tally.popleft()
            checked += 1

        #        print(tally)
        n += 1
        prev += checked

        if first and n >= after:
            break

        if not n % 1000000:
            print(n)

    return scoreboard


if __name__ == "__main__":

    scoreboardOrig = [3, 7]
    nelves = 2
    elves = [(i, s) for s, i in zip(scoreboardOrig, range(nelves))]

    n = 2

    # 1
    scoreboard = solve(scoreboardOrig.copy(), n, first=True)
    print("".join(map(str, scoreboard[after:after + 10])))

    # 2
    scoreboard = solve(scoreboardOrig.copy(), n, first=False)
    for i in range(10, len(scoreboard)):
        if scoreboard[i - 10: i] == [3, 2, 0, 8, 5, 1]:
            print(i - 10)
            break
