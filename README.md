# 🏝️ Treasure Hunt Race

An interactive Python-based maze game where you race against an AI using pathfinding algorithms to reach the treasure first!

## 🎮 Game Overview

In *Treasure Hunt Race*, you play as a red square navigating a randomly generated maze. Your mission is to collect the **key** (yellow) and reach the **treasure** (green) before the **AI opponent** (purple) does.

You can test and compare three search algorithms in action:

- **BFS (Breadth-First Search)**
- **DFS (Depth-First Search)**
- **A\*** (A-Star Search)

The game visualizes the path, performance metrics (path length, nodes explored, and time), and tracks wins between the player and the AI.

---

## 🧠 Algorithms

Each algorithm explores the maze differently:

| Algorithm | Path Length | Nodes Explored | Time (ms) |
|-----------|-------------|----------------|-----------|
| BFS       | 20          | 124            | 8.30      |
| DFS       | 22          | 23             | 4.90      |
| A*        | 20          | 73             | 14.40     |

These values change depending on the maze generated.

---

## 🕹️ How to Play

- Use `W A S D` keys to move the player (red).
- You **must collect the key** (yellow) before reaching the treasure (green).
- Press `Play` to race against the AI (purple).
- Click `Show Path` to view how the selected algorithm solves the maze.
- Press `New Maze` to generate a new challenge.
- Your score (Player Wins vs. AI Wins) is tracked until reset.

---

## 🚀 Technologies Used

- **Python**
- **[Flask]** 
- **Algorithm logic for BFS, DFS, and A\***  

---