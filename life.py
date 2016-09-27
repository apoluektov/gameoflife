# Copyright (c) 2011-2016 Alexander Poluektov (alexander.poluektov@gmail.com)
#
# Use, modification and distribution are subject to the MIT license
# (See accompanying file MIT-LICENSE)

import copy

# represents all cells on the game board
class Generation(object):
    def __init__(self, left_bottom, right_top):
        self.left, self.bottom = left_bottom
        self.right, self.top = right_top
        self.nstep = 0
        self.cells = [[0 for y in range(self.bottom, self.top)] for x in range(self.left, self.right)]

    def add_cell(self, x, y):
        self.cells[x][y] = 1
 
    # calculates next generation
    def next(self):
        next_cells = copy.deepcopy(self.cells)

        for x in range(self.left, self.right):
            for y in range(self.bottom, self.top):
                # for each cell, we are interested in its value and the number of its alive neghbors
                c = self.cells[x][y]
                n = self.alive_neighbors_count(x, y)

                if c == 0:
                    if n == 3:
                        # newborn
                        next_cells[x][y] = 1

                if c == 1:
                    if n < 2 or n > 3:
                        # dead
                        next_cells[x][y] = 0

        self.cells = next_cells
        self.nstep += 1

    # for the given cell returns the number of alive neighbors
    def alive_neighbors_count(self, x, y):
        neighbors = [(x-1,y-1), (x,y-1), (x+1,y-1), (x-1,y), (x+1,y), (x-1,y+1),(x, y+1), (x+1,y+1)]
        res = 0
        for nb in neighbors:
            xn,yn = nb
            if xn >= self.left and xn < self.right and yn >= self.bottom and yn < self.top:
                if self.cells[xn][yn] == 1:
                    res += 1
        return res
