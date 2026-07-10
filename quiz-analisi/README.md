# Quiz di Analisi Matematica I

Web app per l'esercitazione: ogni studente accede con un codice univoco e
riceve un quiz personalizzato (40 domande, pescate casualmente da una banca
dati di 404, modellata sulle tracce d'esame reali del docente), il docente avvia il quiz e ne segue l'avanzamento in tempo
reale, può rivedere in ogni momento le domande e le risposte di ciascuno
studente, e al termine ogni studente vede il proprio punteggio e il voto in
trentesimi. Funziona anche in modalità asincrona: una volta avviato il
quiz resta attivo finché non lo termini tu, quindi ogni studente può
svolgerlo quando vuole (anche da casa, in giorni diversi).

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
   (uno per ogni studente atteso). Alla generazione, ogni codice riceve
   subito un proprio quiz personalizzato di 40 domande (vedi sotto). I
   codici possono essere scaricati come file `.txt` e distribuiti.
2. Ogni studente apre l'URL pubblico, inserisce il proprio codice e il
   proprio nome, ed entra in una sala d'attesa.
3. Il docente clicca "Avvia quiz": da quel momento chiunque inserisca un
   codice valido vede comparire le proprie 40 domande. Il quiz resta
   attivo finché non clicchi "Termina quiz", quindi va bene anche per uso
   asincrono (studenti che si collegano in momenti diversi, anche da casa).
4. Il pannello docente mostra in tempo reale (aggiornamento ogni 2 secondi)
   quanti studenti sono in attesa, in corso o hanno completato il quiz, e
   il voto finale di ciascuno. Cliccando "Vedi quiz" su una riga puoi
   rivedere tutte le domande assegnate a quello studente, con la sua
   risposta e quella corretta evidenziate (funziona anche prima che lo
   studente abbia iniziato, per controllare in anteprima il suo quiz).
5. Ogni studente, al termine, vede il numero di risposte corrette e il voto
   in trentesimi (fino a "30 e lode" se risponde correttamente a tutte le
   40 domande).
6. "Termina quiz" blocca l'invio di nuove risposte per tutti; "Reset
   completo" cancella codici, risposte e punteggi per iniziare una nuova
   sessione.

Lo stato (codici, quiz assegnati, risposte, punteggi) viene salvato su
disco in `data/state.json`, quindi sopravvive a un riavvio del server.

## Le domande e il quiz personalizzato

`data/questions.json` contiene una banca dati di **404 domande** (almeno 50
per ciascuno dei 7 capitoli del programma, alcuni ne hanno di più).

Il nucleo principale delle domande è stato **modellato direttamente sulle
tracce d'esame reali del docente** (8 compiti di "Esonero di Analisi
Matematica, Corso E" forniti come esempio): ogni traccia segue sempre lo
stesso schema — disequazione esponenziale/logaritmica + semplificazione
trigonometrica inversa + radici n-esime di un numero complesso; teoria +
enunciato di un teorema + studio di funzione (immagine/monotonia/
asintoti); teoria + integrale; enunciato e dimostrazione di un teorema. Per
riprodurre fedelmente questo stile sono stati scritti generatori dedicati
(cartella `bank/`, prefisso `exam_`), ciascuno verificato con sympy o per
via numerica:

- `exam_algebra.py` — disequazioni esponenziali/logaritmiche a base
  comune, con base variabile (\(\log_x(\cdot)\)), stesso schema delle
  tracce (es. \(\log_{1/\pi}(2x^2-4)\ge\log_{1/\pi}(9-3x)\)).
- `exam_trig_inverse.py` — semplificazioni tipo \(\sin(\arctan(-1/3))\),
  \(\arctan(\tan(2\pi/3))\), calcolate e verificate numericamente.
- `exam_complex_roots.py` — equazioni \(z^n=w\) e "radici n-esime di ..."
  esattamente nello stile delle tracce (es. \(z^5=9i\), radici quinte di
  \(-8\)).
- `exam_function_study.py` — le quattro famiglie di "studio di funzione"
  viste nelle tracce: \(|x^2-x-2|\) (immagine/estremi assoluti),
  \((x-1)^{1/3}-(x+1)^{1/3}\) (monotonia), \(|x|e^{1/(x-1)}\) (asintoti),
  \(\ln(|\ln x|)-2\ln^2(|x|)\) (asintoti/immagine/massimo assoluto) — con
  formula chiusa generica ricavata e verificata per ciascuna famiglia.
- `exam_integrali.py` — gli stessi tipi di integrale delle tracce
  (\(\int x^3/\sqrt{9+x^2}\,dx\), \(\int\cos(\ln x)\,dx\),
  \(\int x^2/(\sqrt{x}(x+1))\,dx\), \(\int(\tan^4x-4)/(\tan x+\sqrt2)\,dx\),
  \(\int(x+1)/\sqrt{x^2+6x+10}\,dx\), \(\int 1/\sin^2x\,dx\),
  \(\int(x^2+x)/(3-2x+x^2)\,dx\)), con primitiva verificata derivandola
  numericamente e confrontandola con l'integranda.
- `exam_teoremi.py` — enunciato/ipotesi/dimostrazione dei teoremi
  richiesti nelle tracce: Weierstrass, de l'Hôpital, media integrale,
  Teorema degli zeri (e relazione con Bolzano), Fermat (con la catena di
  implicazioni "f derivabile n volte ⇒ f^(n-2) continua ⇒ f continua"),
  Lagrange, unicità del limite, Teorema Fondamentale del Calcolo, criteri
  di monotonia/convessità.

Le domande "generiche" già presenti (`ch1_reali.py` ... `ch7_integrale.py`,
`extra_from_slides.py`, `ch4_successioni.py`, a livello di esame
universitario di Ingegneria, generate e verificate simbolicamente con
sympy) restano nella banca dati ma solo come **riempimento**: vengono
usate esclusivamente nei capitoli dove il materiale stile-esame da solo
non basta a raggiungere 50 domande. Resta incluso anche un nucleo di
domande curate manualmente con grafici da interpretare.

Il conteggio per capitolo (`curate` = con grafici, `stile-esame` = dalle
tracce del docente, `riempimento` = generatori generici):

| Capitolo | Totale | curate | stile-esame | riempimento |
|---|---|---|---|---|
| 1. Numeri reali | 50 | 4 | 36 | 10 |
| 2. Numeri complessi | 62 | 4 | 58 | 0 |
| 3. Funzioni reali | 58 | 4 | 54 | 0 |
| 4. Limiti | 50 | 8 | 15 | 27 |
| 5. Funzioni continue | 50 | 4 | 10 | 36 |
| 6. Calcolo differenziale | 64 | 17 | 47 | 0 |
| 7. Calcolo integrale | 70 | 9 | 61 | 0 |
| **Totale** | **404** | | | |

Quando generi un codice, il server compone automaticamente un quiz da 40
domande pescandole così dalla banca dati:

| Capitolo | Domande pescate |
|---|---|
| 1. Numeri reali | 5 |
| 2. Numeri complessi | 6 |
| 3. Funzioni reali | 6 |
| 4. Limiti | 5 |
| 5. Funzioni continue | 6 |
| 6. Calcolo differenziale | 6 |
| 7. Calcolo integrale | 6 |
| **Totale** | **40** |

Ogni studente riceve quindi una combinazione diversa (e in ordine
mescolato), riducendo il rischio che due studenti vicini abbiano lo stesso
identico quiz.

Le formule sono scritte in LaTeX (delimitate da `\( ... \)`) e vengono
rese a schermo con **KaTeX**, la libreria che usa gli stessi font
(Computer Modern) dei libri di testo di matematica; viene caricata da CDN,
quindi serve una normale connessione a internet lato studente (ce l'ha
già, dato che l'app stessa è online).

Puoi modificare testo, opzioni o immagini direttamente in
`data/questions.json` (il campo `correct` è l'indice — a partire da 0 —
dell'opzione corretta nell'array `options`, il campo `chapter` è il numero
1-7 del capitolo); non serve rigenerare nulla, basta salvare il file e
riavviare il server. La cartella `bank/` contiene gli script Python usati
per generare le domande (non necessari all'esecuzione dell'app): i
generatori `exam_*.py` (stile-esame, prioritari), quelli per capitolo
(`ch1_reali.py` ... `ch7_integrale.py`, usati come riempimento),
`ch4_successioni.py` ed `extra_from_slides.py` per gli argomenti aggiunti
dalle slide del corso, più `build_bank.py` che li combina tutti nel file
finale — utili come riferimento se vuoi aggiungerne altre nello stesso
stile.

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
