import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import unittest
from maze_generator import generate_maze
from uninformed_search import bfs, dfs
from informed_search import a_star
from ai_opponent import minimax_move

class TestMazeGame(unittest.TestCase):
    def test_maze_generation(self):
        """Test that generate_maze produces a valid 10x10 maze."""
        maze_data = generate_maze()
        maze = maze_data["maze"]
        start = maze_data["start"]
        key = maze_data["key"]
        goal = maze_data["treasure"]

        # Check size
        self.assertEqual(len(maze), 10, "Maze should have 10 rows")
        self.assertEqual(len(maze[0]), 10, "Maze should have 10 columns")

        # Count elements
        start_count = sum(row.count(2) for row in maze)
        key_count = sum(row.count(3) for row in maze)
        treasure_count = sum(row.count(4) for row in maze)

        self.assertEqual(start_count, 1, "Maze should have exactly one start (2)")
        self.assertEqual(key_count, 1, "Maze should have exactly one key (3)")
        self.assertEqual(treasure_count, 1, "Maze should have exactly one treasure (4)")

    def test_bfs_simple_maze(self):
        """Test BFS on a simple 3x3 maze."""
        simple_maze = [
            [2, 0, 0],
            [0, 0, 0],
            [0, 3, 4]
        ]
        start = (0, 0)
        key = (2, 1)
        goal = (2, 2)

        path = bfs(simple_maze, start, key, goal)
        self.assertTrue(path, "BFS should find a path")
        self.assertEqual(path[0], start, "Path should start at start position")
        self.assertEqual(path[-1], goal, "Path should end at treasure")
        self.assertIn(key, path, "Path should visit key")
        self.assertTrue(key in path[:path.index(goal)], "Path should visit key before treasure")

    def test_dfs_simple_maze(self):
        """Test DFS on a simple 3x3 maze."""
        simple_maze = [
            [2, 0, 0],
            [0, 0, 0],
            [0, 3, 4]
        ]
        start = (0, 0)
        key = (2, 1)
        goal = (2, 2)

        path = dfs(simple_maze, start, key, goal)
        self.assertTrue(path, "DFS should find a path")
        self.assertEqual(path[0], start, "Path should start at start position")
        self.assertEqual(path[-1], goal, "Path should end at treasure")
        self.assertIn(key, path, "Path should visit key")
        self.assertTrue(key in path[:path.index(goal)], "Path should visit key before treasure")

    def test_a_star_simple_maze(self):
        """Test A* on a simple 3x3 maze."""
        simple_maze = [
            [2, 0, 0],
            [0, 0, 0],
            [0, 3, 4]
        ]
        start = (0, 0)
        key = (2, 1)
        goal = (2, 2)

        path = a_star(simple_maze, start, key, goal)
        self.assertTrue(path, "A* should find a path")
        self.assertEqual(path[0], start, "Path should start at start position")
        self.assertEqual(path[-1], goal, "Path should end at treasure")
        self.assertIn(key, path, "Path should visit key")
        self.assertTrue(key in path[:path.index(goal)], "Path should visit key before treasure")

    def test_minimax_move_toward_key(self):
        """Test minimax_move directs AI toward key."""
        simple_maze = [
            [2, 0, 0],
            [0, 0, 0],
            [0, 3, 4]
        ]
        player_pos = (0, 0)
        ai_pos = (1, 1)
        key = (2, 1)
        goal = (2, 2)

        move = minimax_move(simple_maze, player_pos, ai_pos, key, goal)
        expected_moves = [(1, 2), (2, 1), (1, 0), (0, 1)]  # Valid neighbors
        self.assertIn(move, expected_moves, "AI move should be a valid neighbor")
        old_dist = abs(ai_pos[0] - key[0]) + abs(ai_pos[1] - key[1])
        new_dist = abs(move[0] - key[0]) + abs(move[1] - key[1])
        self.assertLessEqual(new_dist, old_dist, "AI should move closer to or stay at key")

    def test_minimax_move_toward_goal(self):
        """Test minimax_move directs AI toward treasure when it has the key."""
        simple_maze = [
            [2, 0, 0],
            [0, 0, 0],
            [0, 3, 4]
        ]
        player_pos = (0, 0)
        ai_pos = (2, 1)  # At key
        key = (2, 1)
        goal = (2, 2)

        move = minimax_move(simple_maze, player_pos, ai_pos, key, goal)
        expected_moves = [(2, 2), (2, 0), (1, 1)]  # Valid neighbors
        self.assertIn(move, expected_moves, "AI move should be a valid neighbor")
        old_dist = abs(ai_pos[0] - goal[0]) + abs(ai_pos[1] - goal[1])
        new_dist = abs(move[0] - goal[0]) + abs(move[1] - goal[1])
        self.assertLessEqual(new_dist, old_dist, "AI should move closer to or stay at goal")

if __name__ == '__main__':
    unittest.main()