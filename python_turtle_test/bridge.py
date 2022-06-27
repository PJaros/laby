#!/usr/bin/env python3

# Berechnungsformeln: https://rechneronline.de/pi/kreissegment.php
#
#                                 s = 2 * sqrt(2 * r * h - h ** 2)
#                             s / 2 = sqrt(2 * r * h - h ** 2)
#                      (s / 2) ** 2 = 2 * r * h - h ** 2
#             h ** 2 + (s / 2) ** 2 = 2 * r * h
# (h ** 2 + (s / 2) ** 2) / (2 * h) = r

import turtle as t
import math


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
    t.color(color, color)
    t.begin_fill()
    for _ in range(2):
        t.forward(length)
        t.right(90)
        t.forward(width)
        t.right(90)
    t.end_fill()


length = 100
height = 15
width  = length * 0.6

# t.speed(1)
t.tracer(0)
t.hideturtle()

bridge_shadow(length, width)
bridge(length, height, width)
bridge(length, height, width, False)

t.right(90)
bridge_shadow(length, width)
bridge(length, height, width)
bridge(length, height, width, False)

t.update()

s = t.Screen()
s.exitonclick()