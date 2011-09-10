# Copyright (c) 2011 Alexander Poluektov (alexander.poluektov@gmail.com)
#
# Use, modification and distribution are subject to the MIT license
# (See accompanyung file MIT-LICENSE)

import unittest
from life import Generation

class TestCase(unittest.TestCase):
    def testEmpty(self):
        g = Generation()
        self.assertTrue(sorted(g.alive) == [])
        g.next()
        self.assertTrue(sorted(g.alive) == [])

    def testOne(self):
        g = Generation()
        g.add_cell(1, 1)
        self.assertTrue(sorted(g.alive) == [(1,1)])
        g.next()
        self.assertTrue(sorted(g.alive) == [])

    def testTriple(self):
        g = Generation()
        g.add_cell(1,1)
        g.add_cell(2,1)
        g.add_cell(1,2)
        g.next()
        self.assertTrue(sorted(g.alive) == [(1,1), (1,2), (2,1), (2,2)])
        g.next()
        self.assertTrue(sorted(g.alive) == [(1,1), (1,2), (2,1), (2,2)])

    def test3x3(self):
        g = Generation()
        for c in [(x,y) for x in range(0,3) for y in range(0,3)]:
            g.add_cell(*c)
        g.next()
        self.assertEquals(sorted(g.alive), [(-1,1),(0,0),(0,2),(1,-1),(1,3),(2,0),(2,2),(3,1)])

unittest.main()
