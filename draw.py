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

    draw_board()
    draw_generation(g)

    pygame.display.flip()


def draw_board():
    r = pygame.Rect(0, 0, 640, 480)
    pygame.draw.rect(screen,(255,255,255),r)

    for x in range(0,80):
        pygame.draw.line(screen,(220,220,220),(x*8,0),(x*8,480))

    for y in range(0,60):
        pygame.draw.line(screen,(220,220,220),(0,y*8),(640,y*8))


def draw_generation(g):
    for c in g.alive:
        draw_cell(*c)

def draw_cell(x,y):
    r = pygame.Rect(320+x*8, 240+y*8, 7, 7)
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
