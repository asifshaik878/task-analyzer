async function postJson(url, data) {
  const resp = await fetch(url, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  });
  if (!resp.ok) {
    const txt = await resp.text().catch(()=>null);
    throw new Error(txt || resp.status);
  }
  return resp.json();
}

function getPriorityClass(score) {
  if (score >= 100) return 'prio-high';
  if (score >= 50) return 'prio-medium';
  return 'prio-low';
}

function displayResults(list) {
  const out = document.getElementById('results');
  out.innerHTML = '';
  if (!Array.isArray(list) || list.length === 0) {
    out.innerHTML = '<div class=\"small\">No tasks to show.</div>';
    return;
  }
  list.forEach(t => {
    const card = document.createElement('div');
    card.className = 'card ' + getPriorityClass(t.score || 0);
    const title = document.createElement('h3');
    title.innerHTML = \\ <small class=\"small\">(score: \)</small>\;
    const meta = document.createElement('div');
    meta.className = 'meta';
    meta.innerHTML = \<div><b>Due:</b> \</div><div><b>Importance:</b> \</div><div><b>Est hrs:</b> \</div>\;
    const why = document.createElement('p');
    why.innerHTML = '<b>Why:</b> ' + (t.explanation || '');
    card.appendChild(title);
    card.appendChild(meta);
    card.appendChild(why);
    out.appendChild(card);
  });
}

function showError(msg) {
  const el = document.getElementById('error');
  el.textContent = msg;
  setTimeout(()=>{ if (el.textContent===msg) el.textContent=''; }, 6000);
}

document.getElementById('analyzeBtn').addEventListener('click', async ()=>{
  const raw = document.getElementById('taskInput').value;
  let tasks;
  try {
    tasks = JSON.parse(raw);
    if (!Array.isArray(tasks)) throw new Error('Paste a JSON array of tasks');
  } catch(e) { showError('Invalid JSON: '+ (e.message||e)); return; }

  // optional simple client-side strategy tweak (demonstration only)
  const strategy = document.getElementById('strategy').value;
  if (strategy === 'deadline') {
    // no change — backend handles urgency
  } else if (strategy === 'fastest') {
    // push small estimated_hours tasks to front by adding a temporary weight field
    tasks = tasks.map(t => ({...t, _client_bonus: (t.estimated_hours && t.estimated_hours < 2) ? 1000 : 0 }));
  } else if (strategy === 'importance') {
    tasks = tasks.map(t => ({...t, importance: (t.importance||5) + 2 })); // small client bump
  }

  try {
    const data = await postJson('/api/tasks/analyze/', tasks);
    displayResults(data);
  } catch (err) {
    showError('Server error: ' + err.message);
  }
});

document.getElementById('suggestBtn').addEventListener('click', async ()=>{
  const raw = document.getElementById('taskInput').value;
  let tasks;
  try {
    tasks = JSON.parse(raw);
    if (!Array.isArray(tasks)) throw new Error('Paste a JSON array of tasks');
  } catch(e) { showError('Invalid JSON: '+ (e.message||e)); return; }

  try {
    const data = await postJson('/api/tasks/suggest/', tasks);
    // data.top3 expected
    displayResults(data.top3.map(x => x.task));
  } catch (err) {
    showError('Server error: ' + err.message);
  }
});

// load sample on click
document.getElementById('sampleBtn').addEventListener('click', ()=>{
  const sample = [
    {"title":"Fix login bug","due_date":"2025-12-01","estimated_hours":3,"importance":8,"dependencies":[]},
    {"title":"Write documentation","due_date":null,"estimated_hours":1,"importance":6,"dependencies":[]},
    {"title":"Database migration","due_date":"2025-11-25","estimated_hours":5,"importance":9,"dependencies":["Fix login bug"]}
  ];
  document.getElementById('taskInput').value = JSON.stringify(sample, null, 2);
});
