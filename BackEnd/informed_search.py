from heapq import heappush, heappop
from typing import List, Tuple
import math

def euclidean_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def get_neighbors(maze: List[List[int]], pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Return valid neighboring positions (up, down, left, right)."""
    rows, cols = len(maze), len(maze[0])
    r, c = pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != 1:
            neighbors.append((nr, nc))
    return neighbors

def reconstruct_path(came_from: dict, current: Tuple[Tuple[int, int], bool], max_iterations: int = 1000) -> List[Tuple[int, int]]:
    """Reconstruct path from came_from dict using (position, has_key) states."""
    path = [current[0]]
    seen = set([current])
    iterations = 0
    while current in came_from:
        next_current = came_from[current]
        if next_current in seen or next_current == current:
            break
        current = next_current
        path.append(current[0])
        seen.add(current)
        iterations += 1
        if iterations > max_iterations:
            print("Warning: Path reconstruction exceeded max iterations.")
            break
    return path[::-1]

def a_star(maze: List[List[int]], start: Tuple[int, int], key: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[List[Tuple[int, int]], int]:
    def heuristic(pos: Tuple[int, int], has_key: bool) -> float:
        return euclidean_distance(pos, goal if has_key else key)

    open_set = [(0, start, False)]
    came_from = {}
    g_score = {(start, False): 0}
    visited = set()
    nodes_explored = 0

    while open_set:
        _, current, has_key = heappop(open_set)
        nodes_explored += 1

        if (current, has_key) in visited:
            continue
        visited.add((current, has_key))

        if current == goal and has_key:
            return reconstruct_path(came_from, (current, has_key)), nodes_explored

        next_has_key = has_key or current == key

        for neighbor in get_neighbors(maze, current):
            state = (neighbor, next_has_key)
            temp_g = g_score.get((current, has_key), float('inf')) + 1
            if temp_g < g_score.get(state, float('inf')):
                g_score[state] = temp_g
                came_from[state] = (current, has_key)
                f_score = temp_g + heuristic(neighbor, next_has_key)
                heappush(open_set, (f_score, neighbor, next_has_key))

    return [], nodes_explored