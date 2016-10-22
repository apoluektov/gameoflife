#!/usr/bin/env python
# Copyright (c) 2011-2016 Alexander Poluektov (alexander.poluektov@gmail.com)
#
# Use, modification and distribution are subject to the MIT license
# (See accompanying file MIT-LICENSE)

import life
import life.figures
import window
import sys


class Style(window.DefaultStyle):
    def cell_color(self, state):
        if state == 0:
            return (255,255,255)
        elif state == 1:
            return (0,0,0)
        elif state == 2: # dying
            return (127,0,0)
        elif state == 3: # nascent
            return (127,255,127)


class Game(window.DefaultWindowListener):
    def __init__(self, window, board, style):
        super(Game, self).__init__(window)
        self.board = board
        self.style = style

        # self.cell_under_cursor = None

    def on_key_down(self, key):
        import pygame

        if pygame.K_0 <= key <= pygame.K_9:
            state = key - pygame.K_0
            if self.window.pause:
                cell = self.window.cell_under_cursor()
                if cell:
                    x, y = cell
                    self.board.set_cell_state(x, y, state)
        elif key == pygame.K_SPACE:
            if self.window.pause:
                self.board.next_step()
        else:
            super(Game, self).on_key_down(key)


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

    v = window.Window(board, style)
    game = Game(v, board, style)
    v.pause = args.pause
    v.run()


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
