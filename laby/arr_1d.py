#!/usr/bin/env python3

from random import choice, randint
from time import clock
import array


class Laby:
    def __init__(self, sizeX, sizeY):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.realX = sizeX + 2
        self.realY = sizeY + 2
        self.realZ = 2
        self.arr = array.array("B", [0]) * (self.realX * self.realY * self.realZ)
        for x in range(1, self.sizeX + 1):
            for y in range(1, self.sizeY + 1):
                for z in range(2):
                    self.arr[x + y * self.realX + z * self.realX * self.realY] = 1
        self.dirs = (self.realX, 1, -self.realX, -1)


def create_laby(sizeX, sizeY):
    li = Laby(sizeX, sizeY)
    jumpPos = []

    pos = 2 * li.realX + 2
    li.arr[pos] = 0

    while 1:
        while 1:
            avaiDir = [d
                       for d in li.dirs
                       if li.arr[pos + d * 2] == 1]

            if not avaiDir: break
            dir = choice(avaiDir)
            if len(avaiDir) > 1:
                jumpPos.append(pos)

            for i in (0, 1):
                pos += dir
                li.arr[pos] = 0

        if not jumpPos:
            break
        else:
            rand_index = randint(0, len(jumpPos)-1)
            pos = jumpPos[rand_index]
            jumpPos[rand_index] = jumpPos[len(jumpPos)-1]
            jumpPos.pop()

    li.arr[li.realX + 2] = 0
    li.arr[li.realX * sizeY + (li.realX - 3)] = 0
    return li


def print_laby(li):
    for i in range(li.realY):
        line = ['#' if e == 1 else ' ' for e in li.arr[i * li.realX:(i + 1) * li.realX]]
        print("".join(line))


def paint(li, b_size=40, pensize=7, way=None, crosspoint=None, solution=None):
    global show_solution
    import turtle as t
    import math
    import sys

    screen = t.Screen()
    border = 40

    # Fix Window-Size
    width, height = 1024, 768
    if width / li.sizeX < height / li.sizeY:
        b_size = (width - border) / ((li.sizeX - 1) / 2)
        border_w, border_h = border / 2, (height - ((li.sizeY - 1) / 2 * b_size) - border) / 2
    else:
        b_size = (height - border) / ((li.sizeY - 1) / 2)
        border_w, border_h = (width - ((li.sizeX - 1) / 2 * b_size) - border) / 2, border / 2
    x_off, y_off = -width / 2 + border_w, height / 2 - border_h
    screen.setup(width, height, width // 2, height // 2)

    # Fix Block-Size
    # width, height = ((li.sizeX - 1) / 2) * b_size + border , ((li.sizeY - 1) / 2) * b_size + border
    # screen.setup(width, height, width // 2, height // 2)
    # x_off, y_off = -width / 2 + (border / 2), height / 2 - (border / 2)
    # screen.setup(width, height, width // 2, height // 2)

    def conv_x(x, shift=0.0, b_size=b_size, x_off=x_off):
        return ((x - 1) / 2) * b_size + x_off + shift * b_size

    def conv_y(y, shift=0.0, b_size=b_size, y_off=y_off):
        return ((y - 1) / 2) * -b_size + y_off - shift * b_size

    def p_laby_base(li, t=t, b_size=b_size):
        for y in range(1, li.sizeY+1, 2):
            for x in range(1, li.sizeX+1, 2):
                cur_pos = x + y * li.realX
                if li.arr[cur_pos + 1] == 1:
                    t.penup()
                    t.goto(conv_x(x), conv_y(y))
                    t.setheading(0)
                    t.pendown()
                    t.forward(b_size)
                if li.arr[cur_pos + li.realX] == 1:
                    t.penup()
                    t.goto(conv_x(x), conv_y(y))
                    t.setheading(270)
                    t.pendown()
                    t.forward(b_size)

    def p_laby_bridge_shadow(li, t=t, b_size=b_size, rel_width=0.4):
        width = b_size * rel_width
        rel_lo = (1 - rel_width) / 2
        rel_hi = 1 - rel_lo
        # for b in bridge:
        #     x, y = b.x1, b.y1
        for y in range(1, li.sizeY, 2):
            for x in range(1, li.sizeX, 2):
                cur_pos = (x + 1) + (y + 1) * li.realX  + li.realX * li.realY
                if li.arr[cur_pos] == 0:
                    print("0")
                    t.penup()
                    if li.arr[cur_pos + li.realX] == 0:
                        t.setheading(270)
                        t.goto(conv_x(x, rel_hi), conv_y(y - 2, 0.9))
                        print("v, x: " + str(x) + ", y: " + str(y))
                    else:
                        t.setheading(0)
                        t.goto(conv_x(x - 2, 0.9), conv_y(y, rel_lo))
                        print("h, x: " + str(x) + ", y: " + str(y))
                    bridge_shadow(length=b_size*1.2, width=width)

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

    def p_laby_bridge(bridge, t=t, b_size=b_size, rel_width=0.4, pensize=pensize*0.5):
        t.pensize(int(pensize*0.70))
        t.fillcolor("white")
        width = b_size * rel_width
        rel_lo = (1 - rel_width) / 2
        rel_hi = 1 - rel_lo
        for y in range(1, li.sizeY, 2):
            for x in range(1, li.sizeX, 2):
                cur_pos = (x + 1) + (y + 1) * li.realX + li.realX * li.realY
                if li.arr[cur_pos] == 0:
                    t.penup()
                    if li.arr[cur_pos + li.realX] == 0:
                        t.setheading(270)
                        t.goto(conv_x(x, rel_hi), conv_y(y - 2, 0.9))
                    else:
                        t.setheading(0)
                        t.goto(conv_x(x - 2, 0.9), conv_y(y, rel_lo))
                    bridge_arc(length=b_size*1.2, width=width, height=b_size*0.1, pen_size=int(pensize), fill=True)
                    bridge_arc(length=b_size*1.2, width=width, height=b_size*0.1, pen_size=int(pensize), fill=False)

    def bridge_arc(length, height, width, fill=True, pen_size=3):
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

    def draw(li):
        t.reset()
        t.tracer(0)
        t.hideturtle()
        t.pensize(3)
        p_laby_bridge_shadow(li)
        p_laby_base(li)
        p_laby_bridge(li)
        t.update()

    # Focus auf Fenster setzen: https://stackoverflow.com/a/44787756/406423
    rootwindow = screen.getcanvas().winfo_toplevel()
    rootwindow.call('wm', 'attributes', '.', '-topmost', '1')
    rootwindow.call('wm', 'attributes', '.', '-topmost', '0')
    draw(li)
    t.listen()
    screen.onkeypress(lambda: sys.exit(0), "Escape")
    screen.mainloop()

def default_generate_and_paint():
    # sizeX, sizeY = 3, 3
    # sizeX, sizeY = 31, 51
    sizeX, sizeY = 51, 31
    # sizeX, sizeY = 77, 11
    # sizeX, sizeY = 77, 31
    # sizeX, sizeY = 331, 201
    # sizeX, sizeY = 771, 311
    # sizeX, sizeY = 77711, 711
    start = clock()
    li = create_laby(sizeX, sizeY)
    end = clock()
    if li.sizeX * li.sizeY <= 77 * 31:
        print_laby(li)
    print("Berechnungszeit: %.5f" % (end - start))

    if sizeX * sizeY <= 331 * 201:
        paint(li, b_size=10)

def test_paint_v():
    li = Laby(7, 7)
    li.arr = array.array("B", [
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 1, 0, 1, 1, 1, 1, 1, 0,
        0, 1, 0, 1, 0, 0, 0, 1, 0,
        0, 1, 0, 1, 1, 1, 0, 1, 0,
        0, 1, 0, 0, 0, 0, 0, 1, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 0,
        0, 1, 0, 0, 0, 0, 0, 1, 0,
        0, 1, 1, 1, 1, 1, 0, 1, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 0,
        0, 1, 1, 1, 0, 1, 1, 1, 0,
        0, 1, 1, 1, 0, 1, 1, 1, 0,
        0, 1, 1, 1, 0, 1, 1, 1, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
    ])
    paint(li)

def test_paint_h():
    li = Laby(7, 7)
    li.arr = array.array("B", [
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 1, 0, 1, 1, 1, 1, 1, 0,
        0, 1, 0, 0, 0, 1, 0, 1, 0,
        0, 1, 1, 1, 0, 1, 0, 1, 0,
        0, 1, 0, 1, 0, 1, 0, 1, 0,
        0, 1, 0, 1, 0, 1, 0, 1, 0,
        0, 1, 0, 0, 0, 1, 0, 1, 0,
        0, 1, 1, 1, 1, 1, 0, 1, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 0,
        0, 1, 1, 0, 0, 0, 1, 1, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
    ])
    paint(li)


if __name__ == "__main__":
    # default_generate_and_paint()
    # test_paint_h()
    test_paint_v()
