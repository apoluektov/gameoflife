import pygame

from life import *

pygame.init()
screen = pygame.display.set_mode((640,480))


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


def draw():

    draw_board(640, 480, 8)
    draw_generation(g, 640, 480, 8)

    pygame.display.flip()


def draw_board(w, h, s):
    r = pygame.Rect(0, 0, w, h)
    pygame.draw.rect(screen,(255,255,255),r)

    for x in range(0, w/s):
        pygame.draw.line(screen,(220,220,220),(x*s,0),(x*s,h))

    for y in range(0, h/s):
        pygame.draw.line(screen,(220,220,220),(0,y*s),(w,y*s))


def draw_generation(g, w, h, s):
    for c in g.alive:
        draw_cell(w, h, s, *c)

def draw_cell(w, h, s, x, y):
    r = pygame.Rect(w/2 + x*s, h/2 + y*s, s-1, s-1)
    pygame.draw.rect(screen, (0,0,0), r)


def run(ms_generation):
    t0 = pygame.time.get_ticks()
    while True:
        t = pygame.time.get_ticks()
        if t - t0 >= ms_generation:
            g.next()
            t0 = t
        draw()


run(10)
