class Generation(object):
    def __init__(self):
        self.min_x = 0
        self.min_y = 0
        self.max_x = 0
        self.max_y = 0
        self.alive = set()

    def add_cell(self, x, y):
        self.alive.add((x,y))
        self.min_x = min(self.min_x, x)
        self.min_y = min(self.min_y, y)
        self.max_x = max(self.max_x, x)
        self.max_y = max(self.max_y, y)

    def next(self):
        # 1: for all alive: find the next status
        # 2: for all adjacent to alive: find next alive
        new_alive = set()
        for c in self.alive:
            n = self.adjacent_alive(*c)
            if n == 2 or n == 3:
                new_alive.add(c)
        for c in self.alive:
            for c2 in self.adjacent(*c):
                n = self.adjacent_alive(*c2)
                if n == 3:
                    new_alive.add(c2)
        self.alive = new_alive

    def adjacent(self, x0, y0):
        return [(x,y) for x in range(x0-1,x0+2) for y in range(y0-1,y0+2) if (x,y) != (x0,y0)]

    def adjacent_alive(self, x, y):
        return len([c for c in self.adjacent(x,y) if c in self.alive])
