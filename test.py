# Copyright (c) 2011-2016 Alexander Poluektov (alexander.poluektov@gmail.com)
#
# Use, modification and distribution are subject to the MIT license
# (See accompanying file MIT-LICENSE)

import unittest
from life import Generation

def alive(g):
    res = []
    for x in range(g.left, g.right):
        for y in range(g.bottom, g.top):
            if g.cells[x][y] == 1:
                res.append((x,y))
    return res

class TestCase(unittest.TestCase):
    def testEmpty(self):
        g = Generation((-10,-10), (10,10))
        self.assertTrue(sorted(alive(g)) == [])
        self.assertEquals(g.nstep, 0)
        g.next()
        self.assertTrue(sorted(alive(g)) == [])
        self.assertEquals(g.nstep, 1)

    def testOne(self):
        g = Generation((-10,-10), (10,10))
        g.add_cell(1, 1)
        self.assertTrue(sorted(alive(g)) == [(1,1)])
        g.next()
        self.assertTrue(sorted(alive(g)) == [])

    def testTriple(self):
        g = Generation((-10,-10), (10,10))
        g.add_cell(1,1)
        g.add_cell(2,1)
        g.add_cell(1,2)
        g.next()
        self.assertTrue(sorted(alive(g)) == [(1,1), (1,2), (2,1), (2,2)])
        g.next()
        self.assertEquals(g.nstep, 2)
        self.assertTrue(sorted(alive(g)) == [(1,1), (1,2), (2,1), (2,2)])

    def test3x3(self):
        g = Generation((-10,-10), (10,10))
        for c in [(x,y) for x in range(0,3) for y in range(0,3)]:
            g.add_cell(*c)
        self.assertEquals(g.nstep, 0)
        g.next()
        self.assertEquals(sorted(alive(g)), [(-1,1),(0,0),(0,2),(1,-1),(1,3),(2,0),(2,2),(3,1)])

unittest.main()
