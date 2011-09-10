import pygame

from life import *

pygame.init()
screen = pygame.display.set_mode((640,480), pygame.RESIZABLE)


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


class View:
    _cell_sizes = [2,3,5,8,13,21,34]

    def __init__(self, w, h, z):
        self.width = w
        self.height = h
        self.zoom = z

    def draw(self):
        self.draw_board()
        self.draw_generation(g)

        pygame.display.flip()


    def draw_board(self):
        r = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(screen,(255,255,255),r)
        if View._cell_sizes[self.zoom] >= 4:
            self.draw_lines()

    def draw_lines(self):
        s = View._cell_sizes[self.zoom]

        color = (230,230,230)
        if s < 8:
            color = (245,245,245)

        for x in range(0, self.width/s + 1):
            pygame.draw.line(screen,color,(x*s,0),(x*s,self.height))

        for y in range(0, self.height/s + 1):
            pygame.draw.line(screen,color,(0,y*s),(self.width,y*s))


    def draw_generation(self, g):
        for c in g.alive:
            self.draw_cell(*c)

    def draw_cell(self, x, y):
        s = View._cell_sizes[self.zoom]
        rs = s
        if s >= 4:
            rs = s-1
        r = pygame.Rect((self.width/2)/s*s + x*s+1, (self.height/2)/s*s + y*s+1, rs, rs)
        pygame.draw.rect(screen, (0,0,0), r)

    def increase_cellsize(self):
        self.zoom = min(self.zoom + 1, len(View._cell_sizes)-1)

    def decrease_cellsize(self):
        self.zoom = max(self.zoom - 1, 0)


def run(ms_generation):
    t0 = pygame.time.get_ticks()
    pause = False
    view = View(640, 480, 3)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEMOTION:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5:
                    view.increase_cellsize()
                elif event.button == 4:
                    view.decrease_cellsize()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_p:
                    pause = not pause
                elif event.key == pygame.K_SPACE:
                    pass
            elif event.type == pygame.VIDEORESIZE:
                view.width, view.height = event.w, event.h
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

        t = pygame.time.get_ticks()
        if t - t0 >= ms_generation and not pause:
            g.next()
            t0 = t
        view.draw()


run(10)
