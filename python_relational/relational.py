#!/usr/bin/env python3

from random import choice, randint, randrange

sizeX, sizeY = (36, 9)
unused_pos = []
dirs = ((0,-1), (1, 0), (0, 1), (-1, 0))
h_dirs = sorted([(0, -1), (0, 1)])
v_dirs = sorted([(-1, 0), (1, 0)])
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
    later = []
    for p in laby.points.values():
        x, y = coord(p.pos[0]), coord(p.pos[1])
        li[y][x] = ' '
        for p_connect in p.connect:
            xc, yc = coord(p_connect[0]), coord(p_connect[1])
            if xc - x == 2 or yc - y == 2:
                x_mean, y_mean = (x + xc) // 2, (y + yc) // 2
                li[y_mean][x_mean] = ' '
            elif xc - x == 4 or yc - y == 4:
                later.append(((x,y), (xc, yc)))
    for (x, y), (xc, yc) in later:
        if y == yc:
            for rx in range(x+1, xc):
                li[y][rx] = ' '
            li[y-1][x+2] = '_'
            li[y  ][x+2] = '_'
        elif x == xc:
            for ry in range(y+1, yc):
                li[ry][x] = ' '
            li[y+2][x-1] = '|'
            li[y+2][x+1] = '|'

    li[0][1] = ' '
    li[-1][-2] = ' '
    print("\n".join(["".join(elem) for elem in li]))


def all_h_connections(pos):
    if not len(pos.connect) == 2:
        return False
    for p in pos.connect.keys():
        if not pos.pos[0] == p[0]:
            return False
    return True


def all_v_connections(pos):
    if not len(pos.connect) == 2:
        return False
    for p in pos.connect.keys():
        if not pos.pos[1] == p[1]:
            return False
    return True


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
                else:
                    epos = dig[0] + d[0]*2, dig[1] + d[1]*2
                    n_point = laby.points.get(npos, None)
                    if n_point and epos in unused_pos and randrange(0, 5) == 0:
                        if d[0] == 0:
                            if all_v_connections(n_point):
                                avaiPos.append(epos)
                        else:
                            if all_h_connections(n_point):
                                avaiPos.append(epos)
            if len(avaiPos) == 0: break
            if len(avaiPos) > 1 and dig not in jumpPos: jumpPos.append(dig)

            dpos = choice(avaiPos)
            unused_pos.remove(dpos)
            laby.add(dig, dpos)
            dig = dpos
        dig = choice(jumpPos)
    return laby


def laby_horizontal_bridge():
    laby = tunnel()
    laby.add((0, 0), (1, 0))
    laby.add((1, 0), (1, 1))
    laby.add((1, 1), (1, 2))
    laby.add((1, 2), (2, 2))
    laby.add((2, 2), (2, 1))
    laby.add((2, 1), (0, 1))
    return laby


def laby_vertical_bridge():
    laby = tunnel()
    laby.add((0, 0), (0, 1))
    laby.add((0, 1), (1, 1))
    laby.add((1, 1), (2, 1))
    laby.add((2, 1), (2, 2))
    laby.add((2, 2), (1, 2))
    laby.add((1, 2), (1, 0))
    return laby


# laby = laby_horizontal_bridge()
# laby = laby_vertical_bridge()
laby = dig_labyrinth()
show(laby)