# Quiz di Analisi Matematica I

Web app per l'esercitazione: ogni studente accede con un codice univoco e
riceve un quiz personalizzato (40 domande, pescate casualmente da una banca
dati di 350), il docente avvia il quiz e ne segue l'avanzamento in tempo
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

`data/questions.json` contiene una banca dati di **350 domande** (50 per
ciascuno dei 7 capitoli del programma), a livello di esame universitario
di Ingegneria (teoremi applicati, studi di funzione completi, limiti con
Taylor/de l'Hôpital, radici complesse, integrali per parti/sostituzione,
ecc.), generate e verificate simbolicamente con sympy (ogni risultato è
ricalcolato dal programma, non scritto a mano) più un nucleo di domande
curate manualmente con grafici da interpretare.

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
per generare le domande (non necessari all'esecuzione dell'app): uno per
capitolo (`ch1_reali.py` ... `ch7_integrale.py`) più `build_bank.py` che li
combina nel file finale — utili come riferimento se vuoi aggiungerne altre
nello stesso stile.

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
