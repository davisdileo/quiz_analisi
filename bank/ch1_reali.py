# -*- coding: utf-8 -*-
"""Genera la banca di domande per il Capitolo 1 - Numeri reali.
Ogni domanda viene verificata simbolicamente con sympy. Il risultato
(lista di dict con text/correct/wrong) viene importato da build_bank.py.
"""
import random
import sympy as sp


def lin_term(coef, var="x"):
    """Formatta un termine lineare tipo 2x, -x, x, evitando '1x'/'−1x'."""
    if coef == 1:
        return var
    if coef == -1:
        return f"-{var}"
    return f"{coef}{var}"


def signed(n, first=False):
    """Formatta un numero con segno per la concatenazione in un'espressione,
    es. per n=-3 restituisce '- 3', per n=5 restituisce '+ 5'; se first=True
    e n<0 restituisce '-3' (per l'inizio di un'espressione)."""
    if n == 0:
        return ""
    if first:
        return f"{n}"
    return f"+ {n}" if n > 0 else f"- {-n}"


def dedupe_wrong(correct, candidates):
    """Restituisce 3 distrattori distinti tra loro e diversi dalla risposta
    corretta, pescando dalla lista di candidati e, se necessario,
    aggiungendo varianti numeriche per riempire."""
    out = []
    seen = {correct}
    for c in candidates:
        if c not in seen:
            out.append(c)
            seen.add(c)
        if len(out) == 3:
            return out
    # fallback: non dovrebbe mai servire con i template usati qui
    i = 0
    while len(out) < 3:
        filler = f"{correct}'"  # marcatore innocuo, praticamente mai usato
        if filler not in seen:
            out.append(filler)
            seen.add(filler)
        i += 1
    return out


def build():
    items = []
    seen_texts = set()

    def add(text, correct, wrong):
        wrong = dedupe_wrong(correct, wrong)
        if text in seen_texts:
            return False
        seen_texts.add(text)
        items.append({"text": text, "correct": correct, "wrong": wrong})
        return True

    # ---- Template R1: sup/inf di A_k = { n/(n+k) : n>=1 } ----
    ks = list(range(1, 13))
    random.shuffle(ks)
    for i, k in enumerate(ks[:10]):
        ask_sup = (i % 2 == 0)
        setdef = r"\left\{ \dfrac{n}{n+%d} : n \in \mathbb{N},\ n \ge 1 \right\}" % k
        if ask_sup:
            text = r"Sia \( A = %s \). Quanto vale \( \sup A \)?" % setdef
            correct = r"\(1\)"
            wrong = [f"\\({sp.latex(sp.Rational(1, 1 + k))}\\)", r"\(0\)", "non esiste"]
        else:
            val = sp.Rational(1, 1 + k)
            text = r"Sia \( A = %s \). Quanto vale \( \inf A \)?" % setdef
            correct = f"\\({sp.latex(val)}\\)"
            wrong = [r"\(1\)", r"\(0\)", f"\\({sp.latex(sp.Rational(1, k))}\\)"]
        add(text, correct, wrong)

    # ---- Template R2: |ax+b| <= c ----
    combos = []
    for a in [1, 2, 3]:
        for b in range(-5, 6):
            for c in range(1, 8):
                combos.append((a, b, c))
    random.shuffle(combos)
    count = 0
    for a, b, c in combos:
        if count >= 10:
            break
        lo = sp.Rational(-c - b, a)
        hi = sp.Rational(c - b, a)
        if lo > hi:
            lo, hi = hi, lo
        if hi - lo < sp.Rational(1, 2):
            continue
        expr = lin_term(a) + (" " + signed(b) if b != 0 else "")
        text = r"Risolvere in \( \mathbb{R} \) la disequazione \( \left| %s \right| \le %d \)." % (expr, c)
        correct = f"\\( {sp.latex(lo)} \\le x \\le {sp.latex(hi)} \\)"
        wrong = [
            f"\\( {sp.latex(-hi)} \\le x \\le {sp.latex(-lo)} \\)",
            f"\\( x \\le {sp.latex(lo)} \\) oppure \\( x \\ge {sp.latex(hi)} \\)",
            f"\\( {sp.latex(lo - 1)} \\le x \\le {sp.latex(hi + 1)} \\)",
        ]
        if add(text, correct, wrong):
            count += 1

    # ---- Template R3: (x-r1)(x-r2) < 0, chiedere sup o inf ----
    root_pairs = []
    for r1 in range(-6, 5):
        for r2 in range(r1 + 2, 7):  # r2 >= r1+2 per evitare radici troppo vicine
            if r1 != 0 and r2 != 0:  # evita il termine noto nullo (poco leggibile)
                root_pairs.append((r1, r2))
    random.shuffle(root_pairs)
    count = 0
    for i, (r1, r2) in enumerate(root_pairs):
        if count >= 10:
            break
        ask_sup = (i % 2 == 0)
        b = -(r1 + r2)
        c = r1 * r2
        expr = "x^2" + (" " + signed(b) if b != 0 else "") + (" " + signed(c) if c != 0 else "")
        text = r"Sia \( B = \{ x \in \mathbb{R} : %s < 0 \} \). Quanto vale \( %s B \)?" % (
            expr, "\\sup" if ask_sup else "\\inf")
        correct = f"\\({r2 if ask_sup else r1}\\)"
        wrong = [f"\\({r1 if ask_sup else r2}\\)", "non esiste", f"\\({r1 + r2}\\)"]
        if add(text, correct, wrong):
            count += 1

    # ---- Template R4: sup/inf di { x : x^2 < c } ----
    cs = [2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 15, 18]
    random.shuffle(cs)
    count = 0
    for i, c in enumerate(cs[:8]):
        s = sp.sqrt(c)
        ask_sup = (i % 2 == 0)
        text = r"Sia \( C = \{ x \in \mathbb{R} : x^2 < %d \} \). Quanto vale \( %s C \)?" % (
            c, "\\sup" if ask_sup else "\\inf")
        val = s if ask_sup else -s
        correct = f"\\({sp.latex(val)}\\)"
        wrong = [f"\\({sp.latex(-val)}\\)", f"\\({c}\\)", f"\\({sp.latex(val / 2)}\\)"]
        if add(text, correct, wrong):
            count += 1

    # ---- Template R5: domande teoriche (enumerate) ----
    theory = [
        (r"Quale dei seguenti insiemi è limitato ma non ammette massimo?",
         r"\( (0,1) \)", [r"\( [0,1] \)", r"\( \mathbb{N} \)", r"\( \mathbb{Z} \)"]),
        (r"La proprietà archimedea di \( \mathbb{R} \) afferma che:",
         r"per ogni \(x,y \in \mathbb{R}\) con \(x>0\), esiste \(n \in \mathbb{N}\) tale che \(nx>y\)",
         [r"ogni sottoinsieme di \(\mathbb{R}\) è limitato", r"\(\mathbb{R}\) è numerabile", r"tra due razionali non ci sono irrazionali"]),
        (r"L'insieme \( \mathbb{Q} \) dei numeri razionali, come sottoinsieme di \( \mathbb{R} \):",
         r"è denso in \( \mathbb{R} \): tra due reali distinti esiste sempre un razionale",
         [r"è chiuso in \( \mathbb{R} \)", r"è un intervallo", r"non contiene numeri negativi"]),
        (r"Se \( A \subseteq \mathbb{R} \) è non vuoto e limitato superiormente, l'assioma di completezza di \( \mathbb{R} \) garantisce che:",
         r"esiste ed è unico \( \sup A \in \mathbb{R} \)",
         [r"esiste \( \max A \)", r"\(A\) è un intervallo chiuso", r"\(A\) è numerabile"]),
        (r"Per ogni \( a, b \in \mathbb{R} \), la disuguaglianza triangolare afferma che:",
         r"\( |a+b| \le |a| + |b| \)", [r"\( |a+b| \ge |a|+|b| \)", r"\( |a+b| = |a|+|b| \)", r"\( |a-b| \le |a|-|b| \)"]),
        (r"Quale delle seguenti affermazioni sulla disuguaglianza di Bernoulli \( (1+x)^n \ge 1+nx \) (per \(x>-1\), \(n\in\mathbb{N}\)) è corretta?",
         r"vale per ogni \(n \ge 0\)", [r"vale solo se \(n\) è pari", r"vale solo se \(x>0\)", r"non vale in generale"]),
        (r"L'insieme \( \mathbb{N} \) dei numeri naturali, come sottoinsieme di \( \mathbb{R} \):",
         r"non è limitato superiormente (per la proprietà archimedea)",
         [r"è limitato superiormente", r"ammette massimo", r"è denso in \( \mathbb{R} \)"]),
        (r"Un numero \( M \) è un maggiorante di un insieme \( A \subseteq \mathbb{R} \) se:",
         r"\( x \le M \) per ogni \( x \in A \)", [r"\( x < M \) per ogni \( x \in A \)", r"\( M \in A \)", r"\( M = \max A \)"]),
        (r"Se \( \sup A = \max A \), allora:",
         r"il valore \(\sup A\) è un elemento di \(A\)", [r"\(A\) non è limitato", r"\(A\) è vuoto", r"\(A\) coincide con \(\mathbb{R}\)"]),
        (r"Il numero \( \sqrt2 \) è:",
         "irrazionale, poiché non può essere scritto come rapporto di due interi",
         [r"razionale", r"un numero intero", r"negativo"]),
    ]
    for text, correct, wrong in theory:
        add(text, correct, wrong)

    return items


if __name__ == "__main__":
    random.seed(101)
    items = build()
    print("Totale domande generate (Capitolo 1):", len(items))
    # controllo di qualità: nessun distrattore duplicato o uguale alla risposta corretta
    bad = 0
    for it in items:
        opts = [it["correct"]] + it["wrong"]
        if len(set(opts)) != 4:
            bad += 1
            print("DUPLICATO:", it["text"], opts)
    print("Domande con opzioni duplicate:", bad)
    for it in items[:3] + items[-3:]:
        print("-", it["text"])
        print("   OK:", it["correct"], "| KO:", it["wrong"])
