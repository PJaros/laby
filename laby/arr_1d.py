#!/usr/bin/python
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
    if li.sizeX <= 77:
        for i in range(li.realY):
            line = ['#' if e == 1 else ' ' for e in li.arr[i * li.realX:(i + 1) * li.realX]]
            print("".join(line))


def paint(li, b_size=40, pensize=7, way=None, crosspoint=None, solution=None):
    global show_solution
    import turtle as t
    # import math
    import sys

    screen = t.Screen()
    width, height = ((li.sizeX - 1) / 2) * b_size + 40 , ((li.sizeY - 1) / 2) * b_size + 40
    screen.setup(width, height, width // 2, height // 2)
    x_off, y_off = -width / 2 + 15, height / 2 - 15

    def conv_x(x, shift=0.0, b_size=b_size, x_off=x_off):
        return (x / 2) * b_size + x_off + shift * b_size

    def conv_y(y, shift=0.0, b_size=b_size, y_off=y_off):
        return (y / 2) * -b_size + y_off - shift * b_size

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

    def draw(li):
        t.reset()
        t.tracer(0)
        t.hideturtle()
        t.pensize(3)
        p_laby_base(li)
        t.update()

    # Focus auf Fenster setzen: https://stackoverflow.com/a/44787756/406423
    rootwindow = screen.getcanvas().winfo_toplevel()
    rootwindow.call('wm', 'attributes', '.', '-topmost', '1')
    rootwindow.call('wm', 'attributes', '.', '-topmost', '0')
    draw(li)
    t.listen()
    screen.onkeypress(lambda: sys.exit(0), "Escape")
    screen.mainloop()


if __name__ == "__main__":
    # sizeX, sizeY = 3, 3
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

