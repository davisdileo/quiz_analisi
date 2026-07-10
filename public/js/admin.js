const app = document.getElementById("app");

let adminPassword = sessionStorage.getItem("adminPassword") || "";
let latestState = null;
let pollTimer = null;

function api(path, opts = {}) {
  opts.headers = Object.assign({}, opts.headers, {
    "Content-Type": "application/json",
    "x-admin-key": adminPassword,
  });
  return fetch(path, opts);
}

function renderMath() {
  if (window.renderMathInElement) {
    renderMathInElement(app, {
      delimiters: [
        { left: "\\[", right: "\\]", display: true },
        { left: "\\(", right: "\\)", display: false },
      ],
      throwOnError: false,
    });
  }
}

function renderLogin(errorMsg) {
  app.innerHTML = `
    <div class="card" style="max-width:420px;margin:0 auto;">
      <h2>Accesso docente</h2>
      <label for="pwd">Password amministratore</label>
      <input type="password" id="pwd" />
      ${errorMsg ? `<p class="error">${errorMsg}</p>` : ""}
      <button id="loginBtn">Accedi</button>
    </div>
  `;
  document.getElementById("loginBtn").onclick = doLogin;
  document.getElementById("pwd").addEventListener("keydown", (e) => {
    if (e.key === "Enter") doLogin();
  });
}

async function doLogin() {
  const pwd = document.getElementById("pwd").value;
  const res = await fetch("/api/admin/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ password: pwd }),
  });
  const data = await res.json();
  if (!res.ok) return renderLogin(data.error);
  adminPassword = pwd;
  sessionStorage.setItem("adminPassword", pwd);
  renderDashboard();
  startPolling();
}

function statusLabel(s) {
  return {
    not_registered: "Non connesso",
    waiting: "In attesa",
    in_progress: "In corso",
    completed: "Completato",
  }[s] || s;
}

function renderDashboard() {
  app.innerHTML = `
    <div class="card">
      <h2>Genera codici studenti</h2>
      <p class="muted">Genera codici univoci da distribuire agli studenti (via proiettore, lista cartacea, ecc.).</p>
      <label for="count">Numero di codici da generare</label>
      <input type="number" id="count" value="30" min="1" max="300" />
      <button id="genBtn">Genera codici</button>
      <button class="secondary" id="downloadBtn">Scarica elenco codici (.txt)</button>
      <div id="codesBox"></div>
    </div>

    <div class="card">
      <h2>Controllo quiz</h2>
      <div class="top-actions">
        <button id="startBtn">Avvia quiz</button>
        <button class="secondary" id="stopBtn">Termina quiz</button>
        <button class="danger" id="resetBtn">Reset completo</button>
      </div>
      <p class="muted" id="quizStatusMsg"></p>
    </div>

    <div class="card">
      <h2>Andamento in tempo reale</h2>
      <div class="stats-row" id="statsRow"></div>
      <table>
        <thead>
          <tr><th>Codice</th><th>Nome</th><th>Stato</th><th>Progresso</th><th>Voto</th><th></th></tr>
        </thead>
        <tbody id="studentsBody"></tbody>
      </table>
    </div>
  `;

  document.getElementById("genBtn").onclick = generateCodes;
  document.getElementById("downloadBtn").onclick = downloadCodes;
  document.getElementById("startBtn").onclick = () => api("/api/admin/start-quiz", { method: "POST" }).then(refreshState);
  document.getElementById("stopBtn").onclick = () => {
    if (confirm("Terminare il quiz per tutti gli studenti?")) {
      api("/api/admin/stop-quiz", { method: "POST" }).then(refreshState);
    }
  };
  document.getElementById("resetBtn").onclick = () => {
    if (confirm("Questo cancellerà tutti i codici, le risposte e i punteggi. Continuare?")) {
      api("/api/admin/reset", { method: "POST" }).then(refreshState);
    }
  };

  refreshState();
}

async function generateCodes() {
  const count = parseInt(document.getElementById("count").value, 10) || 30;
  const res = await api("/api/admin/generate-codes", {
    method: "POST",
    body: JSON.stringify({ count }),
  });
  const data = await res.json();
  document.getElementById("codesBox").innerHTML = `
    <label>Nuovi codici generati (${data.created.length}):</label>
    <div class="codes-box">${data.created.join("<br/>")}</div>
  `;
  refreshState();
}

function downloadCodes() {
  if (!latestState) return;
  const lines = latestState.students.map((s) => s.code).join("\n");
  const blob = new Blob([lines], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "codici-studenti.txt";
  a.click();
  URL.revokeObjectURL(url);
}

function renderState(data) {
  latestState = data;

  const total = data.students.length;
  const waiting = data.students.filter((s) => s.status === "waiting" || s.status === "not_registered").length;
  const inProgress = data.students.filter((s) => s.status === "in_progress").length;
  const completed = data.students.filter((s) => s.status === "completed").length;
  const avgVoto = (() => {
    const done = data.students.filter((s) => s.voto !== null && s.voto !== undefined);
    if (!done.length) return "-";
    return (done.reduce((a, s) => a + s.voto, 0) / done.length).toFixed(1);
  })();

  document.getElementById("statsRow").innerHTML = `
    <div class="stat"><div class="num">${total}</div><div class="lab">Codici totali</div></div>
    <div class="stat"><div class="num">${waiting}</div><div class="lab">In attesa</div></div>
    <div class="stat"><div class="num">${inProgress}</div><div class="lab">In corso</div></div>
    <div class="stat"><div class="num">${completed}</div><div class="lab">Completati</div></div>
    <div class="stat"><div class="num">${avgVoto}</div><div class="lab">Voto medio</div></div>
  `;

  const statusMsg = document.getElementById("quizStatusMsg");
  if (statusMsg) {
    statusMsg.textContent = data.quizStopped
      ? "Quiz terminato."
      : data.quizStarted
      ? "Quiz avviato — gli studenti stanno rispondendo."
      : "Quiz non ancora avviato.";
  }

  const tbody = document.getElementById("studentsBody");
  if (tbody) {
    tbody.innerHTML = data.students
      .map(
        (s) => `
      <tr>
        <td>${s.code}</td>
        <td>${s.name || "<span class='muted'>—</span>"}</td>
        <td><span class="badge ${s.status}">${statusLabel(s.status)}</span></td>
        <td>${s.answered}/${s.total || data.totalQuestions}</td>
        <td>${s.voto !== null && s.voto !== undefined ? (s.lode ? "30 e lode" : s.voto + "/30") : "—"}</td>
        <td><button class="secondary" style="margin:0;padding:6px 12px;font-size:0.82rem;" data-code="${s.code}">Vedi quiz</button></td>
      </tr>
    `
      )
      .join("");
    tbody.querySelectorAll("button[data-code]").forEach((btn) => {
      btn.onclick = () => renderReview(btn.dataset.code);
    });
  }
}

function optionLabel(q, i) {
  const isCorrectOpt = i === q.correctIndex;
  const isStudentOpt = i === q.studentIndex;
  let cls = "option";
  let tag = "";
  if (isCorrectOpt) {
    cls += " correct-opt";
    tag = " &nbsp;<span class='badge completed'>corretta</span>";
  }
  if (isStudentOpt && !isCorrectOpt) {
    cls += " wrong-opt";
    tag = " &nbsp;<span class='badge not_registered' style='background:#fde2e1;color:#c0392b;'>risposta data</span>";
  }
  if (isStudentOpt && isCorrectOpt) {
    tag = " &nbsp;<span class='badge completed'>risposta corretta</span>";
  }
  return `<div class="${cls}"><span>${q.options[i]}</span>${tag}</div>`;
}

async function renderReview(code) {
  clearInterval(pollTimer);
  app.innerHTML = `<div class="card"><p class="muted">Caricamento...</p></div>`;
  const res = await api("/api/admin/student-review?code=" + encodeURIComponent(code));
  if (res.status === 401) return renderLogin();
  const data = await res.json();
  if (!res.ok) {
    app.innerHTML = `<div class="card"><p class="error">${data.error || "Errore."}</p></div>`;
    return;
  }

  const scoreLine =
    data.voto !== null && data.voto !== undefined
      ? `${data.lode ? "30 e lode" : data.voto + "/30"} &middot; ${data.correctCount}/${data.total} corrette`
      : "Quiz non ancora completato";

  const questionsHtml = data.questions
    .map(
      (q, i) => `
    <div class="card" style="margin-top:16px;">
      <div class="q-topic">${q.topic}</div>
      <div class="q-counter" style="text-align:left;margin-bottom:6px;">Domanda ${i + 1} di ${data.questions.length}${q.answered ? "" : " &middot; <strong>non risposto</strong>"}</div>
      <div class="q-text">${q.text}</div>
      ${q.image ? `<img class="q-image" src="/images/${q.image}" alt="grafico" />` : ""}
      ${q.options.map((_, oi) => optionLabel(q, oi)).join("")}
    </div>
  `
    )
    .join("");

  app.innerHTML = `
    <div class="card">
      <button class="secondary" id="backBtn">&larr; Torna alla dashboard</button>
      <h2 style="margin-top:16px;">${data.name || "Studente"} <span class="muted">(${data.code})</span></h2>
      <p class="muted">${scoreLine}</p>
    </div>
    ${questionsHtml}
  `;
  document.getElementById("backBtn").onclick = () => {
    renderDashboard();
    startPolling();
  };
  renderMath();
}

async function refreshState() {
  const res = await api("/api/admin/state");
  if (res.status === 401) return renderLogin();
  const data = await res.json();
  renderState(data);
}

function startPolling() {
  clearInterval(pollTimer);
  pollTimer = setInterval(() => {
    if (document.getElementById("studentsBody")) refreshState();
  }, 2000);
}

if (adminPassword) {
  renderDashboard();
  startPolling();
} else {
  renderLogin();
}
