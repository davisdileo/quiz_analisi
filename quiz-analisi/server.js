// Quiz Analisi Matematica I — server senza dipendenze esterne (solo Node core).
// Avvio: node server.js  (oppure: npm start)

const http = require("http");
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const url = require("url");

const PORT = process.env.PORT || 3000;
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || "analisi2026";

const PUBLIC_DIR = path.join(__dirname, "public");
const DATA_DIR = path.join(__dirname, "data");
const STATE_FILE = path.join(DATA_DIR, "state.json");
const QUESTIONS_FILE = path.join(DATA_DIR, "questions.json");

if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });

const QUESTIONS = JSON.parse(fs.readFileSync(QUESTIONS_FILE, "utf-8"));
const TOTAL_QUESTIONS = QUESTIONS.length;

const PUBLIC_QUESTIONS = QUESTIONS.map((q) => ({
  id: q.id,
  topic: q.topic,
  text: q.text,
  options: q.options,
  image: q.image || null,
}));

// ---------- State ----------
let state = {
  quizStarted: false,
  quizStartedAt: null,
  quizStopped: false,
  students: {}, // code -> {code,name,status,currentQuestion,answers,correctCount,voto,lode,startedAt,completedAt}
};

function loadState() {
  if (fs.existsSync(STATE_FILE)) {
    try {
      const raw = JSON.parse(fs.readFileSync(STATE_FILE, "utf-8"));
      state = Object.assign(state, raw);
    } catch (e) {
      console.error("Errore nel caricamento dello stato:", e);
    }
  }
}
loadState();

function saveState() {
  // Scrittura sincrona immediata: con poche decine/centinaia di studenti è
  // sufficientemente veloce ed evita di perdere dati in caso di riavvio del processo.
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

const CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
function generateCode() {
  let code = "";
  const bytes = crypto.randomBytes(6);
  for (let i = 0; i < 6; i++) {
    code += CODE_ALPHABET[bytes[i] % CODE_ALPHABET.length];
  }
  return code;
}

function computeVoto(correctCount) {
  const raw = (correctCount / TOTAL_QUESTIONS) * 30;
  const voto = Math.min(Math.round(raw), 30);
  const lode = correctCount === TOTAL_QUESTIONS;
  return { voto, lode };
}

function adminSummary() {
  return {
    quizStarted: state.quizStarted,
    quizStartedAt: state.quizStartedAt,
    quizStopped: state.quizStopped,
    totalQuestions: TOTAL_QUESTIONS,
    students: Object.values(state.students)
      .map((s) => ({
        code: s.code,
        name: s.name,
        status: s.status,
        currentQuestion: s.currentQuestion,
        answered: Object.keys(s.answers || {}).length,
        correctCount: s.correctCount,
        voto: s.voto,
        lode: s.lode,
        startedAt: s.startedAt,
        completedAt: s.completedAt,
      }))
      .sort((a, b) => (a.code > b.code ? 1 : -1)),
  };
}

// ---------- HTTP helpers ----------
function sendJSON(res, statusCode, obj) {
  const body = JSON.stringify(obj);
  res.writeHead(statusCode, {
    "Content-Type": "application/json; charset=utf-8",
    "Content-Length": Buffer.byteLength(body),
  });
  res.end(body);
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let chunks = [];
    req.on("data", (c) => chunks.push(c));
    req.on("end", () => {
      if (chunks.length === 0) return resolve({});
      try {
        resolve(JSON.parse(Buffer.concat(chunks).toString("utf-8")));
      } catch (e) {
        resolve({});
      }
    });
    req.on("error", reject);
  });
}

function isAdmin(req) {
  return req.headers["x-admin-key"] === ADMIN_PASSWORD;
}

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".svg": "image/svg+xml",
  ".json": "application/json; charset=utf-8",
};

function serveStatic(req, res, pathname) {
  let filePath = pathname === "/" ? "/index.html" : pathname;
  filePath = path.normalize(filePath).replace(/^(\.\.[\/\\])+/, "");
  const fullPath = path.join(PUBLIC_DIR, filePath);
  if (!fullPath.startsWith(PUBLIC_DIR)) {
    res.writeHead(403);
    return res.end("Forbidden");
  }
  fs.readFile(fullPath, (err, data) => {
    if (err) {
      res.writeHead(404, { "Content-Type": "text/plain" });
      return res.end("Non trovato");
    }
    const ext = path.extname(fullPath);
    res.writeHead(200, { "Content-Type": MIME[ext] || "application/octet-stream" });
    res.end(data);
  });
}

// ---------- Server ----------
const server = http.createServer(async (req, res) => {
  const parsed = url.parse(req.url, true);
  const pathname = parsed.pathname;

  try {
    // ----- Admin API -----
    if (pathname === "/api/admin/login" && req.method === "POST") {
      const body = await readBody(req);
      if (body.password !== ADMIN_PASSWORD) return sendJSON(res, 401, { error: "Password errata." });
      return sendJSON(res, 200, { ok: true });
    }

    if (pathname === "/api/admin/state" && req.method === "GET") {
      if (!isAdmin(req)) return sendJSON(res, 401, { error: "Password amministratore non valida." });
      return sendJSON(res, 200, adminSummary());
    }

    if (pathname === "/api/admin/generate-codes" && req.method === "POST") {
      if (!isAdmin(req)) return sendJSON(res, 401, { error: "Password amministratore non valida." });
      const body = await readBody(req);
      const created = [];
      const count = Math.max(1, Math.min(300, parseInt(body.count, 10) || 0));
      for (let i = 0; i < count; i++) {
        let code = generateCode();
        while (state.students[code]) code = generateCode();
        state.students[code] = {
          code,
          name: null,
          status: "not_registered",
          currentQuestion: 0,
          answers: {},
          correctCount: null,
          voto: null,
          lode: false,
          startedAt: null,
          completedAt: null,
        };
        created.push(code);
      }
      saveState();
      return sendJSON(res, 200, { created, all: Object.keys(state.students) });
    }

    if (pathname === "/api/admin/start-quiz" && req.method === "POST") {
      if (!isAdmin(req)) return sendJSON(res, 401, { error: "Password amministratore non valida." });
      state.quizStarted = true;
      state.quizStopped = false;
      state.quizStartedAt = new Date().toISOString();
      saveState();
      return sendJSON(res, 200, { ok: true });
    }

    if (pathname === "/api/admin/stop-quiz" && req.method === "POST") {
      if (!isAdmin(req)) return sendJSON(res, 401, { error: "Password amministratore non valida." });
      state.quizStopped = true;
      saveState();
      return sendJSON(res, 200, { ok: true });
    }

    if (pathname === "/api/admin/reset" && req.method === "POST") {
      if (!isAdmin(req)) return sendJSON(res, 401, { error: "Password amministratore non valida." });
      state = { quizStarted: false, quizStartedAt: null, quizStopped: false, students: {} };
      saveState();
      return sendJSON(res, 200, { ok: true });
    }

    // ----- Student API -----
    if (pathname === "/api/student/login" && req.method === "POST") {
      const body = await readBody(req);
      const c = (body.code || "").trim().toUpperCase();
      const student = state.students[c];
      if (!student) return sendJSON(res, 404, { error: "Codice non valido. Controlla e riprova." });
      if (!student.name && body.name && body.name.trim()) student.name = body.name.trim();
      if (student.status === "not_registered") student.status = "waiting";
      saveState();
      return sendJSON(res, 200, {
        code: student.code,
        name: student.name,
        status: student.status,
        quizStarted: state.quizStarted,
        quizStopped: state.quizStopped,
        currentQuestion: student.currentQuestion,
        totalQuestions: TOTAL_QUESTIONS,
        voto: student.voto,
        lode: student.lode,
        correctCount: student.correctCount,
      });
    }

    if (pathname === "/api/student/status" && req.method === "GET") {
      const c = (parsed.query.code || "").toString().trim().toUpperCase();
      const student = state.students[c];
      if (!student) return sendJSON(res, 404, { error: "Codice non valido." });
      return sendJSON(res, 200, {
        status: student.status,
        quizStarted: state.quizStarted,
        quizStopped: state.quizStopped,
        voto: student.voto,
        lode: student.lode,
        correctCount: student.correctCount,
      });
    }

    if (pathname === "/api/questions" && req.method === "GET") {
      const c = (parsed.query.code || "").toString().trim().toUpperCase();
      const student = state.students[c];
      if (!student) return sendJSON(res, 404, { error: "Codice non valido." });
      if (!state.quizStarted) return sendJSON(res, 403, { error: "Il quiz non è ancora iniziato." });
      return sendJSON(res, 200, { questions: PUBLIC_QUESTIONS, answers: student.answers || {} });
    }

    if (pathname === "/api/student/answer" && req.method === "POST") {
      const body = await readBody(req);
      const c = (body.code || "").trim().toUpperCase();
      const student = state.students[c];
      if (!student) return sendJSON(res, 404, { error: "Codice non valido." });
      if (!state.quizStarted || state.quizStopped) return sendJSON(res, 403, { error: "Il quiz non è attivo." });
      if (student.status === "completed") return sendJSON(res, 403, { error: "Hai già completato il quiz." });
      if (student.status === "waiting") {
        student.status = "in_progress";
        student.startedAt = new Date().toISOString();
      }
      student.answers[body.questionId] = body.optionIndex;
      student.currentQuestion = Object.keys(student.answers).length;
      saveState();
      return sendJSON(res, 200, { ok: true });
    }

    if (pathname === "/api/student/submit" && req.method === "POST") {
      const body = await readBody(req);
      const c = (body.code || "").trim().toUpperCase();
      const student = state.students[c];
      if (!student) return sendJSON(res, 404, { error: "Codice non valido." });
      if (student.status === "completed") {
        return sendJSON(res, 200, {
          correctCount: student.correctCount,
          total: TOTAL_QUESTIONS,
          voto: student.voto,
          lode: student.lode,
        });
      }
      let correctCount = 0;
      QUESTIONS.forEach((q) => {
        const given = student.answers[q.id];
        if (given !== undefined && given === q.correct) correctCount++;
      });
      const { voto, lode } = computeVoto(correctCount);
      student.correctCount = correctCount;
      student.voto = voto;
      student.lode = lode;
      student.status = "completed";
      student.completedAt = new Date().toISOString();
      saveState();
      return sendJSON(res, 200, { correctCount, total: TOTAL_QUESTIONS, voto, lode });
    }

    // ----- Static files -----
    if (req.method === "GET") {
      return serveStatic(req, res, pathname);
    }

    sendJSON(res, 404, { error: "Non trovato." });
  } catch (e) {
    console.error(e);
    sendJSON(res, 500, { error: "Errore interno del server." });
  }
});

server.listen(PORT, () => {
  console.log(`Quiz Analisi Matematica in ascolto sulla porta ${PORT}`);
  console.log(`Password admin: ${ADMIN_PASSWORD}`);
});
