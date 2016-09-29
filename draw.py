# Copyright (c) 2011-2016 Alexander Poluektov (alexander.poluektov@gmail.com)
#
# Use, modification and distribution are subject to the MIT license
# (See accompanying file MIT-LICENSE)

import pygame
from life import *
import figures


class Board(object):
    def cell_color(self, x, y):
        return (255, 255, 255)

    def set_cell_color(self, x, y, color):
        pass

    def next_step(self):
        pass

    def step_count(self):
        return 0


# responsible for drawing the generation
class View:
    _cell_sizes = [2,3,5,8,13,21,34]

    # constructs new view using given board parameters
    # board parameter must model Board class shown above
    def __init__(self, board, width, height, zoom):
        self.board = board
        self.width = width
        self.height = height
        self.zoom = clamp(zoom, 0, len(View._cell_sizes))
        self.screen = pygame.display.set_mode((width,height), pygame.RESIZABLE)
        self.font = pygame.font.Font(None, 36)
        s = self.cell_size()
        self.center = ((self.width/2)/s*s, (self.height/2)/s*s)
        self.cursor = (0,0)


    # draws the board and the generation
    def draw(self):
        self.draw_background()
        self.draw_board()
        self.draw_lines()
        self.draw_text()

        pygame.display.flip()

    def draw_background(self):
        r = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(self.screen,(255,255,255),r)

    def draw_lines(self):
        s = self.cell_size()

        color = self.line_color()
        if color == (255,255,255):
            return

        cx, cy = self.center
        dx, dy = cx % s, cy % s

        for x in range(0, self.width/s + 1):
            pygame.draw.line(self.screen,color, (x*s + dx, 0), (x*s + dx, self.height))

        for y in range(0, self.height/s + 1):
            pygame.draw.line(self.screen, color, (0, y*s + dy), (self.width, y*s + dy))

    def draw_board(self):
        c0x, c0y = self.screen_coords_to_cell(1, 1)
        c1x, c1y = self.screen_coords_to_cell(self.width - 2, self.height - 2)
        for x in range(c0x, c1x + 1):
            for y in range(c0y, c1y + 1):
                color = self.board.cell_color(x, y)
                self.draw_cell(x, y, color)

    def draw_cell(self, x, y, color):
        s = self.cell_size()
        rs = s
        cx, cy = self.center
        r = pygame.Rect(cx + x*s+1, cy + y*s+1, rs, rs)
        pygame.draw.rect(self.screen, color, r)

    def draw_text(self):
        nstep_text = self.font.render('{0:06}'.format(self.board.step_count()), 1, (190,190,190))
        x, y = nstep_text.get_size()
        x, y = self.width - x - 10, 10
        self.screen.blit(nstep_text, (x,y))

        cell = self.screen_coords_to_cell(*self.cursor)
        if cell:
            gx, gy = cell
            coords_text = self.font.render('{0:+04}:{1:+04}'.format(gx, gy), 1, (190,190,190))
            x, y = coords_text.get_size()
            x, y = self.width - x - 10, y + 20
            self.screen.blit(coords_text, (x,y))

    def screen_coords_to_cell(self, sx, sy):
        # we exclude the border of the view
        # this is needed to being able to detect whether the screen cursor is in or out
        # (it is clamped by pygame to the view border)
        cx, cy = self.center
        s = self.cell_size()
        if sx > 0 and sx < self.width-1 and sy > 0 and sy < self.height-1:
            gx, gy = (sx - cx) / s, (sy - cy) / s
            return gx, gy
        else:
            return None

    def resize_board(self, w, h):
        self.width, self.height = w, h
        self.screen = pygame.display.set_mode((w,h), pygame.RESIZABLE)

    def increase_cellsize(self):
        self.zoom = min(self.zoom + 1, len(View._cell_sizes)-1)

    def decrease_cellsize(self):
        self.zoom = max(self.zoom - 1, 0)

    def cell_size(self):
        return View._cell_sizes[self.zoom]

    def line_color(self):
        s = self.cell_size()
        color = (0,0,0)
        if  s < 4:
            color = (255,255,255)
        elif s < 8:
            color = (245,245,245)
        else:
            color = (230,230,230)
        return color

    def set_cell_color_under_cursor(self, color):
        cell = self.screen_coords_to_cell(*self.cursor)
        if cell:
            gx, gy = cell
            self.board.set_cell_color(gx, gy, color)


def clamp(v, minv, maxv):
    return min(maxv, max(minv, v))


def run(generation, ms_generation):
    pygame.init()

    t0 = pygame.time.get_ticks()
    pause = False
    mouse_down = False
    view = View(generation, 640, 480, 3)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEMOTION:
                if mouse_down:
                    x, y = view.center
                    dx, dy = event.rel
                    view.center = x+dx, y+dy
                view.cursor = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5:
                    view.increase_cellsize()
                elif event.button == 4:
                    view.decrease_cellsize()
                elif event.button == 1:
                    mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_down = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_p:
                    pause = not pause
                elif event.key == pygame.K_s:
                    ms_generation *= 1.5
                elif event.key == pygame.K_f:
                    ms_generation /= 1.5
                elif event.key == pygame.K_SPACE:
                    if pause:
                        generation.next()
                elif event.key == pygame.K_1:
                    if pause:
                        view.set_cell_color_under_cursor((0,0,0))
                elif event.key == pygame.K_0:
                    if pause:
                        view.set_cell_color_under_cursor((255,255,255))
            elif event.type == pygame.VIDEORESIZE:
                view.resize_board(event.w, event.h)

        t = pygame.time.get_ticks()
        if t - t0 >= ms_generation and not pause:
            generation.next_step()
            t0 = t
        view.draw()


def main():
    g = figures.complex()
    run(g, 50)


if __name__ == '__main__':
    main()
