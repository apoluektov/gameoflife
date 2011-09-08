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


class View:
    def draw(self):

        self.draw_board(640, 480, 12)
        self.draw_generation(g, 640, 480, 12)

        pygame.display.flip()


    def draw_board(self, w, h, s):
        r = pygame.Rect(0, 0, w, h)
        pygame.draw.rect(screen,(255,255,255),r)

        for x in range(0, w/s + 1):
            pygame.draw.line(screen,(220,220,220),(x*s,0),(x*s,h))

        for y in range(0, h/s + 1):
            pygame.draw.line(screen,(220,220,220),(0,y*s),(w,y*s))


    def draw_generation(self, g, w, h, s):
        for c in g.alive:
            self.draw_cell(w, h, s, *c)

    def draw_cell(self, w, h, s, x, y):
        r = pygame.Rect((w/2)/s*s + x*s+1, (h/2)/s*s + y*s+1, s-1, s-1)
        pygame.draw.rect(screen, (0,0,0), r)


def run(ms_generation):
    t0 = pygame.time.get_ticks()
    pause = False
    view = View()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEMOTION:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_p:
                    pause = not pause
                elif event.key == pygame.K_SPACE:
                    pass

        t = pygame.time.get_ticks()
        if t - t0 >= ms_generation and not pause:
            g.next()
            t0 = t
        view.draw()


run(10)
