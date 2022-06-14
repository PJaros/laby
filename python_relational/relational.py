#!/usr/bin/env python3

sizeX, sizeY = (2, 6)
unused_pos = []
wall_str = "#"*(sizeX*2+1)
# dirs = ((0,-1), (1, 0), (0, 1), (-1, 0))
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

def show_laby(laby):
    print(wall_str)
    for y in range(sizeY):
        for x in range(sizeX+1):
            laby_point = laby.points.get((x, y) or None)
            if laby_point and (x-1, y) in laby_point.connect:
                print(" ", end='')
            else:
                print("#", end='')
            if x <= sizeX-1:
                if laby_point:
                    print(" ", end='')
                else:
                    print("#", end='')
        print()
        for x in range(sizeX):
            laby_point = laby.points.get((x, y) or None)
            if laby_point and (x, y+1) in laby_point.connect:
                print("# ", end='')
            else:
                print("##", end='')
        print("#")

laby = tunnel()
laby.add((0, 0), (1, 0))
laby.add((1, 0), (1, 1))
laby.add((1, 1), (1, 2))


show_laby(laby)