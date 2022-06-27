#!/usr/bin/env python3

from random import choice, randint, randrange, Random
import copy

# noinspection PyUnreachableCode
if False:
    # Seed festsetzen und ausgeben
    # import sys
    # seed = randrange(sys.maxsize)
    seed = 647432261897158211
    rng = Random(seed)
    choice = rng.choice
    randrange = rng.randrange
    print("Seed:", seed)

# sizeX, sizeY = (6, 6)
sizeX, sizeY = (14, 14)
# sizeX, sizeY = (18, 18)
# sizeX, sizeY = (36, 9)
# sizeX, sizeY = (36, 36)
dirs = ((0,-1), (1, 0), (0, 1), (-1, 0))

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

def paint(laby, b_size=40, pensize=7, way=None, crosspoint=None, solution=None):
    import turtle as t
    import math

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
    for y in range(sizeY + 1):
        for x in range(sizeX + 1):
            p = laby.points.get((x, y), None)
            if (p and (x + 2, y) in p.connect):
                bridge_h.append((x, y))
            if (p and (x, y + 2) in p.connect):
                bridge_v.append((x, y))

    # def draw_bridge(b_size):
    #     t.begin_fill()
    #     t.pendown()
    #     t.forward(b_size*1.2)
    #     t.left(90)
    #     t.penup()
    #     t.forward(b_size*0.6)
    #     t.pendown()
    #     t.left(90)
    #     t.forward(b_size*1.2)
    #     t.end_fill()

    def arc(height, length):
        abs_height = abs(height)
        radius = (abs_height ** 2 + (length / 2) ** 2) / (2 * abs_height)
        winkel = math.atan2(length / 2, radius - abs_height) * 180.0 / math.pi
        orig_heading = t.heading()
        if height > 0:
            t.right(winkel)
            t.circle(radius, winkel * 2)
        else:
            t.left(winkel)
            t.circle(-radius, winkel * 2)
        t.setheading(orig_heading)

    def bridge(length, height, width, fill=True, pen_size=3):
        if fill:
            t.color("white", "white")
            t.begin_fill()
        else:
            t.color("black", "white")
        if not fill:
            t.pensize(pen_size)
        arc(-height, length)
        t.right(90)
        if not fill:
            t.penup()
        t.forward(width)
        t.right(90)
        if not fill:
            t.pendown()
        t.pensize(pen_size)
        arc(height, length)
        t.right(90)
        t.pensize(1)
        if not fill:
            t.penup()
        t.forward(width)
        t.right(90)
        if fill:
            t.end_fill()
        t.color("black")
        t.pendown()

    def bridge_shadow(length, width, color=(0.8, 0.8, 0.8)):
        t.penup()
        t.color(color, color)
        t.begin_fill()
        for _ in range(2):
            t.forward(length)
            t.right(90)
            t.forward(width)
            t.right(90)
        t.end_fill()
        t.color("black")

    def conv_x(x, shift=0.0, b_size=b_size, x_off=x_off):
        return x * b_size + x_off + shift * b_size

    def conv_y(y, shift=0.0, b_size=b_size, x_off=y_off):
        return y * -b_size + y_off - shift * b_size

    def p_laby_base(laby, t=t, b_size=b_size, pensize=pensize):
        for y in range(sizeY+1):
            for x in range(sizeX+1):
                p = laby.points.get((x, y), None)
                if (not p or not (x, y-1) in p.connect) and x < sizeX and not (x, y) in [(0, 0), (sizeX-1, sizeY)]:
                    t.penup()
                    t.goto(conv_x(x), conv_y(y))
                    t.setheading(0)
                    t.pendown()
                    t.forward(b_size)
                if (not p or not (x-1, y) in p.connect) and y < sizeY:
                    t.penup()
                    t.goto(conv_x(x), conv_y(y))
                    t.setheading(270)
                    t.pendown()
                    t.forward(b_size)

    def p_laby_bridge(laby, t=t, b_size=b_size, pensize=pensize):
        t.pensize(int(pensize*0.70))
        t.fillcolor("white")
        for x, y in bridge_v:
            t.penup()
            t.setheading(270)
            t.goto(conv_x(x, 0.9), conv_y(y, 0.9))
            bridge(length=b_size*1.2, width=b_size*0.6, height=b_size*1.2*0.15, pen_size=int(pensize*0.70), fill=True)
            bridge(length=b_size*1.2, width=b_size*0.6, height=b_size*1.2*0.15, pen_size=int(pensize*0.70), fill=False)
            # t.goto(conv_x(x, 0.2), conv_y(y, 0.9))
            # draw_bridge(b_size)
        for x, y in bridge_h:
            t.penup()
            t.setheading(0)
            t.goto(conv_x(x, 0.9), conv_y(y, 0.2))
            bridge(length=b_size*1.2, width=b_size*0.6, height=b_size*1.2*0.15, pen_size=int(pensize*0.70), fill=True)
            bridge(length=b_size*1.2, width=b_size*0.6, height=b_size*1.2*0.15, pen_size=int(pensize*0.70), fill=False)
            # t.goto(conv_x(x, 0.9), conv_y(y, 0.8))
            # draw_bridge(b_size)

    def p_laby_bridge_shadow(laby, t=t, b_size=b_size):
        for x, y in bridge_v:
            t.penup()
            t.setheading(270)
            t.goto(conv_x(x, 0.9), conv_y(y, 0.9))
            bridge_shadow(length=b_size*1.2, width=b_size*0.6)
        for x, y in bridge_h:
            t.penup()
            t.setheading(0)
            t.goto(conv_x(x, 0.9), conv_y(y, 0.2))
            bridge_shadow(length=b_size*1.2, width=b_size*0.6)

    def p_crosspoint_way(laby, t=t, b_size=b_size, pensize=pensize, crosspoint=crosspoint, way=way):
        t.penup()
        if crosspoint:
            t.shape("circle")
            t.shapesize(1)
            for p in crosspoint:
                x, y = p
                t.goto(conv_x(x, 0.5), conv_y(y, 0.5))
                t.stamp()
        if way:
            for p in way.points.values():
                x, y = p.pos[0], p.pos[1]
                t.goto(conv_x(x, 0.5), conv_y(y, 0.65))
                t.write(p.val, align='center')

    def p_solution(solution, t=t, b_size=b_size):
        t.penup()
        if solution:
            t.pencolor("red")
            t.pensize(1)
            for p in solution:
                t.goto(conv_x(p[0], 0.5), conv_y(p[1], 0.5))
                if not t.isdown(): t.pendown()

    def on_click_solution(x, y):
        # print("on_click_solution")
        p_solution(solution)
        t.update()
        screen.exitonclick()


    p_laby_bridge_shadow(laby)
    p_laby_base(laby)
    p_laby_bridge(laby)
    p_crosspoint_way(laby, crosspoint=crosspoint, way=way)
    # p_solution(solution)
    t.update()
    t.listen()
    screen.onclick(on_click_solution)
    screen.mainloop()

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
    unused_pos = []
    for y in range(sizeY):
        for x in range(sizeX):
            unused_pos.append((x, y))
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
                    if n_point and epos in unused_pos and randrange(0, 3) == 0:
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
    cp_ancestor = {(0,0):[]}
    cur_ancestor = []
    way_int = 0
    solution = None

    while True:
        while True:
            if cur_pos in untested:
                untested.remove(cur_pos)
            if cur_pos == (sizeX-1, sizeY-1):
                solution = copy.copy(cur_ancestor)
                solution.append((sizeX-1, sizeY-1))
            avaiPos = []
            for npos in laby.points[cur_pos].connect.keys():
                if npos in untested:
                    avaiPos.append(npos)
            if len(avaiPos) == 0:
                break
            elif len(avaiPos) > 1:
                jumpPos.append(cur_pos)
                cross_point.append(cur_pos)
            next_pos = avaiPos.pop()
            way.add(cur_pos, next_pos, str(way_int))
            cp_ancestor[cur_pos] = copy.copy(cur_ancestor)
            cur_ancestor.append(cur_pos)
            cur_pos = next_pos
        way_int += 1
        if len(jumpPos) == 0: break
        cur_pos = jumpPos.pop()
        cur_ancestor = cp_ancestor[cur_pos]
    return way, cross_point, solution

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
# way, crosspoint = None, None
# paint(laby)

max_length = 0
for _ in range(20):
    laby = dig_labyrinth()
    way, crosspoint, solution = solve_labyrinth(laby)
    # print("Solution: " + str(len(solution)))
    if len(solution) > max_length:
        max_length = len(solution)
        cur_laby, cur_solution = laby, solution
print("Solution: " + str(len(cur_solution)) + ", " + str(cur_solution))

# show(laby)
# show(laby, way)
# paint(laby, way=way, crosspoint=crosspoint, solution=solution)
# paint(laby, solution=solution)
paint(cur_laby, solution=cur_solution)
# paint(cur_laby)
