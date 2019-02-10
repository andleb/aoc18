# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 05:58:14 2018

@author: Andrej Leban
"""

import numpy as np

def parseInput(inp):
    data = []
    with open(inp, 'r') as f:
        for line in f:
            data.append(line)

    return data


def elim(s):
    left = list(s) + ["0"]
    right = ["0"] + list(s)
    diff = np.array(list(map(ord, right))) - np.array(list(map(ord, left)))

    rem = np.where(abs(diff) == 32)
    rem2 = np.unique(np.append(rem, rem - np.ones(len(rem))))
    print(rem2)

    newS = []
    last = 0
    j = 0

    for i in range(len(s)):
        if i not in rem2:
            newS.append(s[i])

        else:
            if i - last > 1:
#                print(i, j, last)
                j = 0
                last = i

            if j == 2:
#               print(i, j, last, s[i])
                if i - last == 1:
                    newS.append(s[i])
                else:
                    last = i
                    j = 0
            else:
#                print(i, j, last)
                j += 1
                last = i

    return "".join(newS), rem, rem2


def elim2(s, last="0"):
    i = 0
    ret = []
    end = len(s)
    lasti = 0

    while i < end-2:
        i += 1

        j = i - 1
        curr = s[i]
        prev = s[j]

        switch = False
        if abs(ord(curr) - ord(prev)) == 32:
            while (abs(ord(curr) - ord(prev)) == 32):
                try:
#                    print(i, j, curr, prev, ret)
                    i = min((i + 1, end-1))
                    if j > lasti:
                        j = max((0, j-1))
                        prev = s[j]
                    else:
                        if not switch:
                            j = lasti + 1
                            switch = True
                        j -= 1
                        prev = "".join(ret)[j]

                    curr = s[i]
#                    print(i, j, curr, prev)
                except IndexError:
                    pass

            ret.append(s[lasti:j+1])
            lasti = i
#            print(ret)

    ret.append(s[lasti:i+2])
    return "".join(ret)


def elim3(s):
    sOld = None
    while sOld != s:
        sOld = s
        for i in range(0,26):
            s = s.replace(chr(65+i) + chr(97+i), "")
            s = s.replace(chr(97+i) + chr(65+i), "")
    return s


if __name__ == "__main__":

    data = parseInput("input.txt")
    s = data[0][:-1]

#    s0 = 'dabAcCaCBAcCcaDA'
#    s0 = 'tRrgPgGvVpGyYTvVemMQnNqQxXtTqOMmxHhFfGgXhZzSKJjMmksKkDDdaAdrRzZlkKLWwiInmMneEPIipBbNjJFfVvNvdDVsuUSHoCpcCPcHhmiUuSsoiIxXQqODdkKUvhdDuUwWoWwOSsHOoFfVJbBvxXlLVVvj'
#    s0 = 'tRrgPgGvVpGyYTvVemMQnNqQxXtTqOMmxHhFfGgXhZzSKJjMmksKkDD'
#    s0 ='RrcCCctmMgq.QhXyYxHyHWwKkhqAaFfOoQRrIuDdaAUiOomwWlLFFdDfHh'
#    s = s0

    s2 = elim3(s)

    while len(s2) < len(s):
#        print(s2)
#        print(len(s2))
        s = s2
        s2 = elim3(s)

#    print(s2)
    print(len(s2))

    best = 1e18
    for i in range(1, 26):
        candidate = s.replace(chr(65+i), "").replace(chr(97+i), "")
        new = len(elim3(candidate))
        if new < best:
            best = new

    print(best)



