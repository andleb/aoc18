# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 22:00:43 2018

@author: Andrej Leban
"""

import matplotlib.pyplot as plt


def solve(init, rules, numgen):
    siz = len(init)
    pad = numgen + 2

    state = "".join(["."]*pad) + init + "".join(["."]*pad)
    newstate = list(state)

    sums = []

    gen = 0
    while gen < numgen:
        for i in range(2, siz + 2 * pad - 2):
            for r, new in rules.items():
                if state[i - 2:i + 3] == r:
#                    print("matched", r, "at", i-2)
                    newstate[i] = new
                    break

        state = "".join(newstate)
        if state[2] == "#" or state[-2] == "#":
                pad += 2
                state = "".join(["."] * pad) + state + "".join(["."] * pad)
                newstate = list(state)

        s = 0
        for ind, c in enumerate(state):
            if c == "#":
                s += ind - pad
#        print(s)
        sums.append(s)
        gen += 1

    return newstate, sums

if __name__ == "__main__":

#    init = '#..#.#..##......###...###'
    init = '##.######...#.##.#...#...##.####..###.#.##.#.##...##..#...##.#..##....##...........#.#.#..###.#'

#    rules = {'...##': '#',
#            '..#..': '#',
#            '.#...': '#',
#            '.#.#.': '#',
#            '.#.##': '#',
#            '.##..': '#',
#            '.####': '#',
#            '#.#.#': '#',
#            '#.###': '#',
#            '##.#.': '#',
#            '##.##': '#',
#            '###..': '#',
#            '###.#': '#',
#            '####.': '#'}

    rules = {'.###.':'#',
            '#.##.':'.',
            '.#.##':'#',
            '...##':'.',
            '###.#':'#',
            '##.##':'.',
            '.....':'.',
            '#..#.':'#',
            '..#..':'#',
            '#.###':'#',
            '##.#.':'.',
            '..#.#':'#',
            '#.#.#':'#',
            '.##.#':'#',
            '.#..#':'#',
            '#..##':'#',
            '##..#':'#',
            '#...#':'.',
            '...#.':'#',
            '#####':'.',
            '###..':'#',
            '#.#..':'.',
            '....#':'.',
            '.####':'#',
            '..###':'.',
            '..##.':'#',
            '.##..':'.',
            '#....':'.',
            '####.':'#',
            '.#.#.':'.',
            '.#...':'#',
            '##...':'#'}

    state, sums = solve(init, rules, numgen=20)

    final = "".join(state)
    print(sums[-1])

    state, sums = solve(init, rules, numgen=1000)
    plt.plot(sums)


