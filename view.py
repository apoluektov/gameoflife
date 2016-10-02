# Copyright (c) 2011-2016 Alexander Poluektov (alexander.poluektov@gmail.com)
#
# Use, modification and distribution are subject to the MIT license
# (See accompanying file MIT-LICENSE)

import pygame


class Board(object):
    def cell_state(self, x, y):
        return 0

    # unsupported states should be ignored by the implementations
    def set_cell_state(self, x, y, st):
        pass

    def next_step(self):
        pass

    def step_count(self):
        return 0


class Style:
    def color_for(self, state):
        return (255, 255, 255)


# responsible for drawing the board
class View:
    _cell_sizes = [2,3,5,8,13,21,34]

    # constructs new view using given board parameters
    # board parameter must model Board class shown above
    def __init__(self, board, style, width, height, zoom):
        pygame.init()

        self.board = board
        self.style = style
        self.width = width
        self.height = height
        self.zoom = clamp(zoom, 0, len(View._cell_sizes))
        self.screen = pygame.display.set_mode((width,height), pygame.RESIZABLE)
        self.font = pygame.font.Font(None, 36)
        s = self.cell_size()
        self.center = ((self.width/2)/s*s, (self.height/2)/s*s)
        self.cursor = (0,0)
        self.mouse_down = False
        self.quit_requested = False

    def run(self, step_time_ms):
        self.step_time_ms = step_time_ms
        t0 = pygame.time.get_ticks()
        while True:
            for event in pygame.event.get():
                self.process_event(event)

            if self.quit_requested:
                return

            t = pygame.time.get_ticks()
            if t - t0 >= self.step_time_ms and not self.pause:
                self.board.next_step()
                t0 = t
            self.draw()

    def process_event(self, event):
        if event.type == pygame.QUIT:
            self.quit_requested = True
        elif event.type == pygame.MOUSEMOTION:
            if self.mouse_down:
                x, y = self.center
                dx, dy = event.rel
                self.center = x+dx, y+dy
            self.cursor = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 5:
                self.increase_cellsize()
            elif event.button == 4:
                self.decrease_cellsize()
            elif event.button == 1:
                self.mouse_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.mouse_down = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.quit_requested = True
            elif event.key == pygame.K_p:
                self.pause = not self.pause
            elif event.key == pygame.K_s:
                self.step_time_ms *= 1.5
            elif event.key == pygame.K_f:
                self.step_time_ms /= 1.5
            elif event.key == pygame.K_SPACE:
                if self.pause:
                    self.board.next_step()
            elif event.key >= pygame.K_0 and event.key <= pygame.K_9:
                state = event.key - pygame.K_0
                if self.pause:
                    self.set_cell_state_under_cursor(state)
        elif event.type == pygame.VIDEORESIZE:
            self.resize_board(event.w, event.h)


    # draws the board and the board
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
                color = self.style.color_for(self.board.cell_state(x, y))
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

    def set_cell_state_under_cursor(self, st):
        cell = self.screen_coords_to_cell(*self.cursor)
        if cell:
            gx, gy = cell
            self.board.set_cell_state(gx, gy, st)


def clamp(v, minv, maxv):
    return min(maxv, max(minv, v))
