# Copyright (c) 2011-2016 Alexander Poluektov (alexander.poluektov@gmail.com)
#
# Use, modification and distribution are subject to the MIT license
# (See accompanying file MIT-LICENSE)

from life.board import *


def add_figure(board, f):
    for x,y in f:
        board.add_cell(x,y)


def block():
    c = []

    c.append((0,0))
    c.append((0,1))
    c.append((1,0))
    c.append((1,1))

    return c


def glider():
    c = []

    c.append((0,1))
    c.append((1,2))
    c.append((2,0))
    c.append((2,1))
    c.append((2,2))

    return c


def complex():
    c = []

    c.append((0,0))
    c.append((0,1))
    c.append((0,2))
    c.append((1,1))
    c.append((1,2))
    c.append((1,0))
    c.append((2,0))
    c.append((2,1))
    c.append((2,2))
    c.append((3,0))
    c.append((3,1))
    c.append((3,2))
    c.append((4,0))
    c.append((4,1))
    c.append((4,2))

    c.append((-11+2,-10))
    c.append((-10+2,-10))
    c.append((-9+2,-10))
    c.append((-9+2,-11))
    c.append((-10+2,-12))

    return c
