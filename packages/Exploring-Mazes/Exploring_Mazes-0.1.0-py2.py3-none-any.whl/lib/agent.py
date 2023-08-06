from collections import deque


class Agent():
    def __init__(self, maze):
        self.maze = maze
        self.start = self.maze.start

    def valid_square(self, p):
        i, j = p
        return (-1 < j < self.maze.height
                and -1 < i < self.maze.width) and self.maze.pos(p) != '#'

    def move(self, pos, mov):
        return tuple(map(int.__add__, pos, mov))

    def possible_next(self, pos):
        ret = set()
        changes = {(0, 1), (0, -1), (1, 0), (-1, 0)}
        for change in changes:
            next_pos = self.move(pos, change)
            if self.valid_square(next_pos):
                ret.add(next_pos)
        return ret

    def final_state(self, pos):
        return True if pos == self.maze.end else False

    def rewind_path(self, final, parents):
        cur_pos = final
        path = deque([cur_pos])
        while True:
            parent_pos = parents.get(cur_pos, False)
            if not parent_pos:
                break
            cur_pos = parent_pos
            path.appendleft(cur_pos)
        return path

    def find_shortest_path(self):
        """Implement BFS to find the shortest path from S to T."""
        parents = {self.start: None}
        seen = {self.start}
        q = deque([self.start])
        while q:
            cur_pos = q.popleft()
            if self.final_state(cur_pos):
                return self.rewind_path(cur_pos, parents)
            for next_pos in self.possible_next(cur_pos):
                if not next_pos in seen:
                    parents[next_pos] = cur_pos
                    seen.add(next_pos)
                    q.append(next_pos)

    def shortest_path_length(self):
        shortest_path = self.find_shortest_path()
        dist = -1
        while shortest_path:
            shortest_path.pop()
            dist += 1
        return dist if dist != -1 else "DOOMED"
