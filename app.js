const playersKey = 'players';
const evaluationsKey = 'evaluations';
const evalKeys = [
  'energia',
  'concentracion',
  'control',
  'pase',
  'regate',
  'disparo',
  'vision',
  'velocidad'
];

let compareChart = null;

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

function renderPlayerCards() {
  const container = document.getElementById('players-cards');
  if (!container) return;
  container.innerHTML = '';
  players.forEach(p => {
    const avg = playerAverage(p.id);
    const evalCount = evaluations.filter(e => e.playerId === p.id).length;
    const card = document.createElement('div');
    card.className = 'player-card';
    card.innerHTML = `
      <h3>${p.name}</h3>
      <p>${p.pos1}${p.pos2 ? ' / ' + p.pos2 : ''}</p>
      <p>Evaluaciones: ${evalCount}</p>
      <ul>
        ${evalKeys.map(k => `<li>${k}: ${avg ? avg[k].toFixed(1) : '-'}</li>`).join('')}
      </ul>
    `;
    container.appendChild(card);
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
  activateSection('evaluation-section');
  renderHistory(id);
}

function playerAverage(id) {
  const evals = evaluations.filter(e => e.playerId === id);
  if (evals.length === 0) return null;
  const avg = {};
  evalKeys.forEach(k => {
    avg[k] = evals.reduce((sum, e) => sum + Number(e[k] || 0), 0) / evals.length;
  });
  return avg;
}

function teamAverage() {
  if (evaluations.length === 0) return null;
  const avg = {};
  evalKeys.forEach(k => {
    avg[k] = evaluations.reduce((sum, e) => sum + Number(e[k] || 0), 0) / evaluations.length;
  });
  return avg;
}

function renderHistory(playerId) {
  const container = document.getElementById('history-table');
  container.innerHTML = '';
  const evals = evaluations.filter(e => e.playerId === playerId);
  if (evals.length === 0) {
    container.textContent = 'Sin evaluaciones';
    return;
  }
  const table = document.createElement('table');
  const header = document.createElement('tr');
  ['Fecha', ...evalKeys.map(k => k.charAt(0).toUpperCase()) , ''].forEach(t => {
    const th = document.createElement('th');
    th.textContent = t;
    header.appendChild(th);
  });
  table.appendChild(header);
  evals.forEach(ev => {
    const tr = document.createElement('tr');
    const tdDate = document.createElement('td');
    tdDate.textContent = ev.date;
    tr.appendChild(tdDate);
    evalKeys.forEach(k => {
      const td = document.createElement('td');
      td.textContent = ev[k];
      tr.appendChild(td);
    });
    const btnTd = document.createElement('td');
    const btn = document.createElement('button');
    btn.textContent = 'Comparar';
    btn.onclick = () => renderComparison(ev);
    btnTd.appendChild(btn);
    tr.appendChild(btnTd);
    table.appendChild(tr);
  });
  container.appendChild(table);
}

function renderComparison(entry) {
  const teamAvg = teamAverage();
  const container = document.getElementById('compare-results');
  container.innerHTML = '';
  if (!entry || !teamAvg) {
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

  evalKeys.forEach(k => {
    const tr = document.createElement('tr');
    const tdK = document.createElement('td');
    tdK.textContent = k;
    const tdP = document.createElement('td');
    tdP.textContent = Number(entry[k] || 0).toFixed(2);
    const tdT = document.createElement('td');
    tdT.textContent = teamAvg[k].toFixed(2);
    tr.appendChild(tdK);
    tr.appendChild(tdP);
    tr.appendChild(tdT);
    table.appendChild(tr);
  });
  container.appendChild(table);

  // render chart
  const ctx = document.getElementById('compare-chart').getContext('2d');
  if (compareChart) compareChart.destroy();
  compareChart = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: evalKeys,
      datasets: [
        {
          label: 'Jugador',
          data: evalKeys.map(k => Number(entry[k] || 0)),
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)'
        },
        {
          label: 'Equipo',
          data: evalKeys.map(k => teamAvg[k]),
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderColor: 'rgba(255, 99, 132, 1)'
        }
      ]
    },
    options: {
      scales: {
        r: {
          beginAtZero: true,
          max: 10
        }
      }
    }
  });
}

// export/import helpers
function exportData() {
  const data = { players, evaluations };
  const blob = new Blob([JSON.stringify(data, null, 2)], {
    type: 'application/json'
  });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'entreno.json';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  alert('Datos exportados correctamente');
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
        renderPlayerCards();
        const current = document.getElementById('player-id').value;
        if (current) {
          renderHistory(current);
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
  renderPlayerCards();
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
  renderHistory(playerId);
  renderComparison(entry);
  renderPlayerCards();
  e.target.reset();
});

document.getElementById('export-btn').addEventListener('click', exportData);
document.getElementById('import-file').addEventListener('change', e => {
  const file = e.target.files[0];
  if (file) importData(file);
  e.target.value = '';
});

// navigation helpers
function activateSection(sectionId) {
  document.querySelectorAll('section').forEach(sec => {
    const keep =
      sec.id === sectionId ||
      (sectionId === 'evaluation-section' &&
        ['evaluation-section', 'history-section', 'compare-section'].includes(sec.id)) ||
      (sectionId === 'players-list-section' && sec.id === 'player-form-section');

    if (keep) {
      sec.classList.remove('hidden');
    } else {
      sec.classList.add('hidden');
    }
  });
  document.querySelectorAll('#bottom-nav button').forEach(btn => {
    if (btn.dataset.target === sectionId) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });
  if (sectionId === 'players-cards') renderPlayerCards();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

document.querySelectorAll('#bottom-nav button').forEach(btn => {
  btn.addEventListener('click', () => {
    activateSection(btn.dataset.target);
  });
});

// initial render
renderPlayers();
renderPlayerCards();
activateSection('players-list-section');
