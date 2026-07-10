# -*- coding: utf-8 -*-
"""Domande aggiuntive tratte direttamente dalle slide del corso caricate
dall'utente (Analisi Matematica - modulo A, classe B, Politecnico di Bari,
Rossella Bartolo, A.A. 2025-2026), per colmare argomenti non ancora coperti
dalla banca dati: punti angolosi/cuspidi/flessi a tangente verticale,
formula di Taylor, teorema della media integrale, primitive, assiomi di R,
principio di induzione, funzioni periodiche/limitate, criterio di
invertibilità.

Restituisce un dizionario {capitolo: [ {text, correct, wrong[3]}, ... ] }.
"""
import random
import sympy as sp

x = sp.symbols('x')


def wrap(s):
    return f"\\({s}\\)"


def make_list():
    out = []
    seen = set()

    def add(text, correct, wrong):
        if len(set([correct] + wrong)) != 4 or len(wrong) != 3:
            return False
        if text in seen:
            return False
        seen.add(text)
        out.append({"text": text, "correct": correct, "wrong": wrong})
        return True

    return out, add


def build():
    result = {1: [], 3: [], 5: [], 6: [], 7: []}

    # ================= Capitolo 6 - Calcolo differenziale =================
    items, add = make_list()

    add(r"Sia \( f(x) = |x| \). Che tipo di punto è \( x_0=0 \) per \(f\)?",
        "un punto angoloso (\\(f'_-(0)=-1\\), \\(f'_+(0)=1\\): entrambe finite ma diverse)",
        ["un flesso a tangente verticale", "una cuspide", "un punto di massimo relativo"])

    add(r"Sia \( f(x) = \sqrt[3]{x} \) (radice cubica). Che tipo di punto è \( x_0=0 \) per \(f\)?",
        "un flesso a tangente verticale (\\(f'(x)\\to+\\infty\\) da entrambi i lati)",
        ["un punto angoloso", "una cuspide", "un punto di minimo relativo"])

    add(r"Sia \( f(x) = \sqrt{|x|} \). Che tipo di punto è \( x_0=0 \) per \(f\)?",
        "una cuspide (\\(f'_+(0)=+\\infty\\), \\(f'_-(0)=-\\infty\\): infinite di segno opposto)",
        ["un punto angoloso", "un flesso a tangente verticale", "un punto di massimo relativo"])

    add(r"In un punto angoloso \(x_0\) per una funzione \(f\) continua in \(x_0\), le derivate laterali \(f'_-(x_0)\) e \(f'_+(x_0)\):",
        "esistono entrambe finite, ma sono diverse tra loro",
        ["sono entrambe infinite di segno opposto", "coincidono ed entrambe valgono \\(0\\)", "non esistono"])

    add(r"In una cuspide \(x_0\) per una funzione \(f\) continua in \(x_0\), le derivate laterali:",
        "sono entrambe infinite, di segno opposto (\\(f'_+(x_0)=\\pm\\infty\\), \\(f'_-(x_0)=\\mp\\infty\\))",
        ["sono entrambe finite ma diverse", "sono entrambe infinite dello stesso segno", "coincidono"])

    add(r"In un flesso a tangente verticale \(x_0\) per una funzione \(f\) continua in \(x_0\):",
        "\\(f'(x_0) \\in \\{+\\infty,-\\infty\\}\\) (la derivata è infinita, con lo stesso segno da entrambi i lati)",
        ["le derivate laterali sono finite ma diverse", "le derivate laterali sono infinite di segno opposto", "\\(f\\) non è continua in \\(x_0\\)"])

    add(r"Sia \(f(x)=x^{2}+3(x-1)+o(x-1)\) per \(x\to 1\) lo sviluppo di Taylor di ordine 1 di una funzione \(f\) in \(x_0=1\). Quanto vale \(f'(1)\)?",
        r"\(3\)", [r"\(1\)", r"\(2\)", r"\(0\)"])

    add(r"Il polinomio di Taylor di ordine \(n\) di \(f\) in \(x_0\), \( T_{n,x_0}f(x) = \displaystyle\sum_{k=0}^{n} \dfrac{f^{(k)}(x_0)}{k!}(x-x_0)^k \), verifica:",
        "\\(f(x) = T_{n,x_0}f(x) + o((x-x_0)^n)\\) per \\(x\\to x_0\\)",
        ["\\(f(x) = T_{n,x_0}f(x)\\) esattamente, per ogni \\(x\\)", "\\(T_{n,x_0}f(x_0) = 0\\)", "\\(T_{n,x_0}f\\) ha grado \\(n+1\\)"])

    add(r"Il differenziale di \(f\) relativo al punto \(x_0\), \(df(x_0)\), è la funzione affine:",
        "\\(df(x_0): x \\mapsto f'(x_0)(x-x_0)\\)",
        ["\\(df(x_0): x \\mapsto f(x_0)+f'(x_0)\\)", "\\(df(x_0): x \\mapsto f(x)-f(x_0)\\)", "\\(df(x_0): x \\mapsto f'(x)\\)"])

    add(r"Il Teorema di Fermat afferma che se \(x_0\) è un punto di estremo relativo interno al dominio e \(f\) è derivabile in \(x_0\), allora:",
        "\\(f'(x_0) = 0\\)",
        ["\\(f''(x_0) = 0\\)", "\\(f(x_0) = 0\\)", "\\(f\\) non è derivabile in \\(x_0\\)"])

    add(r"Un punto \(x_0\) con \(f'(x_0)=0\) si dice punto stazionario o critico. La condizione \(f'(x_0)=0\) per avere un estremo relativo in \(x_0\) è:",
        "necessaria ma non sufficiente (es. \\(f(x)=x^3\\), \\(x_0=0\\): \\(f'(0)=0\\) ma non è un estremo)",
        ["sufficiente ma non necessaria", "necessaria e sufficiente", "né necessaria né sufficiente"])

    add(r"Il Criterio di monotonia afferma che, per \(f\) continua su \([a,b]\) e derivabile in \((a,b)\): \(f'(x)\ge 0\) per ogni \(x\in(a,b)\) se e solo se:",
        "\\(f\\) è crescente in \\([a,b]\\)", ["\\(f\\) è decrescente in \\([a,b]\\)", "\\(f\\) è costante in \\([a,b]\\)", "\\(f\\) è convessa in \\([a,b]\\)"])

    add(r"Lo sviluppo di Taylor di \(e^x\) in \(x_0=0\) è \(e^x = 1+x+\dfrac{x^2}{2}+\ldots+\dfrac{x^n}{n!}+o(x^n)\). Il coefficiente di \(x^3\) vale:",
        r"\(1/6\)", [r"\(1/3\)", r"\(1/2\)", r"\(1\)"])

    add(r"Lo sviluppo di Taylor di \(\sin x\) in \(x_0=0\) è \(\sin x = x - \dfrac{x^3}{6} + \dfrac{x^5}{120} - \ldots\). Quale delle seguenti affermazioni è corretta?",
        "compaiono solo le potenze dispari di \\(x\\), coerentemente col fatto che \\(\\sin\\) è una funzione dispari",
        ["compaiono solo le potenze pari di \\(x\\)", "tutti i coefficienti sono positivi", "lo sviluppo coincide con quello di \\(\\cos x\\)"])

    result[6] = items

    # ================= Capitolo 7 - Calcolo integrale =================
    items, add = make_list()

    add(r"Il Teorema della media (integrale) afferma che se \(f \in C([a,b])\), allora esiste \(x_0\in[a,b]\) tale che:",
        r"\( \displaystyle\int_a^b f(x)\,dx = f(x_0)(b-a) \)",
        [r"\( \displaystyle\int_a^b f(x)\,dx = f(a)(b-a) \)", r"\( \displaystyle\int_a^b f(x)\,dx = 0 \)",
         r"\( f(x_0) = \displaystyle\int_a^b f(x)\,dx \)"])

    add(r"Applicando il teorema della media a \(f(x)=x^2\) su \([0,3]\), un punto \(x_0\) la cui esistenza è garantita dal teorema è:",
        r"\( x_0 = \sqrt{3} \)", [r"\(x_0=3\)", r"\(x_0=0\)", r"\(x_0=\sqrt{6}\)"])

    add(r"\(F\) si dice primitiva di \(f\) su un intervallo \(I\) se:",
        "\\(F\\) è derivabile su \\(I\\) e \\(F'(x)=f(x)\\) per ogni \\(x\\in I\\)",
        ["\\(F(x) = \\displaystyle\\int f(x)\\,dx\\) per un solo punto \\(x\\)", "\\(F\\) è continua e \\(F(x) \\ge f(x)\\)", "\\(f\\) è derivabile e \\(f'(x)=F(x)\\)"])

    add(r"Se \(F\) e \(G\) sono entrambe primitive di \(f\) su un intervallo \(I\), allora (caratterizzazione delle primitive):",
        "esiste \\(c\\in\\mathbb{R}\\) tale che \\(G(x) = F(x)+c\\) per ogni \\(x\\in I\\)",
        ["\\(F(x) = G(x)\\) per ogni \\(x\\in I\\)", "\\(F\\) e \\(G\\) differiscono per una funzione non costante", "\\(F\\cdot G\\) è costante"])

    add(r"Il Teorema di esistenza delle primitive afferma che se \(f \in C(I)\) e \(a\in I\), la funzione integrale \(F(x)=\displaystyle\int_a^x f(t)\,dt\):",
        "è derivabile su \\(I\\) e \\(F'(x)=f(x)\\) per ogni \\(x\\in I\\)",
        ["è derivabile solo nei punti in cui \\(f\\) è positiva", "non è mai derivabile", "è costante su \\(I\\)"])

    add(r"Per la proprietà di linearità dell'integrale, \(\displaystyle\int (3x^2+2\sin x)\,dx\) è uguale a:",
        r"\( 3\displaystyle\int x^2\,dx + 2\displaystyle\int \sin x\,dx \)",
        [r"\( 3\displaystyle\int x^2\,dx \cdot 2\displaystyle\int \sin x\,dx \)",
         r"\( \displaystyle\int x^2\,dx + \displaystyle\int \sin x\,dx \)",
         r"\( 6\displaystyle\int x^2 \sin x\,dx \)"])

    result[7] = items

    # ================= Capitolo 1 - Numeri reali =================
    items, add = make_list()

    add(r"L'Assioma di completezza di \(\mathbb{R}\) afferma che se \(A,B\subseteq\mathbb{R}\) sono non vuoti e \(a\le b\) per ogni \(a\in A\), \(b\in B\), allora:",
        "esiste \\(c\\in\\mathbb{R}\\) (elemento separatore) tale che \\(a\\le c\\le b\\) per ogni \\(a\\in A,\\ b\\in B\\)",
        ["\\(A=B\\)", "\\(A\\cap B \\neq \\emptyset\\)", "esiste \\(c\\in A\\cap B\\)"])

    add(r"La proprietà archimedea di \(\mathbb{N}\) implica che, per ogni \(x\in\mathbb{R}\):",
        "esiste \\(n\\in\\mathbb{N}\\) tale che \\(n>x\\)",
        ["esiste al più un \\(n\\in\\mathbb{N}\\) tale che \\(n<x\\)", "\\(x\\in\\mathbb{N}\\)", "\\(\\mathbb{N}\\) è limitato superiormente"])

    add(r"Per la densità di \(\mathbb{Q}\) e di \(\mathbb{R}\setminus\mathbb{Q}\) in \(\mathbb{R}\), per ogni \(a,b\in\mathbb{R}\) con \(a<b\):",
        "esistono sia un razionale \\(q\\) sia un irrazionale \\(w\\) tali che \\(a<q<b\\) e \\(a<w<b\\)",
        ["esiste solo un razionale compreso tra \\(a\\) e \\(b\\)", "non esistono numeri irrazionali tra \\(a\\) e \\(b\\)", "\\(a\\) e \\(b\\) devono essere entrambi razionali"])

    add(r"Il principio di induzione afferma che, data \(P(n)\) proposizione dipendente da \(n\in\mathbb{N}\), se \(P(1)\) è vera e per ogni \(n\), \(P(n)\Rightarrow P(n+1)\), allora:",
        "\\(P(n)\\) è vera per ogni \\(n\\in\\mathbb{N}\\)",
        ["\\(P(n)\\) è vera solo per \\(n=1\\)", "\\(P(n)\\) è vera per infiniti \\(n\\), ma non per tutti", "occorre verificare anche \\(P(2)\\)"])

    add(r"Ogni sottoinsieme non vuoto di \(\mathbb{N}\) è dotato di:",
        "minimo", ["massimo", "estremo superiore finito", "un solo elemento"])

    add(r"L'insieme \(A=\{a\in\mathbb{Q}: a>0,\ a^2<2\}\) ammette estremo superiore in \(\mathbb{Q}\)?",
        "No: \\(\\sup A = \\sqrt2\\), che non è un numero razionale (questo mostra che \\(\\mathbb{Q}\\) non verifica l'assioma di completezza)",
        ["Sì, \\(\\sup A = 2\\)", "Sì, \\(\\sup A = 1\\)", "No, perché \\(A\\) è vuoto"])

    result[1] = items

    # ================= Capitolo 3 - Funzioni reali =================
    items, add = make_list()

    add(r"Una funzione \(f: X\to\mathbb{R}\) si dice periodica di periodo \(T>0\) se \(x\in X \Rightarrow x\pm T\in X\) e:",
        "\\(f(x) = f(x\\pm T)\\) per ogni \\(x\\in X\\)",
        ["\\(f(x) = f(x)+T\\) per ogni \\(x\\in X\\)", "\\(f(T) = 0\\)", "\\(f\\) è invertibile"])

    add(r"Il periodo minimo (fondamentale) della funzione \(f(x)=\sin(2x)\) è:",
        r"\(\pi\)", [r"\(2\pi\)", r"\(\pi/2\)", r"\(4\pi\)"])

    add(r"Il periodo minimo della funzione \(f(x) = \cos(3x)\) è:",
        r"\(2\pi/3\)", [r"\(2\pi\)", r"\(3\pi\)", r"\(\pi/3\)"])

    add(r"Una funzione \(f: X\to\mathbb{R}\) si dice limitata se:",
        "\\(f(X)\\) è un insieme limitato (superiormente e inferiormente)",
        ["\\(X\\) è un insieme limitato", "\\(f\\) è continua", "\\(f\\) ammette massimo e minimo"])

    add(r"La funzione \(f(x)=\arctan x\) su \(\mathbb{R}\) è limitata; quanto valgono \(\sup_{\mathbb{R}} f\) e \(\inf_{\mathbb{R}} f\)?",
        "\\(\\sup_{\\mathbb{R}} f = \\pi/2\\), \\(\\inf_{\\mathbb{R}} f = -\\pi/2\\) (nessuno dei due è raggiunto)",
        ["\\(\\sup_{\\mathbb{R}} f = 1\\), \\(\\inf_{\\mathbb{R}} f = -1\\)", "\\(\\sup_{\\mathbb{R}} f = +\\infty\\), \\(\\inf_{\\mathbb{R}} f = -\\infty\\)", "\\(\\sup_{\\mathbb{R}} f = \\pi\\), \\(\\inf_{\\mathbb{R}} f = 0\\)"])

    result[3] = items

    # ================= Capitolo 5 - Funzioni continue =================
    items, add = make_list()

    add(r"Il Criterio di invertibilità afferma che, per \(f\in C([a,b])\): \(f\) è invertibile se e solo se:",
        "\\(f\\) è strettamente monotòna su \\([a,b]\\) (e in tal caso \\(f^{-1}\\) è continua e strettamente monotòna)",
        ["\\(f\\) è limitata", "\\(f\\) è derivabile su \\([a,b]\\)", "\\(f(a) = f(b)\\)"])

    add(r"Il Teorema di Bolzano (dei valori intermedi) afferma che se \(f\in C(I)\), con \(I\) intervallo, allora \(f(I)\):",
        "è un intervallo",
        ["è un insieme finito", "coincide con \\(I\\)", "è un insieme limitato ma non necessariamente un intervallo"])

    add(r"Per il Teorema di Bolzano, se \(f\in C([a,b])\), allora \(f\) assume:",
        "tutti i valori compresi tra il minimo e il massimo di \\(f\\) su \\([a,b]\\)",
        ["solo i valori \\(f(a)\\) e \\(f(b)\\)", "solo valori positivi", "un unico valore costante"])

    add(r"Il Teorema di Weierstrass, nella formulazione generale, afferma che se \(X\subseteq\mathbb{R}\) è compatto e \(f\in C(X)\), allora:",
        "\\(f\\) ammette massimo e minimo assoluti su \\(X\\)",
        ["\\(f\\) è monotòna su \\(X\\)", "\\(f\\) è derivabile su \\(X\\)", "\\(X\\) è un intervallo aperto"])

    result[5] = items

    return result


if __name__ == "__main__":
    result = build()
    total = 0
    for ch, items in result.items():
        print(f"Capitolo {ch}: {len(items)} domande")
        total += len(items)
        bad = 0
        for it in items:
            opts = [it["correct"]] + it["wrong"]
            if len(set(opts)) != 4:
                bad += 1
                print("  PROBLEMA:", it["text"])
        if bad:
            print(f"  -> {bad} domande con opzioni duplicate")
    print("Totale:", total)
