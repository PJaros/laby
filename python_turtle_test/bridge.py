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

# radius = 100
length = 100


# def arc(radius=radius, length=length):
#     winkel = math.atan2(length/2, radius - (length/2)) * 180.0 / math.pi
#     # winkel = math.atan2(length/2, l2 - (length/2)) * 180.0 / math.pi
#     # umfang = radius * 2 * (winkel / (180.0 / math.pi))
#     print("Winkel: " + str(winkel)) #  + ", Umfang: " + str(umfang))
#     t.hideturtle()
#     t.setheading(90)
#     t.right(winkel)
#     t.circle(radius, winkel * 2)
#     # Ausgangswerte zum Vergleich nachzeichnen
#     t.penup()
#     t.goto(0,0)
#     t.setheading(90)
#     t.pendown()
#     t.forward(length)

def arc2(h, s):
    r = (h ** 2 + (s / 2) ** 2) / (2 * h)
    winkel = math.atan2(s / 2, r - h) * 180.0 / math.pi
    print("Winkel: " + str(winkel))
    print("r: " + str(r))
    t.hideturtle()
    t.setheading(90)
    t.right(winkel)
    t.circle(r, winkel * 2)
    # Ausgangswerte zum Vergleich nachzeichnen
    t.penup()
    t.goto(0,0)
    t.setheading(90)
    t.pendown()
    t.forward(s)
    t.penup()
    t.goto(0,s//2)
    t.setheading(0)
    t.pendown()
    t.forward(h)

# arc(radius, length)
arc2(30, length)

s = t.Screen()
s.exitonclick()