# Copyright (c) 2011-2016 Alexander Poluektov (alexander.poluektov@gmail.com)
#
# Use, modification and distribution are subject to the MIT license
# (See accompanying file MIT-LICENSE)

from life.board import *

def add_figure(board, name):
    f = catalog[name]
    for x,y in f.cells:
        board.add_cell(x,y)


def parse(s):
    cells = []
    lines = s.strip().split('\n')
    for y,l in enumerate(lines):
        l = ''.join(l.split())
        for x,c in enumerate(l):
            if c == 'X':
                cells.append((x,y))
    return cells


catalog = dict()

class Figure(object):
    def __init__(self, name, text_repr, alt=None):
        self.alt = alt
        if not self.alt:
            self.alt = []
        self.name = name
        self.cells = parse(text_repr)
        catalog[self.name] = self
        for n in self.alt:
            catalog[n] = self

def list_figures():
    res = []
    for k,v in catalog.items():
        res.append((k,v.alt))
    return res


# stillife

Figure('block', '''
X X
X X
''')

Figure('behive', '''
- X -
X - X
X - X
- X -
''')

Figure('loaf', '''
- X X -
X - - X
- X - X
- - X -
''')

Figure('boat', '''
X X -
X - X
- X -
''')


# oscillators

Figure('blinker', 'X X X')

Figure('toad', '''
- X X X
X X X -
''')

Figure('beacon', '''
X X - -
X X - -
- - X X
- - X X
''')

Figure('pulsar', '''
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
''')

Figure('pentadecathlon', '''
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
''')

# spaceships

Figure('glider', '''
- X -
X - -
X X X
''')

Figure('lightweight-spaceship', '''
X - - X -
- - - - X
X - - - X
- X X X X
''',
alt=['lwss'])

# complex life

Figure('r-pentomino', '''
- X X
X X -
- X -
''')

Figure('diehard', '''
- - - - - - X -
X X - - - - - -
- X - - - X X X
''')

Figure('acorn', '''
- X - - - - -
- - - X - - -
X X - - X X X
''')

# glider guns

Figure('glider-gun', '''
- - - - - - - - - - - - - - - - - - - - - - - - X - - - - - - - - - - -
- - - - - - - - - - - - - - - - - - - - - - X - X - - - - - - - - - - -
- - - - - - - - - - - - X X - - - - - - X X - - - - - - - - - - - - X X
- - - - - - - - - - - X - - - X - - - - X X - - - - - - - - - - - - X X
X X - - - - - - - - X - - - - - X - - - X X - - - - - - - - - - - - - -
X X - - - - - - - - X - - - X - X X - - - - X - X - - - - - - - - - - -
- - - - - - - - - - X - - - - - X - - - - - - - X - - - - - - - - - - -
- - - - - - - - - - - X - - - X - - - - - - - - - - - - - - - - - - - -
- - - - - - - - - - - - X X - - - - - - - - - - - - - - - - - - - - - -
''')

# my custom favorite

Figure('collision', '''
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
''')
