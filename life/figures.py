# Copyright (c) 2011-2016 Alexander Poluektov (alexander.poluektov@gmail.com)
#
# Use, modification and distribution are subject to the MIT license
# (See accompanying file MIT-LICENSE)

from life.board import *

def block():
    g = Board()

    g.add_cell(0,0)
    g.add_cell(0,1)
    g.add_cell(1,0)
    g.add_cell(1,1)

    return g


def glider():
    g = Board()

    g.add_cell(0,1)
    g.add_cell(1,2)
    g.add_cell(2,0)
    g.add_cell(2,1)
    g.add_cell(2,2)

    return g


def complex():
    g = Board()

    g.add_cell(0,0)
    g.add_cell(0,1)
    g.add_cell(0,2)
    g.add_cell(1,1)
    g.add_cell(1,2)
    g.add_cell(1,0)
    g.add_cell(2,0)
    g.add_cell(2,1)
    g.add_cell(2,2)
    g.add_cell(3,0)
    g.add_cell(3,1)
    g.add_cell(3,2)
    g.add_cell(4,0)
    g.add_cell(4,1)
    g.add_cell(4,2)

    g.add_cell(-11+2,-10)
    g.add_cell(-10+2,-10)
    g.add_cell(-9+2,-10)
    g.add_cell(-9+2,-11)
    g.add_cell(-10+2,-12)

    return g
