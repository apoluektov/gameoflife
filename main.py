# Copyright (c) 2011-2016 Alexander Poluektov (alexander.poluektov@gmail.com)
#
# Use, modification and distribution are subject to the MIT license
# (See accompanying file MIT-LICENSE)

import life
import life.figures
import view

import argparse

argparser = argparse.ArgumentParser(description='Conway\'s Game of Life sumulation.')
argparser.add_argument('--pause', action="store_true", help='start game in pause mode (default: false)')
argparser.add_argument('--code', default='B3/S23', help='born/survives game code (default: B3/S23)')

def main():
    args = argparser.parse_args()
    board = life.Board(args.code)
    life.figures.add_figure(board, life.figures.complex)
    s = life.Style()
    v = view.View(board, s, 640, 480, 3)
    v.pause = args.pause
    v.run(200)


if __name__ == '__main__':
    main()
