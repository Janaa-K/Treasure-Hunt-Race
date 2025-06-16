from flask import Flask, jsonify, request, send_from_directory
from maze_generator import generate_maze
from uninformed_search import bfs, dfs
from informed_search import a_star
from ai_opponent import minimax_move
import os

app = Flask(__name__, static_folder="../FrontEnd")

@app.route('/')
def home():
    try:
        if not os.path.exists(os.path.join(app.static_folder, 'index.html')):
            return jsonify({"error": "index.html not found in FrontEnd folder"}), 500
        return send_from_directory(app.static_folder, 'index.html')
    except Exception as e:
        return jsonify({"error": f"Failed to serve index.html: {str(e)}"}), 500

@app.route('/static/<path:path>')
def serve_static(path):
    try:
        if not os.path.exists(os.path.join(app.static_folder, 'static', path)):
            return jsonify({"error": f"Static file {path} not found"}), 404
        return send_from_directory(os.path.join(app.static_folder, 'static'), path)
    except Exception as e:
        return jsonify({"error": f"Failed to serve static file {path}: {str(e)}"}), 500

@app.route('/generate-maze', methods=['GET'])
def generate_maze_route():
    try:
        maze_data = generate_maze()
        if not maze_data or 'maze' not in maze_data:
            return jsonify({"error": "Invalid maze data returned from generate_maze"}), 500
        print(f"Generated maze, Player start: {maze_data['start']}, AI start: {maze_data['ai']}, Key: {maze_data['key']}, Treasure: {maze_data['treasure']}")
        return jsonify({
            "maze": maze_data["maze"],
            "start": maze_data["start"],
            "key": maze_data["key"],
            "goal": maze_data["treasure"],
            "ai": maze_data["ai"],
            "player_has_key": False,
            "ai_has_key": False
        })
    except Exception as e:
        return jsonify({"error": f"Failed to generate maze: {str(e)}"}), 500

@app.route('/search-path', methods=['POST'])
def search_path_route():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        maze = data.get('maze')
        algo = data.get('algo')
        start = tuple(data.get('start'))
        key = tuple(data.get('key'))
        goal = tuple(data.get('goal'))

        if None in [maze, algo, start, key, goal]:
            return jsonify({"error": "Missing required maze data"}), 400

        if algo == 'bfs':
            path, nodes_explored = bfs(maze, start, key, goal)
        elif algo == 'dfs':
            path, nodes_explored = dfs(maze, start, key, goal)
        elif algo == 'astar':
            path, nodes_explored = a_star(maze, start, key, goal)
        else:
            return jsonify({"error": "Invalid algorithm selected"}), 400

        print(f"Search path with {algo}, Path length: {len(path) if path else 0}, Nodes: {nodes_explored}")
        return jsonify({
            "path": path,
            "start": start,
            "key": key,
            "goal": goal,
            "nodes_explored": nodes_explored
        })
    except Exception as e:
        print(f"Error in search-path: {str(e)}")
        return jsonify({"error": f"Failed to search path: {str(e)}"}), 500

@app.route('/move', methods=['POST'])
def move_route():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        maze = data.get('maze')
        player = tuple(data.get('player'))
        ai = tuple(data.get('ai'))
        key = tuple(data.get('key'))
        goal = tuple(data.get('goal'))
        prev_ai = tuple(data.get('prev_ai', ai))
        player_has_key = data.get('player_has_key', False)
        ai_has_key = data.get('ai_has_key', False)

        if not all([maze, player, ai, key, goal]):
            return jsonify({"error": "Missing required data"}), 400

        # Validate player move
        pr, pc = player
        if not (0 <= pr < len(maze) and 0 <= pc < len(maze[0])):
            return jsonify({"error": f"Invalid player move: Out of bounds {player}"}), 400
        if maze[pr][pc] == 1:
            return jsonify({"error": f"Invalid player move: Wall at {player}"}), 400
        print(f"Player move to {player}, valid")

        # Update key status
        if player == key:
            player_has_key = True
        if ai == key:
            ai_has_key = True

        # AI move
        ai_move = minimax_move(maze, player, ai, key, goal, prev_ai, ai_has_key, player_has_key)
        print(f"AI move from {ai} to {ai_move}, has_key: {ai_has_key}, target: {key if not ai_has_key else goal}")

        # Validate AI move
        ar, ac = ai_move
        if not (0 <= ar < len(maze) and 0 <= ac < len(maze[0]) and maze[ar][ac] != 1):
            print(f"AI move invalid {ai_move}, staying at {ai}")
            ai_move = ai

        return jsonify({
            "maze": maze,
            "player": list(player),
            "ai": list(ai_move),
            "key": list(key),
            "goal": list(goal),
            "prev_ai": list(ai),
            "player_has_key": player_has_key,
            "ai_has_key": ai_has_key
        })
    except Exception as e:
        print(f"Error in /move: {str(e)}")
        return jsonify({"error": f"Failed to process move: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)