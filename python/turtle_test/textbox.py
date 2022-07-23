#!/usr/bin/env python3

# Calculating Fontsize: https://stackoverflow.com/a/45520085/406423

import turtle as t

from tkinter.font import Font

text = "A Penny for your thoughts"
pos = (0, 0)  # arbitrary position
font_size = 36  # arbitrary font size
font_type = ('Arial', font_size, 'normal')  # arbitrary font

def box(width, height):
    t.setheading(0)
    for _ in range(2):
        t.forward(width)
        t.left(90)
        t.forward(height)
        t.left(90)

def getTextMetrics(font_type, text):
    font_config = Font(font=font_type)
    font_ascent = font_config.metrics('ascent')
    font_descent = font_config.metrics('descent')
    text_width = font_config.measure(text)
    return font_ascent, font_descent, text_width

screen = t.Screen()
screen.tracer(0)
font_ascent, font_descent, text_width = getTextMetrics(font_type, text)

t.hideturtle()
t.penup()
t.color('black', 'pink')

t.goto(-(text_width / 2), 0)
t.pendown()
t.begin_fill()
box(text_width, font_ascent + font_descent)
t.end_fill()
t.color('black')
box(text_width, font_ascent + font_descent)

t.goto(pos)
t.write(text, align='center', font=font_type)
t.stamp()

screen.exitonclick()