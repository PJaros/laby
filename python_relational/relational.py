#!/usr/bin/env python3

from random import choice, randint

sizeX, sizeY = (100, 20)
unused_pos = []
dirs = ((0,-1), (1, 0), (0, 1), (-1, 0))
for y in range(sizeY):
    for x in range(sizeX):
        unused_pos.append((x, y))

class tunnel_point:
    def __init__(self, pos, connect):
        self.pos = pos
        self.connect = connect

class tunnel:
    def __init__(self):
        self.points = {}

    def add(self, pos1, pos2):
        p1 = self.points.get(pos1, tunnel_point(pos1, {}))
        p2 = self.points.get(pos2, tunnel_point(pos2, {}))
        p1.connect[pos2] = ""
        p2.connect[pos1] = ""
        self.points[pos1] = p1
        self.points[pos2] = p2


def coord(n):
    return n * 2 + 1


def show(laby):
    li = [coord(sizeX) * ['#'] for _ in range(coord(sizeY))]
    for p in laby.points.values():
        x, y = coord(p.pos[0]), coord(p.pos[1])
        li[y][x] = ' '
        for p_connect in p.connect:
            xc, yc = coord(p_connect[0]), coord(p_connect[1])
            x_mean, y_mean = (x + xc) // 2, (y + yc) // 2
            li[y_mean][x_mean] = ' '

    print("\n".join(["".join(elem) for elem in li]))


def dig_labyrinth():
    laby = tunnel()
    dig = (0, 0)
    unused_pos.remove(dig)
    jumpPos = []

    while len(unused_pos) > 0:
        while True:
            avaiPos = []
            for d in dirs:
                npos = dig[0] + d[0], dig[1] + d[1]
                if npos in unused_pos:
                    avaiPos.append(npos)
            if len(avaiPos) == 0: break
            if len(avaiPos) > 1 and dig not in jumpPos: jumpPos.append(dig)

            dpos = choice(avaiPos)
            unused_pos.remove(dpos)
            laby.add(dig, dpos)
            dig = dpos
        dig = choice(jumpPos)

    return laby

# laby = tunnel()
# laby.add((0, 0), (1, 0))
# laby.add((1, 0), (1, 1))
# laby.add((1, 1), (1, 2))

laby = dig_labyrinth()
show(laby)