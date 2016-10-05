# Copyright (c) 2011-2016 Alexander Poluektov (alexander.poluektov@gmail.com)
#
# Use, modification and distribution are subject to the MIT license
# (See accompanying file MIT-LICENSE)

# represents the game board
class Board(object):
    def __init__(self, code='B3/S23'):
        self.alive = set()
        self.nstep = 0
        self.born_counts, self.survive_counts = self._decode(code)

    def _decode(self, code):
        born, survives = code.split('/')
        if born[0] != 'B' or survives[0] != 'S':
            raise ValueError('invalide code: malformed')
        born_counts = [int(c) for c in born[1:]]
        survive_counts = [int(c) for c in survives[1:]]
        if born_counts:
            if max(born_counts) == 9:
                raise ValueError('invalid code: cell cannot have 9 neighbors')
            if min(born_counts) == 0:
                raise ValueError('invalid code: zero neighbors born is not supported')
        if survive_counts:
            if max(survive_counts) == 9:
                raise ValueError('invalid code: cell cannot have 9 neighbors')

        return born_counts, survive_counts

    def cell_state(self, x, y):
        if (x,y) in self.alive:
            return 1
        else:
            return 0

    def set_cell_state(self, x, y, st):
        if st == 1:
            self.add_cell(x, y)
        elif st == 0:
            self.remove_cell(x, y)

    # calculates next generation
    def next_step(self):
        # 1: for all alive: find the next status
        new_alive = set()
        for c in self.alive:
            n = self.number_of_adjacent_alive(*c)
            if n in self.survive_counts:
                new_alive.add(c)

        # 2: for all adjacent to alive: find newborns
        for c in self.alive:
            for c2 in self.adjacent(*c):
                n = self.number_of_adjacent_alive(*c2)
                if n in self.born_counts:
                    new_alive.add(c2)

        self.alive = new_alive
        self.nstep += 1

    def step_count(self):
        return self.nstep

    def add_cell(self, x, y):
        self.alive.add((x,y))

    def remove_cell(self, x, y):
        if (x,y) in self.alive:
            self.alive.remove((x,y))
 
    # for the given cell returns the list of adjacent cells
    def adjacent(self, x0, y0):
        return ((x,y) for x in range(x0-1,x0+2) for y in range(y0-1,y0+2) if (x,y) != (x0,y0))

    # for the given cell returns the number of alive cells
    def number_of_adjacent_alive(self, x, y):
        return len([c for c in self.adjacent(x,y) if c in self.alive])
