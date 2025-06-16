import random
from collections import deque

MAZE_SIZE = 10
OBSTACLE_PERCENTAGE = 0.2

def is_reachable(maze, start, target):
    """Check if target is reachable from start using BFS."""
    rows, cols = len(maze), len(maze[0])
    visited = set([start])
    queue = deque([start])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        r, c = queue.popleft()
        if (r, c) == target:
            return True
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited and maze[nr][nc] != 1:
                visited.add((nr, nc))
                queue.append((nr, nc))
    return False

def has_valid_move(maze, pos):
    """Check if position has at least one valid move."""
    rows, cols = len(maze), len(maze[0])
    r, c = pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != 1:
            return True
    return False

def generate_maze():
    maze = [[0 for _ in range(MAZE_SIZE)] for _ in range(MAZE_SIZE)]

    # Place player start
    start = (0, 0)  # Fixed start position
    maze[start[0]][start[1]] = 2

    # Place key
    key = (random.randint(0, 9), random.randint(0, 9))
    while key == start or not is_reachable(maze, start, key):
        key = (random.randint(0, 9), random.randint(0, 9))
    maze[key[0]][key[1]] = 3

    # Place treasure
    treasure = (random.randint(0, 9), random.randint(0, 9))
    while treasure in [start, key] or not is_reachable(maze, key, treasure):
        treasure = (random.randint(0, 9), random.randint(0, 9))
    maze[treasure[0]][treasure[1]] = 4

    # Place AI
    ai = (random.randint(0, 9), random.randint(0, 9))
    while ai in [start, key, treasure] or not has_valid_move(maze, ai) or not is_reachable(maze, ai, key):
        ai = (random.randint(0, 9), random.randint(0, 9))
    maze[ai[0]][ai[1]] = 5

    # Add obstacles
    empty_cells = [(i, j) for i in range(MAZE_SIZE) for j in range(MAZE_SIZE) if maze[i][j] == 0]
    num_obstacles = int(len(empty_cells) * OBSTACLE_PERCENTAGE)
    obstacles = random.sample(empty_cells, num_obstacles)
    
    # Ensure obstacles don't block key paths
    for i, j in obstacles:
        maze[i][j] = 1
        if not (is_reachable(maze, start, key) and is_reachable(maze, key, treasure) and is_reachable(maze, ai, key)):
            maze[i][j] = 0  # Revert if path is blocked

    return {
        "maze": maze,
        "start": start,
        "key": key,
        "treasure": treasure,
        "ai": ai
    }