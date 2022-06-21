#!/usr/bin/env python3

# Copied from https://www.geeksforgeeks.org/turtle-onclick-function-in-python/

# import package
import turtle

# screen object
wn = turtle.Screen()


# method to perform action
def fxn(x, y):
    turtle.goto(x, y)
    turtle.write(str(x) + "," + str(y))


# onclick action
wn.onclick(fxn)
wn.mainloop()