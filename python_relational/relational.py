#!/usr/bin/env python3

import sys
from random import choice, randint, randrange, Random

if True:
    # Seed festsetzen und ausgeben
    # seed = randrange(sys.maxsize)
    seed = 647432261897158211
    rng = Random(seed)
    choice = rng.choice
    randrange = rng.randrange
    print("Seed:", seed)

# sizeX, sizeY = (6, 6)
sizeX, sizeY = (18, 18)
# sizeX, sizeY = (36, 9)
dirs = ((0,-1), (1, 0), (0, 1), (-1, 0))
unused_pos = []
for y in range(sizeY):
    for x in range(sizeX):
        unused_pos.append((x, y))

class tunnel_point:
    def __init__(self, pos, connect, val=None):
        self.pos = pos
        self.connect = connect
        self.val = val

class tunnel:
    def __init__(self):
        self.points = {}

    def add(self, pos1, pos2, val=""):
        p1 = self.points.get(pos1, tunnel_point(pos1, {}, val))
        p2 = self.points.get(pos2, tunnel_point(pos2, {}, val))
        p1.connect[pos2] = ""
        p2.connect[pos1] = ""
        self.points[pos1] = p1
        self.points[pos2] = p2


def show(laby, way=None):
    def coord(n):
        return n * 2 + 1

    li = [coord(sizeX) * ['#'] for _ in range(coord(sizeY))]
    bridge = []
    for p in laby.points.values():
        x, y = coord(p.pos[0]), coord(p.pos[1])
        li[y][x] = ' '
        for p_connect in p.connect:
            xc, yc = coord(p_connect[0]), coord(p_connect[1])
            if xc - x == 2 or yc - y == 2:
                x_mean, y_mean = (x + xc) // 2, (y + yc) // 2
                li[y_mean][x_mean] = ' '
            elif xc - x == 4 or yc - y == 4:
                bridge.append(((x,y), (xc, yc)))
    for (x, y), (xc, yc) in bridge:
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

    if way:
        for p in way.points.values():
            x, y = coord(p.pos[0]), coord(p.pos[1])
            li[y][x] = p.val

    li[0][1] = ' '
    li[-1][-2] = ' '
    print("\n".join(["".join(elem) for elem in li]))

def paint(laby, b_size=40, pensize=7, way=None, crosspoint=None):
    def draw_bridge(b_size):
        t.begin_fill()
        t.pendown()
        t.forward(b_size*1.2)
        t.left(90)
        t.penup()
        t.forward(b_size*0.6)
        t.pendown()
        t.left(90)
        t.forward(b_size*1.2)
        t.end_fill()

    import turtle as t
    t.speed(0)
    t.tracer(0)
    # t.shapesize(0.01)
    t.hideturtle()
    t.pensize(pensize)
    screen = t.Screen()
    width, height = sizeX * b_size + 40 , sizeY * b_size + 40
    screen.setup(width, height, width // 2, height // 2)
    bridge_h, bridge_v = [], []
    x_off, y_off = -width / 2 + 20, height / 2 - 20
    for y in range(sizeY+1):
        for x in range(sizeX+1):
            p = laby.points.get((x, y), None)
            if (not p or not (x, y-1) in p.connect) and x < sizeX and not (x, y) in [(0, 0), (sizeX-1, sizeY)]:
                t.penup()
                t.goto(x*b_size+x_off, y*-b_size+y_off)
                t.setheading(0)
                t.pendown()
                t.forward(b_size)
            if (not p or not (x-1, y) in p.connect) and y < sizeY:
                t.penup()
                t.goto(x*b_size+x_off, y*-b_size+y_off)
                t.setheading(270)
                t.pendown()
                t.forward(b_size)
            if (p and (x+2, y) in p.connect):
                bridge_h.append((x, y))
            if (p and (x  , y+2) in p.connect):
                bridge_v.append((x, y))
    t.pensize(int(pensize*0.70))
    t.fillcolor("white")
    for x, y in bridge_v:
        t.penup()
        t.goto(x * b_size + x_off + b_size*0.2, y * -b_size + y_off - b_size*0.9)
        t.setheading(270)
        draw_bridge(b_size)
    for x, y in bridge_h:
        t.penup()
        t.goto(x * b_size + x_off + b_size*0.9, y * -b_size + y_off - b_size*0.8)
        t.setheading(0)
        draw_bridge(b_size)
    t.penup()
    if crosspoint:
        t.shape("circle")
        t.shapesize(1)

        for p in crosspoint:
            x, y = p
            t.goto(x * b_size + x_off + b_size * 0.5, y * -b_size + y_off - b_size * 0.5)
            t.stamp()
    if way:
        for p in way.points.values():
            x, y = p.pos[0], p.pos[1]
            t.goto(x * b_size + x_off + b_size * 0.5, y * -b_size + y_off - b_size * 0.65)
            t.write(p.val, align='center')
            # t.goto(x * b_size + x_off + b_size * 0.5, y * -b_size + y_off - b_size * 0.4 - 12)
            # t.write(str(p.pos), align='center')
    t.update()
    # t.mainloop()
    screen.exitonclick()


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
            if len(avaiPos) > 0 and dig not in jumpPos: jumpPos.append(dig)

            dpos = choice(avaiPos)
            unused_pos.remove(dpos)
            laby.add(dig, dpos)
            dig = dpos
        dig = choice(jumpPos)
    return laby

def solve_labyrinth(laby):
    way = tunnel()
    cur_pos = (0, 0)
    untested = list(laby.points.keys())
    jumpPos = []
    cross_point = []
    way_int = 0

    while True:
        while True:
            if cur_pos in untested:
                untested.remove(cur_pos)
            avaiPos = []
            for npos in laby.points[cur_pos].connect.keys():
                if npos in untested:
                    avaiPos.append(npos)
            if len(avaiPos) == 0:
                break;
            elif len(avaiPos) > 1:
                jumpPos.append(cur_pos)
                cross_point.append(cur_pos)
            next_pos = avaiPos.pop()
            way.add(cur_pos, next_pos, str(way_int))
            cur_pos = next_pos
        way_int += 1
        if len(jumpPos) == 0: break
        cur_pos = jumpPos.pop()
    return way, cross_point

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
# way, crosspoint = None, None
way, crosspoint = solve_labyrinth(laby)
# laby.add((0, -1), (0, 0))
# laby.add((sizeX-1, sizeY-1), (sizeX-1, sizeY))
# show(laby, way)
paint(laby, way=way, crosspoint=crosspoint)
