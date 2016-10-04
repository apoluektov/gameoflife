# Copyright (c) 2011-2016 Alexander Poluektov (alexander.poluektov@gmail.com)
#
# Use, modification and distribution are subject to the MIT license
# (See accompanying file MIT-LICENSE)

import life
import life.figures
import view
import sys

import argparse

argparser = argparse.ArgumentParser(description='Conway\'s Game of Life sumulation.')
argparser.add_argument('--pause', action="store_true", help='start game in pause mode (default: false)')
argparser.add_argument('--code', default='B3/S23', help='born/survives game code (default: B3/S23)')
argparser.add_argument('--figure', default='collision', help='initial figure on the board')
argparser.add_argument('--list-figures', action='store_true', help='list availiable figures to use with --figure flag')


def main():
    args = argparser.parse_args()
    if args.list_figures:
        print_figure_list(life.figures.list_figures())
        sys.exit(0)
    board = life.Board(args.code)
    try:
        life.figures.add_figure(board, args.figure)
    except KeyError as detail:
        print 'No such figure in catalog: %s' % detail
        sys.exit(1)
    s = life.Style()
    v = view.View(board, s, 640, 480, 3)
    v.pause = args.pause
    v.run(200)


def print_figure_list(figures):
    for name, alt in figures:
        print name,
        if alt:
            print '(',
            for n in alt:
                print n,
            print ')'
        if not alt:
            print


if __name__ == '__main__':
    main()
