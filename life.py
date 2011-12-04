# Copyright (c) 2011 Alexander Poluektov (alexander.poluektov@gmail.com)
#
# Use, modification and distribution are subject to the MIT license
# (See accompanying file MIT-LICENSE)

# represents all cells on the game board
class Generation(object):
    def __init__(self):
        self.alive = set()
        self.nstep = 0

    def add_cell(self, x, y):
        self.alive.add((x,y))
 
    # calculates next generation
    def next(self):
        # 1: for all alive: find the next status
        new_alive = set()
        for c in self.alive:
            n = self.number_of_adjacent_alive(*c)
            if n == 2 or n == 3:
                new_alive.add(c)

        # 2: for all adjacent to alive: find newborns
        for c in self.alive:
            for c2 in self.adjacent(*c):
                if self.number_of_adjacent_alive(*c2) == 3:
                    new_alive.add(c2)

        self.alive = new_alive
        self.nstep += 1

    # for the given cell returns the list of adjacent cells
    def adjacent(self, x0, y0):
        return ((x,y) for x in range(x0-1,x0+2) for y in range(y0-1,y0+2) if (x,y) != (x0,y0))

    # for the given cell returns the number of alive cells
    def number_of_adjacent_alive(self, x, y):
        return len([c for c in self.adjacent(x,y) if c in self.alive])
