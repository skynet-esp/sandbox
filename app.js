const playersKey = 'players';
const evaluationsKey = 'evaluations';

let players = JSON.parse(localStorage.getItem(playersKey) || '[]');
let evaluations = JSON.parse(localStorage.getItem(evaluationsKey) || '[]');

function savePlayers() {
  localStorage.setItem(playersKey, JSON.stringify(players));
}

function saveEvaluations() {
  localStorage.setItem(evaluationsKey, JSON.stringify(evaluations));
}

function renderPlayers() {
  const list = document.getElementById('players-list');
  list.innerHTML = '';
  players.forEach(player => {
    const li = document.createElement('li');
    const btn = document.createElement('button');
    btn.textContent = player.name;
    btn.onclick = () => selectPlayer(player.id);
    li.appendChild(btn);
    list.appendChild(li);
  });
}

function selectPlayer(id) {
  const player = players.find(p => p.id === id);
  if (!player) return;
  document.getElementById('evaluation-player-name').textContent = player.name;
  document.getElementById('player-id').value = player.id;
  document.getElementById('player-name').value = player.name;
  document.getElementById('player-pos1').value = player.pos1;
  document.getElementById('player-pos2').value = player.pos2 || '';
  document.getElementById('evaluation-section').classList.remove('hidden');
  document.getElementById('compare-section').classList.remove('hidden');
}

function playerAverage(id) {
  const evals = evaluations.filter(e => e.playerId === id);
  if (evals.length === 0) return null;
  const keys = ['energia','concentracion','control','pase','regate','disparo','vision','velocidad'];
  const avg = {};
  keys.forEach(k => {
    avg[k] = evals.reduce((sum, e) => sum + Number(e[k] || 0), 0) / evals.length;
  });
  return avg;
}

function teamAverage() {
  if (evaluations.length === 0) return null;
  const keys = ['energia','concentracion','control','pase','regate','disparo','vision','velocidad'];
  const avg = {};
  keys.forEach(k => {
    avg[k] = evaluations.reduce((sum, e) => sum + Number(e[k] || 0), 0) / evaluations.length;
  });
  return avg;
}

function renderComparison(playerId) {
  const playerAvg = playerAverage(playerId);
  const teamAvg = teamAverage();
  const container = document.getElementById('compare-results');
  container.innerHTML = '';
  if (!playerAvg || !teamAvg) {
    container.textContent = 'Sin datos para comparar.';
    return;
  }
  const table = document.createElement('table');
  const header = document.createElement('tr');
  ['Característica','Jugador','Equipo'].forEach(t => {
    const th = document.createElement('th');
    th.textContent = t;
    header.appendChild(th);
  });
  table.appendChild(header);

  Object.keys(playerAvg).forEach(k => {
    const tr = document.createElement('tr');
    const tdK = document.createElement('td');
    tdK.textContent = k;
    const tdP = document.createElement('td');
    tdP.textContent = playerAvg[k].toFixed(2);
    const tdT = document.createElement('td');
    tdT.textContent = teamAvg[k].toFixed(2);
    tr.appendChild(tdK);
    tr.appendChild(tdP);
    tr.appendChild(tdT);
    table.appendChild(tr);
  });
  container.appendChild(table);
}

// export/import helpers
function exportData() {
  const data = { players, evaluations };
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'entreno.json';
  a.click();
  URL.revokeObjectURL(url);
}

function importData(file) {
  const reader = new FileReader();
  reader.onload = e => {
    try {
      const data = JSON.parse(e.target.result);
      if (Array.isArray(data.players) && Array.isArray(data.evaluations)) {
        players = data.players;
        evaluations = data.evaluations;
        savePlayers();
        saveEvaluations();
        renderPlayers();
        const current = document.getElementById('player-id').value;
        if (current) {
          renderComparison(current);
        }
      } else {
        alert('Archivo no válido');
      }
    } catch (err) {
      alert('Archivo no válido');
    }
  };
  reader.readAsText(file);
}

// form handlers

document.getElementById('player-form').addEventListener('submit', e => {
  e.preventDefault();
  const id = document.getElementById('player-id').value;
  const name = document.getElementById('player-name').value;
  const pos1 = document.getElementById('player-pos1').value;
  const pos2 = document.getElementById('player-pos2').value;
  if (id) {
    const p = players.find(pl => pl.id === id);
    if (p) {
      p.name = name;
      p.pos1 = pos1;
      p.pos2 = pos2;
    }
  } else {
    players.push({ id: Date.now().toString(), name, pos1, pos2 });
  }
  savePlayers();
  renderPlayers();
  e.target.reset();
});

document.getElementById('evaluation-form').addEventListener('submit', e => {
  e.preventDefault();
  const playerId = document.getElementById('player-id').value;
  const entry = {
    playerId,
    date: document.getElementById('eval-date').value,
    energia: document.getElementById('eval-energia').value,
    concentracion: document.getElementById('eval-concentracion').value,
    control: document.getElementById('eval-control').value,
    pase: document.getElementById('eval-pase').value,
    regate: document.getElementById('eval-regate').value,
    disparo: document.getElementById('eval-disparo').value,
    vision: document.getElementById('eval-vision').value,
    velocidad: document.getElementById('eval-velocidad').value
  };
  evaluations.push(entry);
  saveEvaluations();
  renderComparison(playerId);
  e.target.reset();
});

document.getElementById('export-btn').addEventListener('click', exportData);
document.getElementById('import-file').addEventListener('change', e => {
  const file = e.target.files[0];
  if (file) importData(file);
  e.target.value = '';
});

// initial render
renderPlayers();
