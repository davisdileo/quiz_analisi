# -*- coding: utf-8 -*-
"""Domande di teoria su enunciato/dimostrazione dei teoremi che compaiono
nelle tracce d'esame del docente (ogni traccia ha sempre una domanda del
tipo "Enunciare e dimostrare il Teorema di ..."): Weierstrass, de l'Hopital,
Teorema della media integrale, Teorema degli zeri (e relazione con
Bolzano), Teorema di Fermat, Teorema di Lagrange, Teorema di unicita' del
limite, Teorema Fondamentale del Calcolo, criteri di monotonia/convessita'.
Le domande sono scritte a mano seguendo gli enunciati standard dei testi di
Analisi Matematica I; non essendo calcoli simbolici non sono verificabili
con sympy, ma si e' fatta attenzione a riportare fedelmente ipotesi e tesi
di ciascun teorema.
"""


def wrap(s):
    return f"\\({s}\\)"


def make_list():
    out = []
    seen = set()
    current_chapter = [6]  # capitolo di default: Calcolo differenziale

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
    """Restituisce le domande di teoria con il capitolo di destinazione già
    assegnato (Weierstrass/monotonia/Fermat/Lagrange/de l'Hopital -> cap. 6
    Calcolo differenziale; media integrale/Teorema Fondamentale -> cap. 7
    Calcolo integrale; Teorema degli zeri -> cap. 5 Funzioni continue;
    unicità del limite -> cap. 4 Limiti)."""
    items, add, set_chapter = make_list()

    # ---------------- Teorema di Weierstrass ----------------
    set_chapter(5)
    add(r"Il Teorema di Weierstrass afferma che se \(f\) è continua su \([a,b]\) (intervallo chiuso e limitato), allora:",
        "f ammette massimo e minimo assoluti su [a,b]",
        ["f è derivabile su (a,b)", "f è monotona su [a,b]", "f è invertibile su [a,b]"])
    add(r"Nel Teorema di Weierstrass, quali ipotesi sono essenziali su \(f\) e sul dominio?",
        "f continua e dominio chiuso e limitato (compatto)",
        ["f derivabile e dominio limitato", "f continua e dominio aperto", "f monotona e dominio chiuso"])
    add(r"La funzione \(f(x)=1/x\) su \((0,1]\) non ammette minimo assoluto: quale ipotesi del Teorema di Weierstrass viene a mancare?",
        "il dominio (0,1] non è chiuso (non è compatto)",
        ["f non è continua", "f non è definita in x=0", "f non è limitata su (0,1]"])
    add(r"La funzione \(f(x)=x\) su \(\mathbb{R}\) non ammette né massimo né minimo assoluti: quale ipotesi del Teorema di Weierstrass viene a mancare?",
        "il dominio \\(\\mathbb{R}\\) non è limitato (non è compatto)",
        ["f non è continua", "f non è monotona", "f non è derivabile"])
    add(r"Il Teorema di Weierstrass è una condizione:",
        "sufficiente ma non necessaria per l'esistenza di massimo e minimo assoluti",
        ["necessaria ma non sufficiente", "necessaria e sufficiente", "né necessaria né sufficiente"])

    # ---------------- Teoremi di de l'Hopital ----------------
    set_chapter(6)
    add(r"I Teoremi di de l'Hôpital si applicano a limiti della forma:",
        "\\(0/0\\) oppure \\(\\infty/\\infty\\)",
        ["qualunque limite di un rapporto di funzioni", "\\(0\\cdot\\infty\\) soltanto", "\\(\\infty-\\infty\\) soltanto"])
    add(r"Ipotesi dei Teoremi di de l'Hôpital per \(\lim_{x\to x_0} f(x)/g(x)\) in forma \(0/0\): \(f,g\) derivabili in un intorno di \(x_0\) (escluso al più \(x_0\)), \(g'(x)\neq0\) vicino a \(x_0\), \(\lim f=\lim g=0\), e:",
        "esiste (finito o infinito) \\(\\lim_{x\\to x_0} f'(x)/g'(x)\\)",
        ["esiste \\(\\lim_{x\\to x_0} f(x)/g(x)\\) (tesi, non ipotesi)", "\\(f\\) e \\(g\\) sono continue in \\(x_0\\)", "\\(f''\\) e \\(g''\\) esistono"])
    add(r"Se valgono le ipotesi del Teorema di de l'Hôpital, allora:",
        "\\(\\lim_{x\\to x_0} f(x)/g(x) = \\lim_{x\\to x_0} f'(x)/g'(x)\\)",
        ["\\(\\lim_{x\\to x_0} f(x)/g(x) = f'(x_0)/g'(x_0)\\)", "\\(f(x)/g(x)\\) è costante vicino a \\(x_0\\)", "\\(f=g\\) vicino a \\(x_0\\)"])
    add(r"Applicare de l'Hôpital a un limite che NON è nella forma \(0/0\) o \(\infty/\infty\) (senza prima ricondursi a tali forme):",
        "può portare a un risultato errato: le ipotesi del teorema non sono verificate",
        ["è sempre corretto, il teorema vale per ogni limite", "dà sempre \\(0\\)", "dà sempre un risultato indeterminato"])
    add(r"Per calcolare \(\lim_{x\to0}\dfrac{e^x-1-x}{x^2}\) con de l'Hôpital occorre:",
        "verificare che sia una forma \\(0/0\\), poi derivare numeratore e denominatore (eventualmente più volte)",
        ["moltiplicare numeratore e denominatore per \\(x\\)", "sostituire subito \\(x=0\\)", "usare il teorema della media integrale"])

    # ---------------- Teorema della media integrale ----------------
    set_chapter(7)
    add(r"Il Teorema della media integrale afferma che se \(f\in C([a,b])\), esiste \(x_0\in[a,b]\) tale che:",
        r"\( \int_a^b f(x)\,dx = f(x_0)(b-a) \)",
        [r"\( \int_a^b f(x)\,dx = f(a)(b-a) \)", r"\( \int_a^b f(x)\,dx = f(b)-f(a) \)", r"\( f(x_0) = \int_a^b f(x)\,dx \)"])
    add(r"Nella dimostrazione del Teorema della media integrale, il Teorema di Weierstrass garantisce che \(f\) ammette su \([a,b]\):",
        "massimo \\(M\\) e minimo \\(m\\) assoluti, da cui \\(m(b-a)\\le\\int_a^b f\\le M(b-a)\\)",
        ["un unico punto critico", "una primitiva", "un asintoto"])
    add(r"Nella dimostrazione del Teorema della media integrale, dopo aver ottenuto \(m\le \frac{1}{b-a}\int_a^b f(x)\,dx\le M\), quale teorema garantisce l'esistenza di \(x_0\) con \(f(x_0)\) uguale a quel valore medio?",
        "il Teorema dei valori intermedi (di Bolzano), perché f è continua e assume i valori m ed M",
        ["il Teorema di Weierstrass", "il Teorema di Lagrange", "il Teorema di Fermat"])
    add(r"Il valore \(\dfrac{1}{b-a}\int_a^b f(x)\,dx\) fornito dal Teorema della media integrale si chiama:",
        "valor medio integrale di f su [a,b]", ["punto stazionario di f", "estremo superiore di f", "derivata media di f"])

    # ---------------- Teorema degli zeri e relazione con Bolzano ----------------
    set_chapter(5)
    add(r"Il Teorema degli zeri afferma che se \(f\in C([a,b])\) e \(f(a)\cdot f(b)<0\), allora:",
        "esiste \\(c\\in(a,b)\\) tale che \\(f(c)=0\\)",
        ["f è monotona su [a,b]", "f ammette massimo in c", "esiste un unico punto c con f(c)=0"])
    add(r"Qual è la relazione tra il Teorema degli zeri e il Teorema di Bolzano (dei valori intermedi)?",
        "il Teorema degli zeri è il caso particolare del Teorema di Bolzano applicato al valore y=0",
        ["sono teoremi indipendenti, nessuno implica l'altro", "il Teorema di Bolzano è un caso particolare del Teorema degli zeri", "sono lo stesso enunciato con nomi diversi ma ipotesi diverse"])
    add(r"Il Teorema di Bolzano (valori intermedi) si può dimostrare a partire dal Teorema degli zeri:",
        "applicando il Teorema degli zeri alla funzione ausiliaria \\(g(x)=f(x)-y_0\\)",
        ["applicando il Teorema di Weierstrass a f", "applicando il Teorema di Lagrange a f", "non è possibile, richiede una dimostrazione indipendente"])
    add(r"Il Teorema degli zeri richiede \(f(a)\cdot f(b)<0\): questa condizione garantisce che:",
        "\\(f(a)\\) e \\(f(b)\\) hanno segno opposto",
        ["f è crescente su [a,b]", "f si annulla in a o in b", "f è positiva su tutto [a,b]"])
    add(r"Se nel Teorema degli zeri si ha solo \(f(a)\cdot f(b)\le 0\) (non stretta), cosa si può concludere?",
        "esiste comunque almeno uno zero in [a,b] (eventualmente proprio in a o b)",
        ["non esiste necessariamente alcuno zero", "esistono esattamente due zeri", "f deve essere costante"])

    # ---------------- Teorema di Fermat ----------------
    set_chapter(6)
    add(r"Il Teorema di Fermat afferma che se \(x_0\) è un punto di estremo relativo interno al dominio di \(f\) e \(f\) è derivabile in \(x_0\), allora:",
        "\\(f'(x_0)=0\\)", ["\\(f''(x_0)=0\\)", "\\(f(x_0)=0\\)", "\\(f\\) non è continua in \\(x_0\\)"])
    add(r"Il Teorema di Fermat richiede che il punto di estremo \(x_0\) sia:",
        "interno al dominio (non un estremo dell'intervallo)",
        ["un punto di massimo assoluto", "un punto in cui f è due volte derivabile", "un punto in cui f è continua ma non derivabile"])
    add(r"La condizione \(f'(x_0)=0\) fornita dal Teorema di Fermat è, per l'esistenza di un estremo relativo in \(x_0\):",
        "necessaria ma non sufficiente (es. \\(f(x)=x^3\\) in \\(x_0=0\\): \\(f'(0)=0\\) ma non è un estremo)",
        ["sufficiente ma non necessaria", "necessaria e sufficiente", "né necessaria né sufficiente"])
    for n in (3, 4, 5, 6):
        add((r"Sia \(A\subset\mathbb{R}\) un intervallo e \(n\ge %d\). Quali implicazioni sussistono tra le affermazioni: "
             r"a) f è derivabile n volte in A; b) \(f^{(n-2)}\) è una funzione continua in A; c) f è una funzione continua in A?" % n),
            "a) ⇒ b) ⇒ c), e nessuna delle implicazioni inverse vale in generale",
            ["le tre affermazioni sono equivalenti", "solo a) ⇒ c), mentre b) è indipendente dalle altre due", "nessuna delle tre implica le altre"])

    # ---------------- Teorema di Lagrange ----------------
    add(r"Il Teorema di Lagrange (valor medio) afferma che se \(f\) è continua su \([a,b]\) e derivabile su \((a,b)\), allora esiste \(c\in(a,b)\) tale che:",
        r"\( f'(c) = \dfrac{f(b)-f(a)}{b-a} \)",
        [r"\( f'(c) = f(b)-f(a) \)", r"\( f(c) = \dfrac{f(b)-f(a)}{b-a} \)", r"\( f'(c) = 0 \)"])
    add(r"Il Teorema di Rolle è il caso particolare del Teorema di Lagrange in cui:",
        "\\(f(a)=f(b)\\), e la tesi diventa \\(f'(c)=0\\) per qualche \\(c\\in(a,b)\\)",
        ["f è derivabile due volte", "a=b", "f è monotona"])
    add(r"Nella dimostrazione del Teorema di Lagrange si applica il Teorema di Rolle alla funzione ausiliaria:",
        r"\( h(x) = f(x) - f(a) - \dfrac{f(b)-f(a)}{b-a}(x-a) \)",
        [r"\( h(x) = f(x) - f(a) \)", r"\( h(x) = f(x) \cdot (x-a) \)", r"\( h(x) = f'(x) - \dfrac{f(b)-f(a)}{b-a} \)"])
    add(r"Geometricamente, il Teorema di Lagrange afferma che esiste un punto del grafico di f in cui la retta tangente è:",
        "parallela alla retta secante che congiunge (a,f(a)) e (b,f(b))",
        ["perpendicolare all'asse x", "tangente all'asse x", "parallela all'asse y"])
    add(r"Ipotesi del Teorema di Lagrange su \([a,b]\):",
        "f continua su [a,b] e derivabile su (a,b)",
        ["f derivabile su [a,b] incluso gli estremi", "f continua su (a,b) soltanto", "f due volte derivabile su [a,b]"])

    # ---------------- Teorema di unicità del limite ----------------
    set_chapter(4)
    add(r"Il Teorema di unicità del limite afferma che se \(\lim_{x\to x_0} f(x)\) esiste, allora:",
        "tale limite è unico (non possono esistere due limiti distinti per la stessa funzione nello stesso punto)",
        ["il limite deve essere finito", "f è continua in \\(x_0\\)", "f è definita in \\(x_0\\)"])
    add(r"La dimostrazione del Teorema di unicità del limite procede tipicamente:",
        "per assurdo: se \\(\\ell_1\\neq\\ell_2\\) fossero entrambi limite, si trovano intorni disgiunti che portano a una contraddizione",
        ["per induzione su n", "usando il Teorema di Weierstrass", "usando la formula di Taylor"])
    add(r"Il Teorema di unicità del limite vale:",
        "sia per limiti finiti che per limiti infiniti", ["solo per limiti finiti", "solo per limiti infiniti", "solo per funzioni continue"])

    # ---------------- Teorema Fondamentale del Calcolo ----------------
    set_chapter(7)
    add(r"Il Teorema Fondamentale del Calcolo afferma che se \(f\in C([a,b])\) e \(F(x)=\int_a^x f(t)\,dt\), allora:",
        "F è derivabile su [a,b] e \\(F'(x)=f(x)\\) per ogni \\(x\\)",
        ["F è costante su [a,b]", "F(x)=f(x) per ogni x", "F è derivabile solo se f è derivabile"])
    add(r"Per il Teorema Fondamentale del Calcolo, se \(g(x)\) è derivabile e \(F(x)=\int_a^{g(x)} f(t)\,dt\), allora \(F'(x)\) vale:",
        r"\( f(g(x))\cdot g'(x) \)", [r"\( f(g(x)) \)", r"\( f'(g(x))\cdot g'(x) \)", r"\( f(x)\cdot g'(x) \)"])
    add(r"Per \(F(x)=\int_{h(x)}^{g(x)} f(t)\,dt\) con f continua e g,h derivabili, la formula di Leibniz dà \(F'(x)=\)",
        r"\( f(g(x))g'(x) - f(h(x))h'(x) \)", [r"\( f(g(x))g'(x) + f(h(x))h'(x) \)", r"\( f(g(x)) - f(h(x)) \)", r"\( f'(g(x))g'(x) - f'(h(x))h'(x) \)"])
    add(r"Il Teorema Fondamentale del Calcolo collega:",
        "il calcolo integrale e il calcolo differenziale (l'integrazione è l'operazione inversa della derivazione)",
        ["il calcolo dei limiti e la continuità", "le successioni e le serie", "i numeri complessi e le equazioni algebriche"])

    # ---------------- Criteri di monotonia e convessità ----------------
    set_chapter(6)
    add(r"Il criterio di monotonia afferma che, per \(f\) derivabile su \((a,b)\): \(f'(x)\ge0\ \forall x\) se e solo se:",
        "f è crescente (non decrescente) su (a,b)",
        ["f è decrescente su (a,b)", "f è costante su (a,b)", "f è convessa su (a,b)"])
    add(r"Se \(f'(x)>0\) per ogni \(x\in(a,b)\), si può concludere che:",
        "f è strettamente crescente su (a,b)",
        ["f è strettamente decrescente su (a,b)", "f è convessa su (a,b)", "f ha un massimo relativo in (a,b)"])
    add(r"Il viceversa del criterio di monotonia (f strettamente crescente ⇒ \(f'(x)>0\) ovunque) è, in generale:",
        "falso: f può essere strettamente crescente con \\(f'(x_0)=0\\) in qualche punto (es. \\(f(x)=x^3\\) in \\(x_0=0\\))",
        ["vero senza eccezioni", "vero solo se f è un polinomio", "vero solo se f è invertibile"])
    add(r"Il criterio di convessità afferma che, per \(f\) due volte derivabile su \((a,b)\): f è convessa su (a,b) se e solo se:",
        "\\(f''(x)\\ge0\\) per ogni \\(x\\in(a,b)\\)",
        ["\\(f'(x)\\ge0\\) per ogni x", "\\(f''(x)\\le0\\) per ogni x", "\\(f(x)\\ge0\\) per ogni x"])
    add(r"Un punto \(x_0\) in cui la concavità di f cambia (da convessa a concava o viceversa) si chiama:",
        "punto di flesso", ["punto stazionario", "punto angoloso", "punto di discontinuità"])
    add(r"Nel criterio di convessità, se \(f''(x_0)=0\) in un singolo punto \(x_0\), si può concludere che:",
        "nulla in generale: occorre studiare il segno di \\(f''\\) attorno a \\(x_0\\) (potrebbe essere un flesso oppure no)",
        ["x0 è sicuramente un flesso", "f non è convessa in nessun intorno di x0", "f'(x0)=0 necessariamente"])

    return items


def build():
    """Compatibilità: restituisce la lista piatta (senza il campo chapter)
    nello stesso formato {text, correct, wrong} usato dagli altri bank/*.py."""
    return [{"text": it["text"], "correct": it["correct"], "wrong": it["wrong"]} for it in build_tagged()]


if __name__ == "__main__":
    items = build_tagged()
    print("Totale domande teoremi stile esame:", len(items))
    per_ch = {}
    for it in items:
        per_ch[it["chapter"]] = per_ch.get(it["chapter"], 0) + 1
    print("Per capitolo:", per_ch)
    bad = 0
    for it in items:
        opts = [it["correct"]] + it["wrong"]
        if len(set(opts)) != 4:
            bad += 1
            print("PROBLEMA:", it["text"])
    print("Domande con problemi:", bad)
