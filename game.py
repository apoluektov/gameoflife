import window


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