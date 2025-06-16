from typing import List, Tuple
import math
import random
from collections import deque

def manhattan_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def get_neighbors(maze: List[List[int]], pos: Tuple[int, int], target: Tuple[int, int] = None) -> List[Tuple[int, int]]:
    """Return valid neighboring positions, sorted by distance to target if provided."""
    rows, cols = len(maze), len(maze[0])
    r, c = pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != 1:
            neighbors.append((nr, nc))
    if target:
        neighbors.sort(key=lambda x: manhattan_distance(x, target))
        if len(neighbors) > 1:
            for i in range(len(neighbors) - 1):
                if random.random() < 0.2:
                    neighbors[i], neighbors[i + 1] = neighbors[i + 1], neighbors[i]
    else:
        random.shuffle(neighbors)
    return neighbors

def bfs_path(maze: List[List[int]], start: Tuple[int, int], target: Tuple[int, int]) -> Tuple[int, int]:
    """Find the next move toward target using BFS, or return start if no path exists."""
    rows, cols = len(maze), len(maze[0])
    queue = deque([start])
    visited = set([start])
    came_from = {}
    
    while queue:
        pos = queue.popleft()
        if pos == target:
            # Reconstruct path and return the first move
            current = pos
            while current in came_from and came_from[current] != start:
                current = came_from[current]
            return current if current != start else pos
        for neighbor in get_neighbors(maze, pos):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = pos
                queue.append(neighbor)
    
    print(f"No path found from {start} to {target}")
    neighbors = get_neighbors(maze, start)
    return random.choice(neighbors) if neighbors else start

def evaluate_state(player_pos: Tuple[int, int], ai_pos: Tuple[int, int], key: Tuple[int, int], goal: Tuple[int, int], ai_has_key: bool, player_has_key: bool, prev_ai_pos: Tuple[int, int]) -> int:
    """Evaluate the state from AI's perspective, prioritizing progress and blocking player."""
    if ai_pos == goal and ai_has_key:
        return 100000
    if player_pos == goal and player_has_key:
        return -100000

    ai_target = key if not ai_has_key else goal
    ai_dist = manhattan_distance(ai_pos, ai_target)
    player_target = key if not player_has_key else goal
    player_dist = manhattan_distance(player_pos, player_target)

    key_penalty = -1500 if not ai_has_key and ai_dist > 0 else 0
    penalty = -1000 if ai_pos == prev_ai_pos else 0  # Increased penalty
    block_bonus = 250 if manhattan_distance(ai_pos, player_target) <= 2 else 0
    random_factor = random.uniform(-10, 10)

    score = player_dist - 6 * ai_dist + key_penalty + penalty + block_bonus + random_factor
    print(f"Evaluate: AI at {ai_pos}, target {ai_target}, score {score}, dist {ai_dist}, block_bonus {block_bonus}")
    return score

def alpha_beta(maze: List[List[int]], player_pos: Tuple[int, int], ai_pos: Tuple[int, int], key: Tuple[int, int], goal: Tuple[int, int], depth: int, alpha: float, beta: float, is_maximizing: bool, ai_has_key: bool, player_has_key: bool, prev_ai_pos: Tuple[int, int]) -> Tuple[int, Tuple[int, int]]:
    """Alpha-Beta Pruning to optimize Minimax."""
    if depth == 0 or (ai_pos == goal and ai_has_key) or (player_pos == goal and player_has_key):
        return evaluate_state(player_pos, ai_pos, key, goal, ai_has_key, player_has_key, prev_ai_pos), ai_pos

    ai_target = key if not ai_has_key else goal
    if is_maximizing:
        best_value = -math.inf
        best_move = ai_pos
        next_ai_has_key = ai_has_key or ai_pos == key
        neighbors = get_neighbors(maze, ai_pos, ai_target)
        if not neighbors:
            print(f"No valid moves for AI at {ai_pos}")
            return evaluate_state(player_pos, ai_pos, key, goal, ai_has_key, player_has_key, prev_ai_pos), ai_pos
        for move in neighbors:
            value, _ = alpha_beta(maze, player_pos, move, key, goal, depth - 1, alpha, beta, False, next_ai_has_key, player_has_key, ai_pos)
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        print(f"AI move chosen: {best_move}, value: {best_value}")
        return best_value, best_move
    else:
        best_value = math.inf
        best_move = player_pos
        next_player_has_key = player_has_key or player_pos == key
        for move in get_neighbors(maze, player_pos):
            value, _ = alpha_beta(maze, move, ai_pos, key, goal, depth - 1, alpha, beta, True, ai_has_key, next_player_has_key, ai_pos)
            if value < best_value:
                best_value = value
                best_move = move
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_value, best_move

def minimax_move(maze: List[List[int]], player_pos: Tuple[int, int], ai_pos: Tuple[int, int], key: Tuple[int, int], goal: Tuple[int, int], prev_ai: Tuple[int, int] = None, ai_has_key: bool = False, player_has_key: bool = False) -> Tuple[int, int]:
    """Return the AI's next move using Alpha-Beta Pruning with BFS fallback."""
    try:
        print(f"Calculating AI move: pos={ai_pos}, target={'key' if not ai_has_key else 'goal'}, prev={prev_ai or ai_pos}")
        ai_target = key if not ai_has_key else goal
        old_dist = manhattan_distance(ai_pos, ai_target)
        _, move = alpha_beta(maze, player_pos, ai_pos, key, goal, depth=4, alpha=-math.inf, beta=math.inf, is_maximizing=True, ai_has_key=ai_has_key, player_has_key=player_has_key, prev_ai_pos=prev_ai or ai_pos)
        
        # Validate move
        ar, ac = move
        if not (0 <= ar < len(maze) and 0 <= ac < len(maze[0]) and maze[ar][ac] != 1):
            print(f"Invalid AI move {move}, using BFS fallback")
            move = bfs_path(maze, ai_pos, ai_target)
        
        # Check if move advances toward target
        new_dist = manhattan_distance(move, ai_target)
        if move == ai_pos or new_dist >= old_dist:
            print(f"AI move {move} does not advance (old_dist={old_dist}, new_dist={new_dist}), using BFS fallback")
            move = bfs_path(maze, ai_pos, ai_target)
        
        print(f"AI move selected: {move}")
        return move
    except Exception as e:
        print(f"Error in minimax_move: {str(e)}, using BFS fallback")
        neighbors = get_neighbors(maze, ai_pos)
        if neighbors:
            return bfs_path(maze, ai_pos, key if not ai_has_key else goal)
        return ai_pos