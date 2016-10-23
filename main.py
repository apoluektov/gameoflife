#!/usr/bin/env python
# Copyright (c) 2011-2016 Alexander Poluektov (alexander.poluektov@gmail.com)
#
# Use, modification and distribution are subject to the MIT license
# (See accompanying file MIT-LICENSE)

import life
import life.figures
import window
import sys


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

    def run(self):
        import pygame
        t0 = pygame.time.get_ticks()
        while True:
            for event in pygame.event.get():
                self.window.process_event(event)

            if self.window.quit_requested:
                return

            t = pygame.time.get_ticks()
            if t - t0 >= self.window.step_time_ms and not self.window.pause:
                self.board.next_step()
                t0 = t

            self.draw()

    def draw(self):
        self.window.draw_background(self.style.background_color())
        self.draw_cells()
        self.draw_grid()
        self.draw_text()

        self.window.flip_display()

    def draw_cells(self):
        for (x,y) in self.board.alive:
            if self.window.is_visible(x, y):
                self.window.draw_cell(x, y, self.style.cell_color(1))
        if self.board.stage() & self.board.show_nascent:
            for (x,y) in self.board.nascent:
                if self.window.is_visible(x, y):
                    self.window.draw_cell(x, y, self.style.cell_color(3))
        if self.board.stage() & self.board.show_dying:
            if self.window.is_visible(x, y):
                for (x,y) in self.board.dying:
                    self.window.draw_cell(x, y, self.style.cell_color(2))

    def draw_grid(self):
        color = self.style.grid_color(self.window.cell_size())
        if color == self.style.background_color():
            return

        self.window.draw_grid(color)

    def draw_text(self):
        nstep_text = '{0:06}'.format(self.board.step_count())
        self.window.draw_text(nstep_text, 10, 10, self.style.text_color())

        cell = self.window.cell_under_cursor()
        if cell:
            gx, gy = cell
            coords_text = '{0:+04}:{1:+04}'.format(gx, gy)
            self.window.draw_text(coords_text, 10, 40, self.style.text_color())


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

    v = window.Window(board)
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
