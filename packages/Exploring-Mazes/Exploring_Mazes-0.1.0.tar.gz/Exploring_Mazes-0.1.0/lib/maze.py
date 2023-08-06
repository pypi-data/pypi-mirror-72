class Maze():
    """We do '#' for walls and '.' for accessible tiles.

    There is also a start 'S' and an exit 'T'.
    The `grid` is an array of strings."""
    def __init__(self, height, width, grid):

        self.height = int(height)
        self.width = int(width)
        self.grid = grid
        self.start, self.end = self.find_start_exit()

    def __str__(self):
        """Display the grid of the maze.

        It adds a space between every chars for easier inspection."""
        return '\n'.join(' '.join(row) for row in self.grid)

    def pos(self, p):
        i, j = p
        return self.grid[j][i]

    def find_start_exit(self):
        for i in range(self.width):
            for j in range(self.height):
                p = (i, j)
                if self.pos(p) == 'S':
                    s = p
                elif self.pos(p) == 'T':
                    t = p
        return s, t
