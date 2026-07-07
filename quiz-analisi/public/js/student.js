const app = document.getElementById("app");

let session = JSON.parse(localStorage.getItem("quizSession") || "null");
let questions = [];
let answers = {};
let currentIndex = 0;
let waitingPollTimer = null;

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

function saveSession() {
  localStorage.setItem("quizSession", JSON.stringify(session));
}

function renderLogin(errorMsg) {
  app.innerHTML = `
    <div class="card">
      <h2>Accedi al quiz</h2>
      <p class="muted">Inserisci il codice che ti è stato assegnato dal docente.</p>
      <label for="code">Codice univoco</label>
      <input type="text" id="code" placeholder="Es. AB12CD" autocomplete="off" style="text-transform:uppercase" />
      <label for="name">Nome e Cognome</label>
      <input type="text" id="name" placeholder="Es. Mario Rossi" autocomplete="off" />
      ${errorMsg ? `<p class="error">${errorMsg}</p>` : ""}
      <button id="loginBtn">Entra</button>
    </div>
  `;
  document.getElementById("loginBtn").onclick = doLogin;
  document.getElementById("code").addEventListener("keydown", (e) => {
    if (e.key === "Enter") doLogin();
  });
  document.getElementById("name").addEventListener("keydown", (e) => {
    if (e.key === "Enter") doLogin();
  });
}

async function doLogin() {
  const code = document.getElementById("code").value.trim().toUpperCase();
  const name = document.getElementById("name").value.trim();
  if (!code) return renderLogin("Inserisci il codice.");
  try {
    const res = await fetch("/api/student/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code, name }),
    });
    const data = await res.json();
    if (!res.ok) return renderLogin(data.error || "Errore.");
    session = data;
    saveSession();
    route();
  } catch (e) {
    renderLogin("Errore di connessione al server.");
  }
}

function renderWaiting() {
  app.innerHTML = `
    <div class="card waiting-box">
      <div class="spinner"></div>
      <h2>Ciao ${session.name || ""}!</h2>
      <p class="muted">Il tuo codice è <strong>${session.code}</strong>.<br/>
      In attesa che il docente avvii il quiz...</p>
    </div>
  `;
}

function renderStopped() {
  app.innerHTML = `
    <div class="card waiting-box">
      <h2>Il quiz è stato terminato dal docente</h2>
      <p class="muted">Non è più possibile inviare risposte.</p>
    </div>
  `;
}

async function loadQuestions() {
  const res = await fetch("/api/questions?code=" + encodeURIComponent(session.code));
  const data = await res.json();
  if (!res.ok) throw new Error(data.error);
  questions = data.questions;
  answers = data.answers || {};
}

function renderQuiz() {
  const q = questions[currentIndex];
  const answeredCount = Object.keys(answers).length;
  const pct = Math.round((answeredCount / questions.length) * 100);

  const navButtons = questions
    .map((qq, i) => {
      const cls = [
        i === currentIndex ? "current" : "",
        answers[qq.id] !== undefined ? "answered" : "",
      ]
        .join(" ")
        .trim();
      return `<button data-idx="${i}" class="navnum ${cls}">${i + 1}</button>`;
    })
    .join("");

  app.innerHTML = `
    <div class="card">
      <div class="q-counter">Domanda ${currentIndex + 1} di ${questions.length} &middot; Risposte date: ${answeredCount}/${questions.length}</div>
      <div class="progress-bar"><div style="width:${pct}%"></div></div>
      <div class="q-topic">${q.topic}</div>
      <div class="q-text">${q.text}</div>
      ${q.image ? `<img class="q-image" src="/images/${q.image}" alt="grafico" />` : ""}
      <div id="options"></div>
      <div class="nav-row">
        <button class="secondary" id="prevBtn" ${currentIndex === 0 ? "disabled" : ""}>&larr; Precedente</button>
        ${
          currentIndex === questions.length - 1
            ? `<button id="submitBtn">Consegna quiz</button>`
            : `<button id="nextBtn">Successiva &rarr;</button>`
        }
      </div>
      <div class="grid-nums">${navButtons}</div>
    </div>
  `;

  const optionsDiv = document.getElementById("options");
  q.options.forEach((opt, i) => {
    const selected = answers[q.id] === i;
    const div = document.createElement("div");
    div.className = "option" + (selected ? " selected" : "");
    div.innerHTML = `<input type="radio" name="opt" ${selected ? "checked" : ""} /> <span>${opt}</span>`;
    div.onclick = () => selectOption(q.id, i);
    optionsDiv.appendChild(div);
  });

  document.getElementById("prevBtn").onclick = () => {
    currentIndex = Math.max(0, currentIndex - 1);
    renderQuiz();
  };
  const nextBtn = document.getElementById("nextBtn");
  if (nextBtn) nextBtn.onclick = () => {
    currentIndex = Math.min(questions.length - 1, currentIndex + 1);
    renderQuiz();
  };
  const submitBtn = document.getElementById("submitBtn");
  if (submitBtn) submitBtn.onclick = confirmSubmit;

  document.querySelectorAll(".navnum").forEach((btn) => {
    btn.onclick = () => {
      currentIndex = parseInt(btn.dataset.idx, 10);
      renderQuiz();
    };
  });

  renderMath();
}

async function selectOption(questionId, optionIndex) {
  answers[questionId] = optionIndex;
  renderQuiz();
  try {
    await fetch("/api/student/answer", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code: session.code, questionId, optionIndex }),
    });
  } catch (e) {
    /* ignore transient errors, answer kept locally */
  }
}

function confirmSubmit() {
  const unanswered = questions.length - Object.keys(answers).length;
  const msg =
    unanswered > 0
      ? `Hai ${unanswered} domande senza risposta. Vuoi consegnare comunque il quiz?`
      : "Confermi di voler consegnare il quiz? Non potrai più modificare le risposte.";
  if (confirm(msg)) submitQuiz();
}

async function submitQuiz() {
  const res = await fetch("/api/student/submit", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code: session.code }),
  });
  const data = await res.json();
  session.status = "completed";
  session.voto = data.voto;
  session.lode = data.lode;
  session.correctCount = data.correctCount;
  saveSession();
  renderScore(data);
}

function renderScore(data) {
  app.innerHTML = `
    <div class="card score-box">
      <h2>Quiz completato!</h2>
      <p class="muted">Risposte corrette: ${data.correctCount} su ${data.total}</p>
      <div class="score-voto">${data.lode ? "30 e lode" : data.voto + "/30"}</div>
      <p class="score-detail">Il docente ha ricevuto il tuo risultato.</p>
    </div>
  `;
}

async function pollStatus() {
  if (!session || !session.code) return;
  if (session.status === "completed") return clearInterval(waitingPollTimer);
  try {
    const res = await fetch("/api/student/status?code=" + encodeURIComponent(session.code));
    if (res.status === 404) {
      // il codice non esiste più (probabile reset da parte del docente)
      localStorage.removeItem("quizSession");
      session = null;
      clearInterval(waitingPollTimer);
      return route();
    }
    const data = await res.json();
    const startedNow = !session.quizStarted && data.quizStarted;
    const stoppedNow = !session.quizStopped && data.quizStopped;
    session.quizStarted = data.quizStarted;
    session.quizStopped = data.quizStopped;
    if (data.status === "completed" && session.status !== "completed") {
      session.status = "completed";
      session.voto = data.voto;
      session.lode = data.lode;
      session.correctCount = data.correctCount;
    }
    saveSession();
    if (startedNow || stoppedNow || session.status === "completed") {
      clearInterval(waitingPollTimer);
      route();
    }
  } catch (e) {
    /* ignora errori temporanei di rete */
  }
}

function startWaitingPoll() {
  clearInterval(waitingPollTimer);
  waitingPollTimer = setInterval(pollStatus, 2000);
}

async function route() {
  if (!session || !session.code) return renderLogin();

  if (session.status === "completed" || (session.voto !== null && session.voto !== undefined)) {
    clearInterval(waitingPollTimer);
    return renderScore({
      correctCount: session.correctCount,
      total: session.totalQuestions || 50,
      voto: session.voto,
      lode: session.lode,
    });
  }

  if (session.quizStopped) {
    clearInterval(waitingPollTimer);
    return renderStopped();
  }

  if (!session.quizStarted) {
    renderWaiting();
    startWaitingPoll();
    return;
  }

  try {
    await loadQuestions();
    currentIndex = Object.keys(answers).length < questions.length ? Object.keys(answers).length : questions.length - 1;
    if (currentIndex < 0) currentIndex = 0;
    renderQuiz();
  } catch (e) {
    renderWaiting();
    startWaitingPoll();
  }
}

route();
