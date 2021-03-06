# Copyright (c) 2011-2016 Alexander Poluektov (alexander.poluektov@gmail.com)
#
# Use, modification and distribution are subject to the MIT license
# (See accompanying file MIT-LICENSE)

import unittest
from life import Board

class TestCase(unittest.TestCase):
    def testEmpty(self):
        g = Board()
        self.assertTrue(sorted(g.alive) == [])
        self.assertEquals(g.nstep, 0)
        g.next_step()
        self.assertTrue(sorted(g.alive) == [])
        self.assertEquals(g.nstep, 1)

    def testOne(self):
        g = Board()
        g.add_cell(1, 1)
        self.assertTrue(sorted(g.alive) == [(1,1)])
        g.next_step()
        self.assertTrue(sorted(g.alive) == [])

    def testTriple(self):
        g = Board()
        g.add_cell(1,1)
        g.add_cell(2,1)
        g.add_cell(1,2)
        g.next_step()
        self.assertTrue(sorted(g.alive) == [(1,1), (1,2), (2,1), (2,2)])
        g.next_step()
        self.assertEquals(g.nstep, 2)
        self.assertTrue(sorted(g.alive) == [(1,1), (1,2), (2,1), (2,2)])

    def test3x3(self):
        g = Board()
        for c in [(x,y) for x in range(0,3) for y in range(0,3)]:
            g.add_cell(*c)
        self.assertEquals(g.nstep, 0)
        g.next_step()
        self.assertEquals(sorted(g.alive), [(-1,1),(0,0),(0,2),(1,-1),(1,3),(2,0),(2,2),(3,1)])

unittest.main()
