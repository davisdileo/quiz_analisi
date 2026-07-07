# -*- coding: utf-8 -*-
"""Capitolo 5 - Funzioni continue: generazione verificata con sympy."""
import random
import sympy as sp

x = sp.symbols('x')


def wrap(s):
    return f"\\({s}\\)"


def coef_x(n, var="x"):
    if n == 1:
        return var
    if n == -1:
        return f"-{var}"
    return f"{n}{var}"


def lin_expr(a, b, var="x"):
    """a*var + b, formattato in modo pulito: niente '0x', '1x' o '+0'."""
    parts = []
    if a != 0:
        parts.append(coef_x(a, var))
    if b > 0:
        parts.append(f"+ {b}" if parts else f"{b}")
    elif b < 0:
        parts.append(f"- {-b}" if parts else f"-{-b}")
    if not parts:
        return "0"
    return " ".join(parts)


def num_distractors(correct_val, extra=()):
    cv = sp.nsimplify(correct_val)
    cands = list(extra) + [-cv, cv * 2, cv + 1, cv - 1, sp.Integer(0), cv / 2]
    out, seen = [], {sp.latex(cv)}
    for c in cands:
        cs = sp.latex(sp.nsimplify(c))
        if cs not in seen:
            out.append(cs)
            seen.add(cs)
        if len(out) == 3:
            break
    return out


def build():
    items = []
    seen_texts = set()

    def add(text, correct, wrong):
        if len(set([correct] + wrong)) != 4 or len(wrong) != 3:
            return False
        if text in seen_texts:
            return False
        seen_texts.add(text)
        items.append({"text": text, "correct": correct, "wrong": wrong})
        return True

    # ---- CT1: continuità con parametro, pezzi lineare/quadratico ----
    count = 0
    combos = [(m, q, c, p) for m in range(-4, 5) for q in range(-4, 5)
              for c in range(-3, 4) for p in [2] if m != 0]
    random.shuffle(combos)
    for m, q, c, p in combos:
        if count >= 10:
            break
        # f(x) = a*x + q  per x<=c ;  x^p + m*x  per x>c   (continua per un certo a)
        right_val_at_c = c ** p + m * c
        a_needed = sp.Rational(right_val_at_c - q, c) if c != 0 else None
        if c == 0 or a_needed is None or a_needed == 0:
            continue
        q_term = (f" + {q}" if q > 0 else (f" - {-q}" if q < 0 else ""))
        m_term = (f" + {coef_x(m)}" if m > 0 else (f" - {coef_x(-m)}" if m < 0 else ""))
        text = (r"Per quale valore del parametro \(a\) la funzione "
                r"\( f(x)=\begin{cases} ax%s & x \le %d \\ x^{%d}%s & x > %d \end{cases} \) "
                r"è continua su \( \mathbb{R} \)?") % (q_term, c, p, m_term, c)
        correct = wrap(sp.latex(a_needed))
        wrong = [wrap(w) for w in num_distractors(a_needed)]
        if add(text, correct, wrong):
            count += 1

    # ---- CT2: teorema degli zeri, esistenza/unicità soluzione ----
    count = 0
    funcs = []
    for k in range(-6, 7):
        if k == 0:
            continue
        funcs.append((sp.exp(x) + k * x, f"e^x {'+' if k>=0 else '-'} {abs(k)}x", True))  # f'=e^x+k, monotona se k>-1... verificare
        funcs.append((x ** 3 + k * x, f"x^3 {'+' if k>=0 else '-'} {abs(k)}x", None))
    random.shuffle(funcs)
    for expr, expr_s, _ in funcs:
        if count >= 10:
            break
        a_int, b_int = 0, 2
        expr_shift = expr - random.randint(1, 8)
        fa = expr_shift.subs(x, a_int)
        fb = expr_shift.subs(x, b_int)
        fa_val = float(fa.evalf())
        fb_val = float(fb.evalf())
        if fa_val * fb_val >= 0:
            continue
        deriv = sp.diff(expr_shift, x)
        # verifica monotonia stretta su [a_int,b_int] campionando alcuni punti
        is_monotone = all(float(deriv.subs(x, t).evalf()) > 0 for t in
                           [a_int + i * (b_int - a_int) / 10 for i in range(11)])
        if not is_monotone:
            continue
        const = -(expr - expr_shift)  # il termine costante sottratto, con segno per la stampa
        c_val = int(sp.nsimplify(expr - expr_shift))
        text = (r"Sia \( f(x) = %s - %d \) su \( [%d,%d] \). Cosa si può concludere sull'equazione \(f(x)=0\)?"
                % (expr_s, c_val, a_int, b_int))
        correct = ("poiché \\(f\\) è continua, cambia segno agli estremi ed è strettamente monotona su "
                   "\\([%d,%d]\\), esiste un'unica soluzione in \\((%d,%d)\\)" % (a_int, b_int, a_int, b_int))
        wrong = [
            "non esiste alcuna soluzione nell'intervallo",
            "esistono infinite soluzioni nell'intervallo",
            "esistono esattamente due soluzioni nell'intervallo",
        ]
        if add(text, correct, wrong):
            count += 1

    # ---- CT4: classificazione discontinuità con parametro (salto finito) ----
    count = 0
    combos = [(m1, q1, m2, q2, c) for m1 in range(-4, 5) for q1 in range(-4, 5)
              for m2 in range(-4, 5) for q2 in range(-4, 5) for c in range(-3, 4)]
    random.shuffle(combos)
    for m1, q1, m2, q2, c in combos:
        if count >= 10:
            break
        left_val = m1 * c + q1
        right_val = m2 * c + q2
        if left_val == right_val:
            continue  # vogliamo un salto, non continuità
        jump = abs(right_val - left_val)
        text = (r"Sia \( f(x)=\begin{cases} %s & x \le %d \\ %s & x > %d \end{cases} \). "
                r"Classificare la discontinuità di \(f\) in \(x=%d\).") % (
            lin_expr(m1, q1), c, lin_expr(m2, q2), c, c)
        correct = f"discontinuità di prima specie (salto finito di ampiezza {jump})"
        wrong = [
            "discontinuità eliminabile",
            "discontinuità di seconda specie",
            f"\\(f\\) è continua in \\(x={c}\\)",
        ]
        if add(text, correct, wrong):
            count += 1

    # ---- CT5: discontinuità eliminabile (buco), con parametro ----
    count = 0
    for k in random.sample([n for n in range(-9, 10) if n != 0], 8):
        # f(x) = (x^2 - k^2)/(x-k) per x != k, con f(k)=v ; il limite per x->k vale 2k
        limit_val = 2 * k
        v = limit_val + random.choice([1, -1, 2, -2])
        text = (r"Sia \( f(x) = \dfrac{x^2 - %d}{x-%d} \) per \(x \neq %d\), con \(f(%d) = %d\). "
                r"La funzione \(f\) in \(x=%d\) è:") % (k ** 2, k, k, k, v, k)
        correct = (f"discontinua con discontinuità eliminabile (il limite per \\(x\\to {k}\\) vale "
                   f"{limit_val}, diverso da \\(f({k})={v}\\))")
        wrong = [
            f"continua, perché il limite coincide con \\(f({k})\\)",
            "discontinua con discontinuità di prima specie",
            "discontinua con discontinuità di seconda specie",
        ]
        if add(text, correct, wrong):
            count += 1

    # ---- CT6: teoria (enumerate) ----
    theory = [
        (r"Il teorema di Weierstrass afferma che una funzione continua su un intervallo chiuso e limitato \([a,b]\):",
         "ammette massimo e minimo assoluti", ["è sempre derivabile", "è sempre monotona", "ha infiniti punti di discontinuità"]),
        (r"La funzione \( f(x) = \tan x \) sull'intervallo \( \left(-\pi/2, \pi/2\right) \):",
         "non ammette massimo né minimo assoluti, perché l'intervallo non è chiuso e \\(f\\) è illimitata",
         ["ammette massimo e minimo per Weierstrass", "è limitata", "è periodica su questo intervallo"]),
        (r"Una funzione continua su un intervallo \((a,b)\) aperto:",
         "non è detto che ammetta massimo o minimo assoluti (Weierstrass richiede un intervallo chiuso e limitato)",
         ["ammette sempre massimo e minimo", "non può essere limitata", "è sempre derivabile"]),
        (r"Se \(f\) è continua su \([a,b]\) e \(f(a) \cdot f(b) < 0\), il teorema degli zeri garantisce:",
         "l'esistenza di almeno uno zero di \\(f\\) in \\((a,b)\\)", ["l'unicità dello zero", "che \\(f\\) sia monotona", "che \\(f\\) sia derivabile"]),
        (r"Il teorema dei valori intermedi afferma che una funzione continua su \([a,b]\):",
         "assume tutti i valori compresi tra \\(f(a)\\) e \\(f(b)\\)",
         ["assume solo i valori \\(f(a)\\) e \\(f(b)\\)", "è sempre crescente", "non può annullarsi"]),
        (r"La funzione \( f(x) = \dfrac{\sin x}{x} \) per \(x \neq 0\), prolungata con \(f(0)=1\), in \(x=0\) è:",
         "continua, perché \\(\\lim_{x\\to0}\\sin x / x = 1 = f(0)\\)", ["discontinua eliminabile", "discontinua di prima specie", "discontinua di seconda specie"]),
        (r"Una funzione con un asintoto verticale in \(x_0\) presenta in \(x_0\) una discontinuità:",
         "di seconda specie", ["di prima specie", "eliminabile", "non è una discontinuità"]),
        (r"Se \(f\) e \(g\) sono continue in \(x_0\), allora \(f+g\) e \(f \cdot g\) in \(x_0\):",
         "sono anch'esse continue in \\(x_0\\)", ["non sono necessariamente continue", "sono sempre derivabili", "sono sempre limitate"]),
        (r"La composizione \(g \circ f\) di due funzioni continue (con \(f\) continua in \(x_0\) e \(g\) continua in \(f(x_0)\)) è:",
         "continua in \\(x_0\\)", ["discontinua in generale", "continua solo se \\(f=g\\)", "derivabile in \\(x_0\\)"]),
        (r"Una funzione monotona su un intervallo può avere al più discontinuità:",
         "di prima specie (salto)", ["di seconda specie", "eliminabili", "non può avere discontinuità"]),
    ]
    for text, correct, wrong in theory:
        add(text, correct, wrong)

    return items


if __name__ == "__main__":
    random.seed(505)
    items = build()
    print("Totale domande generate (Capitolo 5):", len(items))
    bad = 0
    for it in items:
        opts = [it["correct"]] + it["wrong"]
        if len(set(opts)) != 4:
            bad += 1
            print("PROBLEMA:", it["text"], opts)
    print("Domande con problemi:", bad)
