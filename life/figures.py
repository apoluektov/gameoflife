# Copyright (c) 2011-2016 Alexander Poluektov (alexander.poluektov@gmail.com)
#
# Use, modification and distribution are subject to the MIT license
# (See accompanying file MIT-LICENSE)

from life.board import *

def add_figure(board, f):
    for x,y in parse(f):
        board.add_cell(x,y)

block = '''
X X
X X
'''

glider = '''
- X _
X - -
X X X
'''

hive = '''
- X -
X - X
X - X
- X -
'''

complex = '''
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
