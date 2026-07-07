# Quiz di Analisi Matematica I

Web app per l'esercitazione: gli studenti accedono con un codice univoco,
il docente avvia il quiz (50 domande a risposta multipla) e ne segue
l'avanzamento in tempo reale; al termine ogni studente vede il proprio
punteggio e il voto in trentesimi.

Nessuna dipendenza esterna: è un unico server Node.js (modulo `http` nativo),
quindi non serve `npm install`.

## Avvio rapido (in locale)

```
node server.js
```

Il server parte sulla porta 3000 (o quella indicata da `PORT`).

- Pagina studenti: `http://localhost:3000/`
- Pannello docente: `http://localhost:3000/admin.html`
- Password docente predefinita: `analisi2026`
  (cambiala impostando la variabile d'ambiente `ADMIN_PASSWORD` prima di
  avviare il server, es. `ADMIN_PASSWORD=nuovapassword node server.js`)

## Come si usa

1. Il docente apre `/admin.html`, inserisce la password e genera N codici
   (uno per ogni studente atteso). I codici possono essere scaricati come
   file `.txt` e proiettati/distribuiti.
2. Ogni studente apre l'URL pubblico, inserisce il proprio codice e il
   proprio nome, ed entra in una sala d'attesa.
3. Il docente clicca "Avvia quiz": tutti gli studenti connessi vedono
   comparire le 50 domande.
4. Il pannello docente mostra in tempo reale (aggiornamento ogni 2 secondi)
   quanti studenti sono in attesa, in corso o hanno completato il quiz, e
   il voto finale di ciascuno.
5. Ogni studente, al termine, vede il numero di risposte corrette e il voto
   in trentesimi (fino a "30 e lode" se risponde correttamente a tutte le
   50 domande).
6. "Termina quiz" blocca l'invio di nuove risposte per tutti; "Reset
   completo" cancella codici, risposte e punteggi per iniziare una nuova
   sessione.

Lo stato (codici, risposte, punteggi) viene salvato su disco in
`data/state.json`, quindi sopravvive a un riavvio del server.

## Le domande

Le 50 domande si trovano in `data/questions.json`, a livello di esame
universitario di Ingegneria (teoremi applicati, studi di funzione
completi, limiti con Taylor/de l'Hôpital, radici complesse, integrali per
parti/sostituzione, ecc.), verificate tutte simbolicamente con sympy. Sono
distribuite in proporzione ai CFU: 4 numeri reali, 4 numeri complessi, 4
funzioni reali, 8 limiti, 4 funzioni continue, 17 calcolo differenziale, 9
calcolo integrale. 9 domande richiedono di ragionare su un grafico (le
immagini sono in `public/images/`).

Le formule sono scritte in LaTeX (delimitate da `\( ... \)`) e vengono
rese a schermo con **KaTeX**, la libreria che usa gli stessi font
(Computer Modern) dei libri di testo di matematica; viene caricata da CDN,
quindi serve una normale connessione a internet lato studente (ce l'ha
già, dato che l'app stessa è online).

Puoi modificare testo, opzioni o immagini direttamente nel file JSON (il
campo `correct` è l'indice — a partire da 0 — dell'opzione corretta
nell'array `options`); non serve rigenerare nulla, basta salvare il file
e riavviare il server. Lo script `gen_questions.py` (non necessario
all'esecuzione) mostra come sono state costruite, se vuoi aggiungerne
altre nello stesso stile.

## Distribuire l'app online oggi stesso

Il server è pensato per girare ovunque con `node server.js`, senza build
né database esterni. Due opzioni gratuite e rapide:

### Opzione A — Replit (la più veloce, zero configurazione)

1. Vai su replit.com, crea un account (se non ce l'hai) e crea un nuovo
   Repl "Node.js".
2. Carica tutti i file di questa cartella (o trascina lo zip e importalo).
3. Premi "Run": Replit mostra subito un URL pubblico (riquadro webview /
   "Open in a new tab") utilizzabile dagli studenti finché il Repl resta
   aperto nel tuo browser.
4. Va benissimo per una sessione di un giorno; non serve pubblicare
   (Deploy) l'app, basta lasciarla in esecuzione durante l'esercitazione.

### Opzione B — Render.com (URL stabile, resta online anche più giorni)

1. Crea un account gratuito su render.com (con GitHub, GitLab o Google,
   senza carta di credito).
2. Carica questa cartella su un repository GitHub (puoi usare "Add file
   → Upload files" direttamente dal sito di GitHub, senza riga di
   comando).
3. Su Render: "New +" → "Web Service" → collega il repository.
   - Build command: (lascialo vuoto, non serve)
   - Start command: `node server.js`
4. Aggiungi la variabile d'ambiente `ADMIN_PASSWORD` con una password a
   tua scelta.
5. Deploy: dopo 1-2 minuti ottieni un URL pubblico tipo
   `https://tuonome.onrender.com`.
6. Nota: il piano gratuito "si addormenta" dopo 15 minuti di inattività
   e la prima richiesta successiva impiega 30-60 secondi a rispondere;
   apri tu l'URL qualche minuto prima di iniziare l'esercitazione così è
   già "sveglio" quando arrivano gli studenti.

In entrambi i casi l'URL da dare agli studenti è quello pubblico (senza
`/admin.html`); tu userai `<stesso-url>/admin.html` per il pannello di
controllo.
