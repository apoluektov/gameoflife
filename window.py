# Copyright (c) 2011-2016 Alexander Poluektov (alexander.poluektov@gmail.com)
#
# Use, modification and distribution are subject to the MIT license
# (See accompanying file MIT-LICENSE)

import pygame


class WindowListener(object):
    def __init__(self, window):
        window.set_listener(self)
        self.window = window

    def on_key_down(self, key):
        pass

    def on_key_up(self, key):
        pass

    def on_mouse_button_down(self):
        pass

    def on_mouse_button_up(self):
        pass

    def on_mouse_wheel(self, direction):
        pass

    def on_mouse_drag(self, dx, dy):
        pass


class  DefaultWindowListener(WindowListener):
    def __init__(self, window):
        WindowListener.__init__(self, window)

    def on_key_down(self, key):
        import pygame
        if key == pygame.K_ESCAPE:
            self.window.quit_requested = True
        elif key == pygame.K_p:
            self.window.pause = not self.window.pause
        elif key == pygame.K_s:
            self.window.step_time_ms *= 1.5
        elif key == pygame.K_f:
            self.window.step_time_ms /= 1.5

    def on_mouse_wheel(self, direction):
        if direction == 1:
            self.window.increase_cellsize()
        elif direction == -1:
            self.window.decrease_cellsize()

    def on_mouse_drag(self, dx, dy):
        self.window.drag_board(dx, dy)


# responsible for drawing the game content and for UI event dispatching
class Window(object):
    _cell_sizes = [2,3,5,8,13,21,34]

    def __init__(self, width=640, height=480, zoom=3, step_time_ms=200):
        pygame.init()

        self.width = width
        self.height = height
        self.zoom = clamp(zoom, 0, len(Window._cell_sizes))
        self.step_time_ms = step_time_ms
        self.screen = pygame.display.set_mode((width,height), pygame.RESIZABLE)
        self.font = pygame.font.Font(None, 36)
        s = self.cell_size()
        self.center = ((self.width/2)/s*s, (self.height/2)/s*s)
        self.cursor = (0,0)
        self.pause = False
        self.mouse_down = False
        self.quit_requested = False
        self.listener = None

    # listener parameter must model WindowListener
    def set_listener(self, listener):
        self.listener = listener

    def process_event(self, event):
        if event.type == pygame.QUIT:
            self.quit_requested = True
        elif event.type == pygame.MOUSEMOTION:
            if self.mouse_down:
                dx, dy = event.rel
                self.listener.on_mouse_drag(dx, dy)
            self.cursor = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 5:
                self.listener.on_mouse_wheel(1)
            elif event.button == 4:
                self.listener.on_mouse_wheel(-1)
            elif event.button == 1:
                self.mouse_down = True
                self.listener.on_mouse_button_down()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.mouse_down = False
                self.listener.on_mouse_button_up()
        elif event.type == pygame.KEYDOWN:
            self.listener.on_key_down(event.key)
        elif event.type == pygame.KEYUP:
            self.listener.on_key_up(event.key)
        elif event.type == pygame.VIDEORESIZE:
            self.resize(event.w, event.h)

    def drag_board(self, dx, dy):
        x, y = self.center
        self.center = x + dx, y + dy

    def flip_display(self):
        pygame.display.flip()

    def draw_background(self, color):
        r = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(self.screen, color, r)

    def draw_grid(self, color):
        s = self.cell_size()

        cx, cy = self.center
        dx, dy = cx % s, cy % s

        for x in range(0, self.width/s + 1):
            pygame.draw.line(self.screen,color, (x*s + dx, 0), (x*s + dx, self.height))

        for y in range(0, self.height/s + 1):
            pygame.draw.line(self.screen, color, (0, y*s + dy), (self.width, y*s + dy))

    def is_visible(self, x, y):
        c0x, c0y = self.screen_coords_to_cell(1, 1)
        c1x, c1y = self.screen_coords_to_cell(self.width - 2, self.height - 2)
        return c0x <= x <= c1x and c0y <= y <= c1y

    def draw_cell(self, x, y, color):
        s = self.cell_size()
        rs = s
        cx, cy = self.center
        r = pygame.Rect(cx + x*s+1, cy + y*s+1, rs, rs)
        pygame.draw.rect(self.screen, color, r)

    def draw_text(self, text, px, py, color):
        t = self.font.render(text, 1, color)
        self.screen.blit(t, (px, py))

    def screen_coords_to_cell(self, sx, sy):
        # we exclude the border of the view
        # this is needed to being able to detect whether the screen cursor is in or out
        # (it is clamped by pygame to the view border)
        cx, cy = self.center
        s = self.cell_size()
        if 0 < sx < self.width-1 and 0 < sy < self.height - 1:
            gx, gy = (sx - cx) / s, (sy - cy) / s
            return gx, gy
        else:
            return None

    def resize(self, w, h):
        self.width, self.height = w, h
        self.screen = pygame.display.set_mode((w,h), pygame.RESIZABLE)

    def increase_cellsize(self):
        self.zoom = min(self.zoom + 1, len(Window._cell_sizes) - 1)

    def decrease_cellsize(self):
        self.zoom = max(self.zoom - 1, 0)

    def cell_size(self):
        return Window._cell_sizes[self.zoom]

    def cell_under_cursor(self):
        return self.screen_coords_to_cell(*self.cursor)


def clamp(v, minv, maxv):
    return min(maxv, max(minv, v))
