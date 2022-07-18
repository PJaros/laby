#!/usr/bin/python
from random import choice, randint
from time import clock
import array

def randEntry(size):
    return randint(1, size // 2 - 2) * 2 + 2

# sizeX, sizeY = (77, 11)
sizeX, sizeY = (77, 31)
# sizeX, sizeY = (771, 311)
# sizeX, sizeY = (77711, 711)
realX, realY = sizeX + 2, sizeY + 2
dirs = (realX, 1, -realX, -1)
# li = np.zeros(realX * realY)
li = array.array("B", [0]) * (realX * realY)
for x in range(1, sizeX + 1):
    for y in range(1, sizeY + 1):
        li[x + y * realX] = 1
start = clock()
jumpPos = []

pos = 2 * realX + 2
li[pos] = 0

while 1:
    while 1:
        avaiDir = [d
                   for d in dirs
                   if li[pos + d * 2] == 1]

        if not avaiDir: break
        dir = choice(avaiDir)
        jumpPos.append(pos)

        for i in (0, 1):
            pos += dir
            li[pos] = 0

    if not jumpPos:
        break
    else:
        pos = jumpPos.pop()

li[realX + 2] = 0
li[realX * sizeY + (realX - 3)] = 0
# li[1 * realX + randEntry(sizeX)] = 0
# li[sizeY * realX + randEntry(sizeX)] = 0
end = clock()

if sizeX <= 77:
    for i in range(realY):
        line = ['#' if e == 1 else ' ' for e in li[i * realX:(i + 1) * realX]]
        print("".join(line))

print("Berechnungszeit: %.5f" % (end - start))
