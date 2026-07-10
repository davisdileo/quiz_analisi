# -*- coding: utf-8 -*-
"""Affermazioni 'vero o falso, giustificando la risposta' tratte
fedelmente dalle 7 tracce d'esame 'Esonero di Analisi Matematica modulo A
- classe B' (A.A. 2025/2026) caricate dall'utente (07/11/2025, 15/01/2026,
03/02/2026, 24/02/2026, 23/04/2026, 19/06/2026, 10/07/2026). Ogni traccia
ne contiene 6-8, per un totale di 56 affermazioni. Ciascuna è stata
verificata a mano (con calcolo esplicito dove serve: limiti, derivate,
insiemi di definizione, controesempi) e trasformata in una domanda a
risposta multipla: il verdetto corretto (vero/falso) compare una sola
volta tra le 4 opzioni, sempre accompagnato dalla motivazione corretta;
i distrattori hanno il verdetto sbagliato e/o la motivazione sbagliata.
"""


def wrap(s):
    return f"\\({s}\\)"


def make_list():
    out = []
    seen = set()
    current_chapter = [5]

    def set_chapter(ch):
        current_chapter[0] = ch

    def add(text, correct, wrong):
        if len(set([correct] + wrong)) != 4 or len(wrong) != 3:
            return False
        if text in seen:
            return False
        seen.add(text)
        out.append({"text": text, "correct": correct, "wrong": wrong, "chapter": current_chapter[0]})
        return True

    return out, add, set_chapter


def build_tagged():
    items, add, ch = make_list()

    # ============ Traccia 07/11/2025 ============
    ch(6)
    add(r'Sia D l\'insieme di definizione di \(f(x) = x\log^3 x\). L\'affermazione "\(D_r D = \mathbb{R}\)" (dove \(D_r\) indica il derivato di D) è:',
        "Falsa: D=(0,+∞), il suo derivato è \\([0,+\\infty)\\), non tutto \\(\\mathbb{R}\\) (i numeri negativi non sono di accumulazione per D)",
        ["Vera: ogni punto di \\(\\mathbb{R}\\) è di accumulazione per (0,+∞)", "Falsa: D non ha punti di accumulazione", "Vera: il derivato di un insieme illimitato è sempre \\(\\mathbb{R}\\)"])

    ch(4)
    add(r'L\'affermazione \(\displaystyle\lim_{n\to+\infty}\frac{\sin(n^2)}{n^2}=1\) è:',
        "Falsa: per il teorema del confronto, \\(\\left|\\frac{\\sin(n^2)}{n^2}\\right|\\le\\frac{1}{n^2}\\to 0\\), quindi il limite vale 0, non 1",
        ["Vera: \\(\\sin(n^2)\\) e \\(n^2\\) crescono allo stesso modo", "Falsa: il limite non esiste perché \\(\\sin(n^2)\\) oscilla", "Vera: per \\(n\\to+\\infty\\), \\(\\sin(n^2)\\to n^2\\)"])

    ch(5)
    add(r"L'affermazione \(f,g\in C(\mathbb{R}) \Rightarrow \sqrt{fg}\in C(\mathbb{R})\) è:",
        "Falsa: se il prodotto fg è negativo in qualche punto, \\(\\sqrt{fg}\\) non è nemmeno definita lì (es. \\(f=x,\\ g=1\\))",
        ["Vera: il prodotto e la radice di funzioni continue sono sempre continui", "Falsa: fg non è mai continua se f e g lo sono", "Vera: basta che f e g siano positive, ipotesi implicita nel testo"])
    add(r"L'affermazione \(f\in C((a,b)),\ f\) prolungabile con continuità in \(a\) \(\Rightarrow f\) limitata è:",
        "Falsa: f potrebbe non essere prolungabile (o essere illimitata) in un intorno di b, l'altro estremo dell'intervallo",
        ["Vera: prolungare con continuità in un estremo rende automaticamente f limitata su tutto (a,b)", "Falsa: nessuna funzione continua su un intervallo aperto è limitata", "Vera: per il Teorema di Weierstrass applicato ad (a,b)"])
    add(r"L'affermazione \(f\in C([a,b])\) strettamente crescente \(\Rightarrow f\) ammette uno e un solo zero in \((a,b)\) è:",
        "Falsa: senza ipotesi sul segno di f(a) e f(b), f potrebbe non avere alcuno zero (es. f sempre positiva)",
        ["Vera: ogni funzione strettamente crescente e continua ha uno zero", "Falsa: una funzione strettamente crescente non può mai avere zeri", "Vera: per il Teorema degli zeri, sempre applicabile alle funzioni monotone"])
    add(r"L'affermazione \(f:X\subseteq\mathbb{R}\to\mathbb{R},\ f(X)\) intervallo \(\Rightarrow X\) intervallo è:",
        "Falsa: X può essere un insieme sconnesso e avere comunque immagine un intervallo (es. f costante su X sconnesso)",
        ["Vera: solo un dominio a forma di intervallo può dare immagine a forma di intervallo", "Falsa: l'immagine di una funzione non è mai un intervallo", "Vera: per il Teorema di Bolzano applicato all'immagine"])

    ch(7)
    add(r"L'affermazione \(f(x)=\sin^4 x\cdot 2^{x^3+x^8}+\log_4(x^2+1)\) non ammette primitive è:",
        "Falsa: f è definita e continua su tutto \\(\\mathbb{R}\\) (nessun problema di dominio), quindi per il Teorema Fondamentale del Calcolo ammette sempre una primitiva",
        ["Vera: la funzione è troppo complicata per avere una primitiva elementare", "Vera: \\(\\log_4(x^2+1)\\) non è definito per \\(x=0\\)", "Falsa: solo le funzioni polinomiali ammettono primitive"])
    add(r"Sia \(F(x)=\int_0^x 2(t^2+1)^4\,dt\). L'affermazione \"F è strettamente crescente su \\(\\mathbb{R}\\)\" è:",
        "Vera: F'(x) = \\(2(x^2+1)^4>0\\) per ogni x, quindi F è strettamente crescente per il criterio di monotonia",
        ["Falsa: F non è derivabile ovunque", "Falsa: F'(x) può annullarsi e cambiare segno", "Vera, ma solo perché l'integrando è un polinomio, non per il segno della derivata"])

    # ============ Traccia 15/01/2026 ============
    ch(1)
    add(r'Sia X l\'insieme di definizione di \(g(x)=\dfrac{1}{(x+1)^2(\log|x|+1)^3}\). L\'affermazione "\(\operatorname{Fr}X=\emptyset\)" (frontiera di X) è:',
        "Falsa: X = \\(\\mathbb{R}\\setminus\\{-1,0,1/e,-1/e\\}\\) è aperto ma non chiuso; la sua frontiera è proprio l'insieme dei 4 punti esclusi, non vuota",
        ["Vera: X è un aperto, e la frontiera di un aperto è sempre vuota", "Vera: X coincide con tutto \\(\\mathbb{R}\\)", "Falsa: X non ammette punti esclusi dal dominio"])

    ch(4)
    add(r"L'affermazione \(h(x)=\dfrac{\sqrt{x^2-1}}{x}\) non ammette limite per \(x\to-\infty\) è:",
        "Falsa: per \\(x\\to-\\infty\\), \\(\\sqrt{x^2-1}\\sim|x|=-x\\), quindi \\(h(x)\\to -x/x=-1\\): il limite esiste e vale \\(-1\\)",
        ["Vera: la funzione oscilla senza stabilizzarsi", "Vera: il dominio non si estende fino a \\(-\\infty\\)", "Falsa: il limite esiste e vale \\(+1\\)"])
    add(r"L'affermazione \((a_n)_{n\in\mathbb{N}}\) limitata \(\Rightarrow (a_n)_{n\in\mathbb{N}}\) monotòna è:",
        "Falsa: es. \\(a_n=(-1)^n\\) è limitata ma non è monotòna",
        ["Vera: ogni successione limitata è definitivamente monotòna", "Vera: per il Teorema di Bolzano-Weierstrass", "Falsa: nessuna successione limitata può essere non monotòna"])

    ch(5)
    add(r"L'affermazione \(f\in C((a,b]),\ f\) prolungabile con continuità in \(a\) \(\Rightarrow f\) limitata è:",
        "Vera: prolungando in a si ottiene \\(f\\in C([a,b])\\), dominio compatto, quindi f è limitata per il Teorema di Weierstrass",
        ["Falsa: prolungare in un solo estremo non garantisce nulla sulla limitatezza", "Falsa: [a,b] non è un insieme compatto", "Vera, ma solo se f è anche derivabile"])

    ch(1)
    add(r"Sia \(p(x)=-\pi x^9-2x^3\). L'affermazione \"p ammette uno e un solo zero reale\" è:",
        "Vera: \\(p(x)=-x^3(\\pi x^6+2)\\), il fattore \\(\\pi x^6+2>0\\) sempre, quindi l'unico zero è \\(x=0\\) (e p è strettamente decrescente)",
        ["Falsa: p è un polinomio di grado 9, quindi ha 9 zeri reali distinti", "Falsa: p non si annulla mai", "Vera, ma per un motivo diverso: p è pari"])

    ch(6)
    add(r'Il polinomio di Taylor di grado 3 in \(x_0=1\) della funzione \(f(x)=1/x\) è \(1+(x-1)^2+(x-1)^3\): questa affermazione è:',
        "Falsa: il polinomio corretto è \\(1-(x-1)+(x-1)^2-(x-1)^3\\) (manca il termine lineare \\(-(x-1)\\) e il segno del termine cubico è errato)",
        ["Vera: le derivate di \\(1/x\\) in \\(x_0=1\\) danno esattamente quei coefficienti", "Vera, a meno del resto di Peano", "Falsa: il polinomio di Taylor di \\(1/x\\) ha solo termini pari"])

    ch(7)
    add(r"L'affermazione \"F primitiva di f su \\(\\mathbb{R}\\) e \\(f\\ge0\\) su \\(\\mathbb{R}\\) \\(\\Rightarrow\\) F crescente\" è:",
        "Vera: \\(F'=f\\ge0\\) ovunque implica, per il criterio di monotonia, che F è crescente (non decrescente)",
        ["Falsa: F potrebbe comunque decrescere in qualche tratto", "Falsa: servirebbe \\(f>0\\) strettamente, non \\(f\\ge0\\)", "Vera, ma solo se F è anche limitata"])
    add(r"Sia \(k\in C(\mathbb{R})\) dispari. L'affermazione \(\displaystyle\int_{-1}^{2}k(t)\,dt = \int_1^2 k(t)\,dt\) è:",
        "Vera: per k dispari \\(\\int_{-1}^1 k=0\\) per simmetria, quindi \\(\\int_{-1}^2 k = \\int_{-1}^1 k+\\int_1^2 k = \\int_1^2 k\\)",
        ["Falsa: per una funzione dispari l'integrale su ogni intervallo simmetrico è diverso da zero", "Falsa: l'uguaglianza vale solo se k è pari, non dispari", "Vera, ma solo se k è anche limitata"])

    # ============ Traccia 03/02/2026 ============
    ch(1)
    add(r'Sia D l\'insieme di definizione di \(f(x)=\dfrac{\log x+1}{\log x-1}\). L\'affermazione "D è chiuso" è:',
        "Falsa: D = \\((0,e)\\cup(e,+\\infty)\\), unione di due intervalli aperti, quindi D è aperto, non chiuso",
        ["Vera: D è il complementare di un punto, quindi chiuso", "Vera: ogni dominio di una funzione razionale in \\(\\log x\\) è chiuso", "Falsa: D è addirittura tutto \\(\\mathbb{R}\\)"])

    ch(3)
    add(r"L'affermazione \(h(x)=\dfrac{x}{\sqrt{1-x^2}}\) è dispari è:",
        "Vera: \\(h(-x) = \\dfrac{-x}{\\sqrt{1-x^2}} = -h(x)\\) per ogni x nel dominio",
        ["Falsa: h è pari, perché contiene \\(x^2\\) al denominatore", "Falsa: h non ha alcuna simmetria", "Vera, ma solo su metà del dominio"])

    ch(4)
    add(r"L'affermazione \((a_n)_{n\in\mathbb{N}}\) monotòna \(\Rightarrow (a_n)_{n\in\mathbb{N}}\) regolare è:",
        "Vera: è il Teorema di regolarità delle successioni monotòne (ogni successione monotòna converge o diverge a \\(\\pm\\infty\\))",
        ["Falsa: una successione monotòna può non avere alcun limite", "Falsa: servirebbe anche la limitatezza", "Vera, ma solo per le successioni crescenti, non per quelle decrescenti"])

    ch(5)
    add(r"L'affermazione \(f:X\subseteq\mathbb{R}\to\mathbb{R},\ X\) compatto \(\Rightarrow f\) limitata è:",
        "Falsa: manca l'ipotesi di continuità di f; senza di essa (Teorema di Weierstrass) X compatto da solo non basta",
        ["Vera: la compattezza del dominio basta sempre a garantire la limitatezza di f", "Vera: è esattamente il Teorema di Weierstrass", "Falsa: nessuna funzione su un compatto è limitata"])
    add(r"L'affermazione \(f\in C([a,b]) \Rightarrow f\) ha uno e un solo punto di minimo assoluto è:",
        "Falsa: il Teorema di Weierstrass garantisce l'esistenza del minimo assoluto, ma f potrebbe raggiungerlo in più punti (es. f costante)",
        ["Vera: il Teorema di Weierstrass garantisce anche l'unicità del minimo", "Falsa: f potrebbe non avere alcun minimo assoluto", "Vera, se f è anche strettamente monotòna"])

    ch(6)
    add(r"L'affermazione \(F:(2,5)\cup(6,7)\to\mathbb{R}\) derivabile, \(F'(x)=0\) su \((2,5)\cup(6,7)\) \(\Rightarrow F\) costante su \((2,5)\cup(6,7)\) è:",
        "Falsa: il dominio è sconnesso (unione di due intervalli disgiunti); F è costante su ciascun intervallo separatamente, ma le due costanti possono essere diverse",
        ["Vera: derivata nulla implica sempre funzione costante, indipendentemente dal dominio", "Falsa: F'=0 non implica nulla sulla monotonia di F", "Vera, per il criterio di monotonia applicato globalmente"])
    add(r"Il polinomio di Taylor di grado 2 di \(f(x)=\arcsin x\) di punto iniziale \(x_0=\sqrt3/2\) è \(p_2(x)=\pi/3+2x\): questa affermazione è:",
        "Falsa: sviluppando correttamente si ottiene \\(p_2(x)=\\pi/3+2(x-\\sqrt3/2)+2\\sqrt3(x-\\sqrt3/2)^2\\), diverso da \\(\\pi/3+2x\\) (manca lo sviluppo attorno a \\(x_0\\) e il termine quadratico)",
        ["Vera: le derivate di \\(\\arcsin\\) in \\(x_0=\\sqrt3/2\\) danno esattamente quei coefficienti", "Vera, il termine quadratico è nullo per \\(\\arcsin\\)", "Falsa: il polinomio di Taylor di \\(\\arcsin\\) ha solo potenze dispari"])

    ch(7)
    add(r"L'affermazione \(\displaystyle\int_{-e}^{e} x^8\,\pi^{x^6}\cos x\,dx = 0\) è:",
        "Falsa: l'integrando \\(x^8\\pi^{x^6}\\cos x\\) è una funzione PARI (prodotto di funzioni pari), quindi l'integrale su un intervallo simmetrico NON è in generale zero (lo sarebbe solo per funzioni dispari)",
        ["Vera: ogni integrale su un intervallo simmetrico rispetto a 0 vale zero", "Vera: l'integrando è una funzione dispari", "Falsa: l'integrale è zero solo perché il dominio è simmetrico, indipendentemente dalla parità"])

    # ============ Traccia 24/02/2026 ============
    ch(1)
    add(r"L'affermazione \(1\in D_r\mathbb{N}\) (1 è punto di accumulazione di \(\mathbb{N}\)) è:",
        "Falsa: \\(\\mathbb{N}\\) è un insieme discreto, ogni suo punto è isolato: nessun intorno di 1 privato di 1 contiene altri naturali",
        ["Vera: 1 è il primo elemento di \\(\\mathbb{N}\\), quindi è di accumulazione", "Vera: ogni sottoinsieme infinito di \\(\\mathbb{R}\\) ha punti di accumulazione al suo interno", "Falsa: \\(\\mathbb{N}\\) non ha alcun punto di accumulazione, nemmeno in \\(\\mathbb{R}\\)"])

    ch(2)
    add(r'L\'affermazione "la parte immaginaria di \(z=\dfrac{1}{2-3i}\) scritta in forma algebrica è \(-3i\)" è:',
        "Falsa: razionalizzando, \\(z=\\dfrac{2+3i}{13}\\), quindi \\(\\operatorname{Im}(z)=3/13\\) (un numero reale, non \\(-3i\\))",
        ["Vera: basta guardare il segno davanti a \\(3i\\) nel denominatore", "Vera: \\(\\operatorname{Im}(z)\\) può essere un numero complesso", "Falsa: \\(\\operatorname{Im}(z)=-3/13\\)"])

    ch(4)
    add(r"L'affermazione \(\nexists\displaystyle\lim_{x\to+\infty}\left(\cos^2 x+x^3\arctan(x^2)\right)\) è:",
        "Falsa: \\(\\cos^2x\\) è limitato in [0,1] mentre \\(x^3\\arctan(x^2)\\to+\\infty\\cdot\\pi/2=+\\infty\\); il limite esiste e vale \\(+\\infty\\)",
        ["Vera: \\(\\cos^2x\\) oscilla indefinitamente e impedisce l'esistenza del limite", "Vera: la somma di una funzione limitata e una divergente non ha limite", "Falsa: il limite esiste mafinito, vale 0"])
    add(r"L'affermazione \((a_n)_{n\in\mathbb{N}}\) regolare \(\Rightarrow (a_n)_{n\in\mathbb{N}}\) convergente è:",
        "Falsa: 'regolare' significa convergente OPPURE divergente a \\(\\pm\\infty\\); una successione regolare può benissimo divergere",
        ["Vera: per definizione regolare equivale a convergente", "Vera: solo le successioni irregolari possono divergere", "Falsa: nessuna successione regolare converge"])

    ch(5)
    add(r"L'affermazione \(f:X\subseteq\mathbb{R}\to\mathbb{R}\) discontinua in \(x_0\in X \Rightarrow f\) non limitata è:",
        "Falsa: una funzione può avere una discontinuità (es. un salto) restando comunque limitata, es. la funzione segno",
        ["Vera: ogni discontinuità implica un comportamento illimitato vicino al punto", "Vera: solo le funzioni continue possono essere limitate", "Falsa: una funzione discontinua è sempre continua sul resto del dominio, quindi limitata"])
    add(r"L'affermazione \(f:X\subseteq\mathbb{R}\to\mathbb{R},\ x_0\in X\) punto di minimo assoluto per f \(\Rightarrow f\) derivabile in \(x_0\) è:",
        "Falsa: es. \\(f(x)=|x|\\) ha minimo assoluto in \\(x_0=0\\) ma non è derivabile lì",
        ["Vera: nei punti di estremo assoluto la funzione è sempre derivabile con derivata nulla", "Vera: per il Teorema di Fermat, sempre applicabile ai minimi assoluti", "Falsa: nessuna funzione con un minimo assoluto è derivabile in alcun punto"])

    ch(7)
    add(r"L'affermazione \(h\in C(\mathbb{R}) \Rightarrow H(x):=\int_0^x h(t)\,dt \in C(\mathbb{R})\) è:",
        "Vera: per il Teorema Fondamentale del Calcolo, H è addirittura derivabile con \\(H'=h\\), quindi in particolare continua",
        ["Falsa: H potrebbe non essere definita per ogni x", "Falsa: l'integrale di una funzione continua non è mai continuo", "Vera, ma solo se h è anche limitata"])
    add(r"L'affermazione \(\displaystyle\int_{-10}^{10} 3^{10|x|}\,dx = 0\) è:",
        "Falsa: l'integrando \\(3^{10|x|}\\) è sempre strettamente positivo, quindi l'integrale è un numero positivo, non zero",
        ["Vera: l'intervallo di integrazione è simmetrico rispetto a 0", "Vera: \\(3^{10|x|}\\) è una funzione dispari", "Falsa: l'integrale vale esattamente 0 solo nel punto \\(x=0\\)"])

    # ============ Traccia 19/06/2026 ============
    ch(6)
    add(r'Sia \(k(x)=x^2\sin(1/x)\) per \(x\neq0\), \(k(0)=0\). L\'affermazione "il Teorema di Rolle è applicabile in \([-1/\pi,1/\pi]\) a k" è:',
        "Vera: k è continua su \\([-1/\\pi,1/\\pi]\\) (incluso in 0, dove il limite è 0), derivabile su \\((-1/\\pi,1/\\pi)\\) (anche in 0, con \\(k'(0)=0\\)), e \\(k(-1/\\pi)=k(1/\\pi)=0\\): tutte le ipotesi sono verificate",
        ["Falsa: k non è derivabile in \\(x=0\\)", "Falsa: \\(k(-1/\\pi)\\neq k(1/\\pi)\\)", "Vera, ma solo perché k è dispari"])

    ch(4)
    add(r'L\'affermazione "la successione \(a_n=\dfrac{(-1)^n}{n^3}\) è limitata" è:',
        "Vera: \\(|a_n|=1/n^3\\le1\\) per ogni \\(n\\ge1\\), quindi la successione è limitata (ed è anche infinitesima)",
        ["Falsa: il fattore \\((-1)^n\\) la rende illimitata", "Falsa: \\(1/n^3\\to+\\infty\\)", "Vera, ma solo per n pari"])

    ch(6)
    add(r'L\'affermazione "l\'equazione \(\log x=1+1/x\), \(x\in(0,+\infty)\), ha due soluzioni reali" è:',
        "Falsa: posto \\(h(x)=\\log x-1-1/x\\), si ha \\(h'(x)=1/x+1/x^2>0\\) sempre: h è strettamente crescente, quindi ha al più (e in questo caso esattamente) una soluzione",
        ["Vera: un'equazione logaritmica ha sempre più soluzioni", "Vera: per il Teorema degli zeri applicato due volte", "Falsa: l'equazione non ha alcuna soluzione reale"])

    ch(7)
    add(r'L\'affermazione "tutte le funzioni derivabili sono dotate di primitive" è:',
        "Vera: f derivabile \\(\\Rightarrow\\) f continua \\(\\Rightarrow\\) (per il Teorema Fondamentale del Calcolo) f ammette una primitiva",
        ["Falsa: derivabilità e integrabilità sono proprietà indipendenti", "Falsa: solo le funzioni polinomiali derivabili hanno primitive", "Vera, ma solo se f è anche limitata"])

    ch(5)
    add(r"L'affermazione \(f,g\in C(\mathbb{R}) \Rightarrow f/g\in C(\mathbb{R})\) è:",
        "Falsa: se g si annulla in qualche punto, f/g non è nemmeno definita lì, quindi non può essere continua su tutto \\(\\mathbb{R}\\)",
        ["Vera: il quoziente di funzioni continue è sempre continuo dove definito, cioè ovunque", "Vera: basta che g non sia mai negativa", "Falsa: il quoziente di funzioni continue non è mai continuo"])
    add(r'L\'affermazione "la funzione \(f(x)=\log|x|\) è prolungabile con continuità in \(x=0\)" è:',
        "Falsa: \\(\\lim_{x\\to0}\\log|x|=-\\infty\\) (limite infinito, non un valore finito), quindi f non è prolungabile con continuità in 0",
        ["Vera: basta porre \\(f(0)=0\\)", "Vera: il limite per \\(x\\to0\\) esiste finito", "Falsa: f non ha nemmeno un limite (né finito né infinito) per \\(x\\to0\\)"])

    ch(1)
    add(r"L'affermazione \(X\subset\mathbb{R}\) limitato \(\Rightarrow\) esiste \(\min X\) è:",
        "Falsa: es. \\(X=(0,1)\\) è limitato ma non ha minimo (l'estremo inferiore 0 non è raggiunto)",
        ["Vera: ogni insieme limitato ha minimo e massimo", "Vera: per l'assioma di completezza di \\(\\mathbb{R}\\)", "Falsa: nessun insieme limitato ha estremo inferiore"])

    ch(7)
    add(r'L\'affermazione "\(g\in C(\mathbb{R}) \Rightarrow h(x)=\displaystyle\int_2^x g(t)\,dt\in C(\mathbb{R})\)" è:',
        "Vera: per il Teorema Fondamentale del Calcolo, h è derivabile con \\(h'=g\\), quindi in particolare continua su tutto \\(\\mathbb{R}\\)",
        ["Falsa: l'estremo di integrazione 2 rende h discontinua in \\(x=2\\)", "Falsa: h è definita solo per \\(x\\ge2\\)", "Vera, ma solo se g è anche derivabile"])

    # ============ Traccia 10/07/2026 ============
    ch(5)
    add(r"L'affermazione \(h(x)=2\arctan x-\sqrt x,\ x\in[0,3]\) è dotata di estremi assoluti è:",
        "Vera: h è continua su [0,3], che è chiuso e limitato (compatto); per il Teorema di Weierstrass h ammette massimo e minimo assoluti",
        ["Falsa: \\(\\sqrt x\\) non è definita per \\(x<0\\), quindi il teorema non si applica", "Falsa: [0,3] non è un insieme compatto", "Vera, ma solo perché h è monotòna"])

    ch(4)
    add(r'L\'affermazione "la successione \(\left(\dfrac{5^n-1}{5^n+1}\right)_{n\in\mathbb{N}}\) è limitata" è:',
        "Vera: la successione è crescente da 0 e tende a 1 restando sempre in \\([0,1)\\), quindi è limitata",
        ["Falsa: il numeratore e il denominatore divergono entrambi a \\(+\\infty\\)", "Falsa: la successione non è definita per n grandi", "Vera, ma solo perché è decrescente"])

    ch(5)
    add(r'L\'affermazione "se una funzione ha un punto di discontinuità allora non è limitata" è:',
        "Falsa: es. la funzione a gradino (Heaviside) ha una discontinuità in 0 ma resta limitata",
        ["Vera: ogni discontinuità genera un comportamento illimitato", "Vera: per definizione le discontinuità sono sempre di tipo infinito", "Falsa: nessuna funzione discontinua può essere limitata su un intervallo"])

    ch(1)
    add(r"Sia \(p(x)=9x^9-7x^7+5x^5\). L'affermazione \"p ha almeno uno zero reale\" è:",
        "Vera: \\(p(x)=x^5(9x^4-7x^2+5)\\), quindi \\(p(0)=0\\): almeno lo zero \\(x=0\\) esiste",
        ["Falsa: p non si annulla mai per \\(x\\in\\mathbb{R}\\)", "Falsa: essendo di grado 9, p non ha zeri reali ma solo complessi", "Vera, ma il suo unico zero è \\(x=1\\)"])

    ch(4)
    add(r'L\'affermazione "se esiste \(\lim_{n\to+\infty}a_n=\ell>0\) allora \(a_n>0\) per ogni \(n\in\mathbb{N}\)" è:',
        "Falsa: per il Teorema della permanenza del segno, \\(a_n>0\\) vale solo DEFINITIVAMENTE (da un certo n in poi), non necessariamente per i primi termini",
        ["Vera: se il limite è positivo, tutti i termini della successione sono positivi", "Vera: per la definizione stessa di limite", "Falsa: il teorema della permanenza del segno non fornisce alcuna informazione"])

    ch(7)
    add(r"L'affermazione \(F,G\) primitive di f in \((a,b) \Rightarrow \exists c\in\mathbb{R}: F(x)+G(x)=c\ \forall x\in(a,b)\) è:",
        "Falsa: due primitive della stessa funzione differiscono per una costante (\\(F(x)-G(x)=c\\)), non è la loro SOMMA a essere costante",
        ["Vera: è la caratterizzazione standard delle primitive", "Vera, se f è anche continua", "Falsa: non esiste alcuna relazione tra due primitive della stessa funzione"])

    ch(5)
    add(r"L'affermazione \(f\in C(\mathbb{R}) \Rightarrow f\) non ammette estremi assoluti è:",
        "Falsa: es. \\(f(x)=1/(1+x^2)\\) è continua su \\(\\mathbb{R}\\) e ha massimo assoluto in \\(x=0\\)",
        ["Vera: il dominio \\(\\mathbb{R}\\) non è compatto, quindi il Teorema di Weierstrass non garantisce mai estremi assoluti", "Vera: nessuna funzione su un dominio illimitato può avere estremi assoluti", "Falsa: ogni funzione continua su \\(\\mathbb{R}\\) ammette sia massimo che minimo assoluti"])

    ch(7)
    add(r"L'affermazione \(\displaystyle\int_{-1}^{1} e^{-|x|}\,dx = 0\) è:",
        "Falsa: l'integrando \\(e^{-|x|}\\) è sempre strettamente positivo, quindi l'integrale è un numero positivo (vale \\(2(1-e^{-1})\\)), non zero",
        ["Vera: l'intervallo di integrazione è simmetrico rispetto a 0", "Vera: \\(e^{-|x|}\\) è una funzione dispari", "Falsa: l'integrale diverge a \\(+\\infty\\)"])

    # ============ Traccia 23/04/2026 ============
    ch(4)
    add(r'L\'affermazione "\((a_n),(b_n)\) tali che \(a_n\le b_n\ \forall n\), \(b_n\to+\infty \Rightarrow a_n\to+\infty\)" è:',
        "Falsa: la disuguaglianza va nella direzione sbagliata per questa conclusione; es. \\(a_n=0\\le b_n=n\\to+\\infty\\), ma \\(a_n\\) non diverge",
        ["Vera: se il maggiorante diverge, anche il minorante deve divergere", "Vera: per il Teorema del confronto per successioni divergenti", "Falsa: la conclusione corretta è \\(a_n\\to-\\infty\\)"])

    ch(6)
    add(r"L'affermazione \(f(x)=|x+1|(x+1)\) non è derivabile in \(x=-1\) è:",
        "Falsa: f(x) equivale a \\(\\operatorname{sign}(x+1)(x+1)^2\\), che è derivabile anche in \\(x=-1\\) con \\(f'(-1)=0\\) (entrambe le branche hanno derivata nulla lì)",
        ["Vera: il valore assoluto rende sempre non derivabile nel punto critico", "Vera: c'è un punto angoloso in \\(x=-1\\)", "Falsa: f non è nemmeno continua in \\(x=-1\\)"])

    ch(4)
    add(r'L\'affermazione "non esiste \(\displaystyle\lim_{n\to+\infty}\dfrac{(-1)^n\arctan(1/n)}{5n^2+1/n}\)" è:',
        "Falsa: il numeratore è limitato (\\(|\\arctan(1/n)|\\le\\pi/2\\)) mentre il denominatore diverge a \\(+\\infty\\): il limite esiste e vale 0",
        ["Vera: \\((-1)^n\\) fa oscillare la successione senza limite", "Vera: il denominatore si annulla per qualche n", "Falsa: il limite esiste ma vale \\(+\\infty\\)"])

    ch(5)
    add(r'L\'affermazione "una funzione \(f:\mathbb{R}\to\mathbb{R}\) continua non può avere come codominio (immagine) \([0,1]\cup[2,3]\)" è:',
        "Vera: \\(\\mathbb{R}\\) è connesso (un intervallo) e l'immagine continua di un connesso è connessa; \\([0,1]\\cup[2,3]\\) è sconnesso, quindi impossibile",
        ["Falsa: basta una funzione a tratti opportuna per ottenere quell'immagine", "Falsa: il Teorema di Weierstrass lo esclude solo per domini limitati", "Vera, ma solo se f è anche derivabile"])
    add(r'L\'affermazione "\(f:[-3,+\infty)\to\mathbb{R}\) continua e strettamente crescente ha almeno uno zero reale" è:',
        "Falsa: senza ipotesi sul segno di f, f potrebbe essere sempre positiva pur essendo continua e strettamente crescente, es. \\(f(x)=e^x\\)",
        ["Vera: ogni funzione strettamente crescente e continua ha uno zero", "Vera: per il Teorema degli zeri, sempre valido per funzioni monotòne su semirette", "Falsa: nessuna funzione strettamente crescente può avere uno zero"])
    add(r'L\'affermazione "\(f:[-3,+\infty)\to\mathbb{R}\) continua non ha estremi assoluti" è:',
        "Falsa: f potrebbe benissimo avere un minimo o massimo assoluto, es. \\(f(x)=(x+3)^2\\) ha minimo assoluto in \\(x=-3\\)",
        ["Vera: un dominio illimitato impedisce sempre l'esistenza di estremi assoluti", "Vera: per l'assenza del Teorema di Weierstrass su domini non compatti", "Falsa: ogni funzione continua su una semiretta ha sia massimo che minimo assoluti"])
    add(r'L\'affermazione "\(f:[-3,+\infty)\to\mathbb{R}\), \(\lim_{x\to+\infty}f(x)>0 \Rightarrow f(x)>0\) per ogni \(x\ge-3\)" è:',
        "Falsa: per il Teorema della permanenza del segno, \\(f(x)>0\\) vale solo DEFINITIVAMENTE (per x grande), non su tutto il dominio",
        ["Vera: se il limite all'infinito è positivo, tutta la funzione è positiva", "Vera: per definizione di limite finito positivo", "Falsa: il teorema della permanenza del segno non esiste per le funzioni, solo per le successioni"])

    ch(6)
    add(r'Il polinomio di Taylor di grado 3 in \(x_0=0\) di \(f(x)=e^x+\sin x\) è \(1+2x+x^2-\dfrac{x^3}{3}\): questa affermazione è:',
        "Falsa: sviluppando \\(e^x=1+x+x^2/2+x^3/6+\\dots\\) e \\(\\sin x=x-x^3/6+\\dots\\) e sommando si ottiene \\(1+2x+x^2/2+0\\cdot x^3\\) (il termine cubico si annulla esattamente, e quello quadratico è \\(x^2/2\\), non \\(x^2\\))",
        ["Vera: sommando le due serie termine a termine si ottiene esattamente quel polinomio", "Vera, a meno del resto di Peano", "Falsa: il polinomio corretto non ha alcun termine quadratico"])

    return items


def build():
    return [{"text": it["text"], "correct": it["correct"], "wrong": it["wrong"]} for it in build_tagged()]


if __name__ == "__main__":
    items = build_tagged()
    print("Totale affermazioni vero/falso:", len(items))
    bad = 0
    for it in items:
        opts = [it["correct"]] + it["wrong"]
        if len(set(opts)) != 4:
            bad += 1
            print("PROBLEMA:", it["text"])
    print("Domande con problemi:", bad)
    per_ch = {}
    for it in items:
        per_ch[it["chapter"]] = per_ch.get(it["chapter"], 0) + 1
    print("Per capitolo:", per_ch)
