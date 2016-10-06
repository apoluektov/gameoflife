# Copyright (c) 2011-2016 Alexander Poluektov (alexander.poluektov@gmail.com)
#
# Use, modification and distribution are subject to the MIT license
# (See accompanying file MIT-LICENSE)

from life.board import *
from collections import defaultdict

def add_figure(board, name):
    f = catalog.by_name[name]
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


class Catalog(object):
    def __init__(self):
        self.by_name = dict()
        self.by_category = defaultdict(list)

    def add_figure(self, figure):
        self.by_name[figure.name] = figure
        for n in figure.alt:
            self.by_name[n] = figure

        self.by_category[figure.category].append(figure)


catalog = Catalog()


class Figure(object):
    def __init__(self, name, text_repr, alt=None, category='miscellaneous'):
        self.name = name
        self.alt = alt
        if not self.alt:
            self.alt = []
        self.category = category
        self.cells = parse(text_repr)

        catalog.add_figure(self)


def list_figures_by_category():
    res = []
    for cat, fs in catalog.by_category.items():
        res.append((cat, fs))
    return res


# stillife

Figure('block', '''
X X
X X
''', category='still life')

Figure('behive', '''
- X -
X - X
X - X
- X -
''', category='still life')

Figure('loaf', '''
- X X -
X - - X
- X - X
- - X -
''', category='still life')

Figure('boat', '''
X X -
X - X
- X -
''', category='still life')


# oscillators

Figure('blinker', 'X X X', category='oscillators')

Figure('toad', '''
- X X X
X X X -
''', category='oscillators')

Figure('beacon', '''
X X - -
X X - -
- - X X
- - X X
''', category='oscillators')

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
''', category='oscillators')

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
''', category='oscillators')

# spaceships

Figure('glider', '''
- X -
X - -
X X X
''', category='spaceships')

Figure('lightweight-spaceship', '''
X - - X -
- - - - X
X - - - X
- X X X X
''',
alt=['lwss'], category='spaceships')

# explosive life

Figure('r-pentomino', '''
- X X
X X -
- X -
''', category='explosive life')

Figure('diehard', '''
- - - - - - X -
X X - - - - - -
- X - - - X X X
''', category='explosive life')

Figure('acorn', '''
- X - - - - -
- - - X - - -
X X - - X X X
''', category='explosive life')

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
''', category='guns')

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
''', category='explosive life')
