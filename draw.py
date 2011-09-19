# Copyright (c) 2011 Alexander Poluektov (alexander.poluektov@gmail.com)
#
# Use, modification and distribution are subject to the MIT license
# (See accompanyung file MIT-LICENSE)

import pygame
from life import *

# responsible for drawing the generation
class View:
    _cell_sizes = [2,3,5,8,13,21,34]

    # constructs new view using given board parameters
    def __init__(self, width, height, zoom):
        self.width = width
        self.height = height
        self.zoom = clamp(zoom, 0, len(View._cell_sizes))
        self.screen = pygame.display.set_mode((width,height), pygame.RESIZABLE)
        self.font = pygame.font.Font(None, 36)
        s = self.cell_size()
        self.center = ((self.width/2)/s*s, (self.height/2)/s*s)


    # draws the board and the generation
    def draw(self):
        self.draw_board()
        self.draw_generation(g)
        self.draw_text(g.nstep)

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

        for x in range(0, self.width/s + 1):
            pygame.draw.line(self.screen,color,(x*s,0),(x*s,self.height))

        for y in range(0, self.height/s + 1):
            pygame.draw.line(self.screen,color,(0,y*s),(self.width,y*s))

    def draw_generation(self, g):
        for c in g.alive:
            self.draw_cell(*c)

    def draw_cell(self, x, y):
        s = self.cell_size()
        rs = s
        if s >= 4:
            rs = s-1
        cx, cy = self.center
        r = pygame.Rect(cx + x*s+1, cy + y*s+1, rs, rs)
        pygame.draw.rect(self.screen, (0,0,0), r)

    def draw_text(self, n):
        text = self.font.render('{0:{f}6}'.format(n, f='0'), 1, (190,190,190))
        x, y = text.get_size()
        x, y = self.width - x - 10, 10
        self.screen.blit(text, (x,y))

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


def clamp(v, minv, maxv):
    return min(maxv, max(minv, v))


def run(generation, ms_generation):
    pygame.init()

    t0 = pygame.time.get_ticks()
    pause = False
    mouse_down = False
    view = View(640, 480, 3)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEMOTION:
                if mouse_down:
                    x, y = view.center
                    dx, dy = event.rel
                    view.center = x+dx, y+dy
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5:
                    view.increase_cellsize()
                elif event.button == 4:
                    view.decrease_cellsize()
                elif event.button == 3:
                    mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
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
            elif event.type == pygame.VIDEORESIZE:
                view.resize_board(event.w, event.h)

        t = pygame.time.get_ticks()
        if t - t0 >= ms_generation and not pause:
            generation.next()
            t0 = t
        view.draw()



g = Generation()
g.add_cell(0,0)
g.add_cell(0,1)
g.add_cell(0,2)
g.add_cell(1,1)
g.add_cell(1,2)
g.add_cell(1,0)
g.add_cell(2,0)
g.add_cell(2,1)
g.add_cell(2,2)
g.add_cell(3,0)
g.add_cell(3,1)
g.add_cell(3,2)
g.add_cell(4,0)
g.add_cell(4,1)
g.add_cell(4,2)

g.add_cell(-11+2,-10)
g.add_cell(-10+2,-10)
g.add_cell(-9+2,-10)
g.add_cell(-9+2,-11)
g.add_cell(-10+2,-12)


run(g, 50)
