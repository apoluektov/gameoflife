# Copyright (c) 2011-2016 Alexander Poluektov (alexander.poluektov@gmail.com)
#
# Use, modification and distribution are subject to the MIT license
# (See accompanying file MIT-LICENSE)

import pygame
from life import *
import figures

# responsible for drawing the generation
class View:
    _cell_sizes = [2,3,5,8,13,21,34]

    # constructs new view using given board parameters
    def __init__(self, gen, width, height, zoom):
        self.gen = gen
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
        self.draw_board()
        self.draw_generation()
        self.draw_text()

        pygame.display.flip()

    def draw_board(self):
        r = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(self.screen,(255,255,255),r)
        self.draw_lines()

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

    def draw_generation(self):
        for c in self.gen.alive:
            self.draw_cell(*c)

    def draw_cell(self, x, y):
        s = self.cell_size()
        rs = s
        if s >= 4:
            rs = s-1
        cx, cy = self.center
        r = pygame.Rect(cx + x*s+1, cy + y*s+1, rs, rs)
        pygame.draw.rect(self.screen, (0,0,0), r)

    def draw_text(self):
        nstep_text = self.font.render('{0:06}'.format(self.gen.nstep), 1, (190,190,190))
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

    def set_cell_under_cursor_alive(self, alive):
        cell = self.screen_coords_to_cell(*self.cursor)
        if cell:
            gx, gy = cell
            if alive == 1:
                self.gen.add_cell(gx, gy)
            elif alive == 0:
                self.gen.remove_cell(gx, gy)
            else:
                raise ValueError('View.set_cell_under_cursor_alive() argument must be 0 or 1; got %s' % alive)


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
                        view.set_cell_under_cursor_alive(1)
                elif event.key == pygame.K_0:
                    if pause:
                        view.set_cell_under_cursor_alive(0)
            elif event.type == pygame.VIDEORESIZE:
                view.resize_board(event.w, event.h)

        t = pygame.time.get_ticks()
        if t - t0 >= ms_generation and not pause:
            generation.next()
            t0 = t
        view.draw()


def main():
    g = figures.complex()
    run(g, 50)


if __name__ == '__main__':
    main()
