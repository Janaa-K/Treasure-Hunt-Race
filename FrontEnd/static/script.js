const COLORS = {
  0: 'path',
  1: 'wall',
  2: 'start',
  3: 'key',
  4: 'goal',
  5: 'ai-start',
  '-1': 'visited'
};

let maze = [];
let start, key, goal, aiStart;
let player = [0, 0];
let ai = [9, 9];
let prevAi = [9, 9];
let playerHasKey = false;
let aiHasKey = false;
let playerWins = 0, aiWins = 0;
let gameStarted = false;

function renderMaze() {
  const container = document.getElementById('mazeContainer');
  if (!container) {
    console.error('Error: mazeContainer not found in HTML');
    document.getElementById('status').textContent = 'Error: mazeContainer not found';
    return;
  }
  container.innerHTML = '';
  if (!maze || !Array.isArray(maze) || maze.length === 0 || !Array.isArray(maze[0])) {
    console.error('Error: Invalid maze data', maze);
    document.getElementById('status').textContent = 'Error: Invalid maze data';
    return;
  }
  maze.forEach((row, r) => {
    row.forEach((cell, c) => {
      const div = document.createElement('div');
      div.className = `maze-cell ${COLORS[cell] || 'path'}`;
      // Prioritize player and AI over key and goal
      if (player[0] === r && player[1] === c) {
        div.classList.remove('key', 'goal');
        div.classList.add('player');
        if (r === key[0] && c === key[1] && !playerHasKey) {
          div.classList.add('pop');
        }
      } else if (ai[0] === r && ai[1] === c) {
        div.classList.remove('key', 'goal');
        div.classList.add('ai');
        if (r === key[0] && c === key[1] && !aiHasKey) {
          div.classList.add('pop');
        }
      }
      container.appendChild(div);
    });
  });
  const aiTarget = aiHasKey ? goal : key;
  const aiDist = Math.abs(ai[0] - aiTarget[0]) + Math.abs(ai[1] - aiTarget[1]);
  console.log('Maze rendered, Player at:', player, 'AI at:', ai, 'Has key:', aiHasKey, 'Target:', aiTarget, 'Distance:', aiDist);
}

async function generateMaze() {
  stopGame();
  try {
    console.log('Fetching maze from /generate-maze');
    const res = await fetch('/generate-maze');
    if (!res.ok) {
      throw new Error(`HTTP error! Status: ${res.status}`);
    }
    const data = await res.json();
    if (data.error) {
      throw new Error(data.error);
    }
    if (!data.maze || !Array.isArray(data.maze)) {
      throw new Error('Invalid maze data received');
    }
    maze = data.maze;
    start = data.start;
    key = data.key;
    goal = data.goal;
    aiStart = data.ai;
    player = [...start];
    ai = [...aiStart];
    prevAi = [...ai];
    playerHasKey = data.player_has_key;
    aiHasKey = data.ai_has_key;
    document.getElementById('status').textContent = 'Click Play to start the game!';
    updateScores();
    renderMaze();
    console.log('New maze generated, Player start:', player, 'AI start:', ai);
  } catch (error) {
    console.error('Error generating maze:', error);
    document.getElementById('status').textContent = `Error: Failed to load maze - ${error.message}`;
  }
}

function restartGame() {
  stopGame();
  try {
    player = [...start];
    ai = [...aiStart];
    prevAi = [...ai];
    playerHasKey = false;
    aiHasKey = false;
    maze = maze.map((row, r) =>
      row.map((cell, c) => {
        if (r === start[0] && c === start[1]) return 2;
        if (r === key[0] && c === key[1]) return 3;
        if (r === goal[0] && c === goal[1]) return 4;
        if (r === aiStart[0] && c === aiStart[1]) return 5;
        if (cell === -1) return 0;
        return cell;
      })
    );
    document.getElementById('status').textContent = 'Game restarted! Click Play to start.';
    renderMaze();
    console.log('Game restarted, Player at:', player, 'AI at:', ai);
  } catch (error) {
    console.error('Error restarting game:', error);
    document.getElementById('status').textContent = `Error: Failed to restart - ${error.message}`;
  }
}

function updateScores() {
  document.getElementById('playerScore').textContent = `Player Wins: ${playerWins}`;
  document.getElementById('aiScore').textContent = `AI Wins: ${aiWins}`;
}

function checkVictory() {
  if (player[0] === goal[0] && player[1] === goal[1]) {
    if (playerHasKey) {
      document.getElementById('winSound').play();
      document.getElementById('status').innerHTML = '<span class="text-3xl font-bold text-green-400">🏁 Player Wins!</span>';
      playerWins++;
      updateScores();
      stopGame();
      alert('Congratulations! The player reached the treasure first! 🎉');
    } else {
      document.getElementById('status').textContent = '❌ You must collect the key first!';
    }
  } else if (ai[0] === goal[0] && ai[1] === goal[1]) {
    if (aiHasKey) {
      document.getElementById('loseSound').play();
      document.getElementById('status').innerHTML = '<span class="text-3xl font-bold text-red-400">🤖 AI Wins!</span>';
      aiWins++;
      updateScores();
      stopGame();
      alert('Oh no! The AI reached the treasure first! 😔');
    }
  }
}

async function searchPath() {
  const algo = document.getElementById('algoSelect').value;
  let tempMaze = maze.map(row => [...row]);
  try {
    console.log(`Searching path with ${algo}`);
    const startTime = performance.now();
    const res = await fetch('/search-path', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ maze: tempMaze, start, key, goal, algo })
    });
    const data = await res.json();
    if (data.error) {
      throw new Error(data.error);
    }
    const path = data.path;
    const timeTaken = performance.now() - startTime;
    if (path && path.length > 0) {
      const originalPlayer = [...player];
      const originalHasKey = playerHasKey;
      for (let i = 0; i < path.length; i++) {
        const [r, c] = path[i];
        if (!(r === key[0] && c === key[1]) && !(r === goal[0] && c === goal[1])) {
          tempMaze[r][c] = -1;
        }
        player = [r, c];
        if (player[0] === key[0] && player[1] === key[1]) playerHasKey = true;
        maze = tempMaze;
        renderMaze();
        await new Promise(res => setTimeout(res, 100));
      }
      document.getElementById('winSound').play();
      document.getElementById('status').textContent = `${algo.toUpperCase()} found path, length: ${path.length}, time: ${timeTaken.toFixed(2)}ms`;
      // Update performance table
      const tbody = document.getElementById('perfTable').querySelector('tbody');
      const existingRows = tbody.querySelectorAll(`tr[data-algo="${algo}"]`);
      existingRows.forEach(row => row.remove());
      const row = tbody.insertRow();
      row.setAttribute('data-algo', algo);
      row.innerHTML = `<td>${algo.toUpperCase()}</td><td>${path.length}</td><td>${data.nodes_explored}</td><td>${timeTaken.toFixed(2)}</td>`;
      console.log(`${algo.toUpperCase()} path found, length: ${path.length}, nodes: ${data.nodes_explored}, time: ${timeTaken.toFixed(2)}ms`);
      player = originalPlayer;
      playerHasKey = originalHasKey;
      maze = maze.map((row, r) =>
        row.map((cell, c) => {
          if (r === start[0] && c === start[1]) return 2;
          if (r === key[0] && c === key[1]) return 3;
          if (r === goal[0] && c === goal[1]) return 4;
          if (r === aiStart[0] && c === aiStart[1]) return 5;
          if (cell === -1) return 0;
          return cell;
        })
      );
      renderMaze();
    } else {
      document.getElementById('status').textContent = `${algo.toUpperCase()} found no path!`;
      console.log(`${algo.toUpperCase()} found no path, nodes: ${data.nodes_explored}, time: ${timeTaken.toFixed(2)}ms`);
    }
  } catch (error) {
    console.error('Error searching path:', error);
    document.getElementById('status').textContent = `Error: Failed to search path - ${error.message}`;
  }
}

async function makeMove(newPlayerPos) {
  if (!gameStarted) {
    document.getElementById('status').textContent = 'Click Play to start moving!';
    console.log('Move blocked: Game not started');
    return;
  }
  const [nr, nc] = newPlayerPos;
  if (nr < 0 || nr >= maze.length || nc < 0 || nc >= maze[0].length) {
    console.log('Move blocked: Out of bounds', newPlayerPos);
    return;
  }
  if (maze[nr][nc] === 1) {
    console.log('Move blocked: Wall at', newPlayerPos);
    return;
  }
  try {
    const aiTarget = aiHasKey ? goal : key;
    console.log('Player attempting move to:', newPlayerPos, 'AI at:', ai, 'AI target:', aiTarget);
    const res = await fetch('/move', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        maze,
        player: newPlayerPos,
        ai,
        key,
        goal,
        prev_ai: prevAi,
        player_has_key: playerHasKey,
        ai_has_key: aiHasKey
      })
    });
    if (!res.ok) {
      throw new Error(`HTTP error! Status: ${res.status}`);
    }
    const data = await res.json();
    if (data.error) {
      throw new Error(data.error);
    }
    const oldPlayer = [...player];
    player = data.player;
    prevAi = data.prev_ai;
    const newAi = data.ai;
    console.log('Move response:', { player: data.player, ai: newAi, prevAi: data.prev_ai, aiHasKey: data.ai_has_key });
    if (newAi[0] === ai[0] && newAi[1] === ai[1]) {
      console.warn('AI did not move:', { from: ai, to: newAi });
    }
    ai = newAi;
    const wasPlayerAtKey = player[0] === key[0] && player[1] === key[1] && !playerHasKey;
    const wasAiAtKey = ai[0] === key[0] && ai[1] === key[1] && !aiHasKey;
    playerHasKey = data.player_has_key;
    aiHasKey = data.ai_has_key;
    renderMaze();
    if (wasPlayerAtKey || wasAiAtKey) {
      document.getElementById('winSound').play();
    }
    checkVictory();
  } catch (error) {
    console.error('Error making move:', error);
    document.getElementById('status').textContent = `Error: Failed to process move - ${error.message}`;
  }
}

function startGame() {
  if (gameStarted) return;
  gameStarted = true;
  document.getElementById('playBtn').disabled = true;
  document.getElementById('status').textContent = 'Game started! Use WASD to move.';
  console.log('Game started');
}

function stopGame() {
  gameStarted = false;
  document.getElementById('playBtn').disabled = false;
}

document.getElementById('generateBtn').addEventListener('click', generateMaze);
document.getElementById('searchBtn').addEventListener('click', searchPath);
document.getElementById('restartBtn').addEventListener('click', restartGame);
document.getElementById('playBtn').addEventListener('click', startGame);

document.addEventListener('keydown', async (e) => {
  console.log('Key pressed:', e.key);
  if (!gameStarted) {
    console.log('Key ignored: Game not started');
    document.getElementById('status').textContent = 'Click Play to start moving!';
    return;
  }
  const moves = {
    'w': [-1, 0],
    'a': [0, -1],
    's': [1, 0],
    'd': [0, 1]
  };
  if (e.key.toLowerCase() in moves) {
    const [dr, dc] = moves[e.key.toLowerCase()];
    const [r, c] = player;
    const nr = r + dr, nc = c + dc;
    console.log('Calculated move: from', [r, c], 'to', [nr, nc]);
    if (nr >= 0 && nr < 10 && nc >= 0 && nc < 10) {
      await makeMove([nr, nc]);
    } else {
      console.log('Move blocked: Out of bounds', [nr, nc]);
    }
  }
});

window.addEventListener('load', () => {
  console.log('Page loaded, generating maze');
  generateMaze();
});