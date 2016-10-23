#!/usr/bin/env python
# Copyright (c) 2011-2016 Alexander Poluektov (alexander.poluektov@gmail.com)
#
# Use, modification and distribution are subject to the MIT license
# (See accompanying file MIT-LICENSE)

import sys

import life
import life.figures
import window
from game import Game


class Style(object):
    def background_color(self):
        return (255,255,255)

    def grid_color(self, cell_size):
        if cell_size < 4:
            return (255,255,255)
        elif cell_size < 8:
            return (245,245,245)
        else:
            return (230,230,230)

    def text_color(self):
        return (190,190,190)

    def cell_color(self, state):
        if state == 0:
            return (255,255,255)
        elif state == 1:
            return (0,0,0)
        elif state == 2: # dying
            return (127,0,0)
        elif state == 3: # nascent
            return (127,255,127)


def main():
    args = parse_args()
    if args.list_figures:
        print_figure_list()
        sys.exit(0)
    board = life.Board(args.code, args.show_intermediate)
    try:
        life.figures.add_figure(board, args.figure)
    except KeyError as detail:
        print 'No such figure in catalog: %s' % detail
        sys.exit(1)
    style = Style()

    v = window.Window()
    game = Game(v, board, style)
    v.pause = args.pause
    game.run()


def parse_args():
    import argparse

    argparser = argparse.ArgumentParser(description='Conway\'s Game of Life simulation.')
    argparser.add_argument('--pause', action="store_true", help='start game in pause mode (default: false)')
    argparser.add_argument('--code', default='B3/S23', help='born/survives game code (default: B3/S23)')
    argparser.add_argument('--figure', default='collision', help='initial figure on the board')
    argparser.add_argument('--list-figures', action='store_true', help='list available figures to use with --figure flag')
    argparser.add_argument('--show-intermediate', action='store_true', help='show which cells are about to be born or die')

    return argparser.parse_args()


def print_figure_list():
    categories = life.figures.list_figures_by_category()
    for cat, fs in categories:
        print '%s:' % cat
        for f in fs:
            alt = ''
            if f.alt:
                alt = ' (%s' % f.alt[0]
                for a in f.alt[1:]:
                    alt += ', %s' % a
                alt += ')'
            print '  %s%s' % (f.name, alt)


if __name__ == '__main__':
    main()
