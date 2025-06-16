from collections import deque
from typing import List, Tuple

def get_neighbors(maze: List[List[int]], pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    rows, cols = len(maze), len(maze[0])
    r, c = pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    neighbors = []
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != 1:
            neighbors.append((nr, nc))
    return neighbors

def reconstruct_path(came_from: dict, end: Tuple[Tuple[int, int], bool]) -> List[Tuple[int, int]]:
    path = [end[0]]
    while end in came_from:
        end = came_from[end]
        path.append(end[0])
    return path[::-1]

def bfs(maze: List[List[int]], start: Tuple[int, int], key: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], int]:
    queue = deque([(start, False)])  # (pos, has_key)
    visited = set([(start, False)])
    came_from = {}
    nodes_explored = 0

    while queue:
        pos, has_key = queue.popleft()
        nodes_explored += 1

        if pos == goal and has_key:
            return reconstruct_path(came_from, (pos, has_key)), nodes_explored

        next_has_key = has_key or pos == key
        for neighbor in get_neighbors(maze, pos):
            state = (neighbor, next_has_key)
            if state not in visited:
                visited.add(state)
                came_from[state] = (pos, has_key)
                queue.append(state)

    return [], nodes_explored

def dfs(maze: List[List[int]], start: Tuple[int, int], key: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], int]:
    stack = [(start, False)]  # (pos, has_key)
    visited = set([(start, False)])
    came_from = {}
    nodes_explored = 0

    while stack:
        pos, has_key = stack.pop()
        nodes_explored += 1

        if pos == goal and has_key:
            return reconstruct_path(came_from, (pos, has_key)), nodes_explored

        next_has_key = has_key or pos == key
        for neighbor in get_neighbors(maze, pos):
            state = (neighbor, next_has_key)
            if state not in visited:
                visited.add(state)
                came_from[state] = (pos, has_key)
                stack.append(state)

    return [], nodes_explored