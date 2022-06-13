#!/usr/bin/env python3

from random import choice, randint

dirs = ((1,0), (0,1), (-1,0), (0,-1))

def randEntry(size):
    return randint(1, size//2-2)*2+2

sizeX, sizeY = (37, 15)
li = [[' ']+['#']*sizeX+[' '] for i in range(sizeY)]
li.append([' ']*(sizeX+2))
li.insert(0,[' ']*(sizeX+2))

jumpPos = []

posY, posX = (2, 2)
li[posY][posX] = ' '

while 1:
    while 1:
        avaiDir = [d
                   for d in dirs
                   if li[posY+d[1]*2][posX+d[0]*2] != ' ']

        if not avaiDir: break
        dir = choice(avaiDir)
        jumpPos.append((posY, posX))

        for i in (0, 1):
            posX, posY = posX + dir[0], posY + dir[1]
            li[posY][posX] = ' '

    if not jumpPos: break
    else:           posY, posX = jumpPos.pop()

li[1][randEntry(sizeX)] =' '
li[sizeY][randEntry(sizeX)] =' '

print("\n".join(["".join(elem) for elem in li]))