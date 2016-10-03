# Copyright (c) 2011-2016 Alexander Poluektov (alexander.poluektov@gmail.com)
#
# Use, modification and distribution are subject to the MIT license
# (See accompanying file MIT-LICENSE)

from life.board import *

def add_figure(board, f):
    for x,y in parse(f):
        board.add_cell(x,y)

# stillife

block = '''
X X
X X
'''

beehive = '''
- X -
X - X
X - X
- X -
'''

loaf = '''
- X X -
X - - X
- X - X
- - X -
'''

boat = '''
X X -
X - X
- X -
'''

# oscillators

blinker = 'X X X'

toad = '''
- X X X
X X X -
'''

beacon = '''
X X - -
X X - -
- - X X
- - X X
'''

pulsar = '''
- - X X X - - - X X X - -
- - - - - - - - - - - - -
X - - - - X - X - - - - X
X - - - - X - X - - - - X
X - - - - X - X - - - - X
- - X X X - - - X X X - -
- - - - - - - - - - - - -
- - X X X - - - X X X - -
X - - - - X - X - - - - X
X - - - - X - X - - - - X
X - - - - X - X - - - - X
- - - - - - - - - - - - -
- - X X X - - - X X X - -
'''

pentadecathlon = '''
- X -
- X -
X - X
- X -
- X -
- X -
- X -
X - X
- X -
- X -
'''

# spaceships

glider = '''
- X _
X - -
X X X
'''

lightweight_spaceship = '''
X - - X -
- - - - X
X - - - X
- X X X X
'''

lwss = lightweight_spaceship

# complex life

r_pentomino = '''
- X X
X X -
- X -
'''

diehard = '''
- - - - - - X -
X X - - - - - -
- X - - - X X X
'''

acorn = '''
- X - - - - -
- - - X - - -
X X - - X X X
'''

# glider guns

glider_gun = '''
- - - - - - - - - - - - - - - - - - - - - - - - X - - - - - - - - - - -
- - - - - - - - - - - - - - - - - - - - - - X - X - - - - - - - - - - -
- - - - - - - - - - - - X X - - - - - - X X - - - - - - - - - - - - X X
- - - - - - - - - - - X - - - X - - - - X X - - - - - - - - - - - - X X
X X - - - - - - - - X - - - - - X - - - X X - - - - - - - - - - - - - -
X X - - - - - - - - X - - - X - X X - - - - X - X - - - - - - - - - - -
- - - - - - - - - - X - - - - - X - - - - - - - X - - - - - - - - - - -
- - - - - - - - - - - X - - - X - - - - - - - - - - - - - - - - - - - -
- - - - - - - - - - - - X X - - - - - - - - - - - - - - - - - - - - - -
'''

# my custom favorite

collision = '''
- X - - - - - - - - - - -
- - X - - - - - - - - - -
X X X - - - X - - - - - -
- - - - - X - X - - - - -
- - - - - X - X - - - - -
- - - - - - X - - - - - -
- - - - - - - - - - - - -
- X X - - - - - - - X X -
X - - X - - - - - X - - X
- X X - - - - - - - X X -
- - - - - - - - - - - - -
- - - - - - X - - - - - -
- - - - - X - X - - - - -
- - - - - X - X - - - - -
- - - - - - X - - - - - -
'''


def parse(s):
    cells = []
    lines = s.strip().split('\n')
    for y,l in enumerate(lines):
        l = ''.join(l.split())
        for x,c in enumerate(l):
            if c == 'X':
                cells.append((x,y))
    return cells
