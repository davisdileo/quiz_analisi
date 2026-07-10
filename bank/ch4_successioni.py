# -*- coding: utf-8 -*-
"""Domande su Successioni numeriche (dalle slide del corso, cap. 3 'Limiti di
funzioni' -> capitolo interno 4 'Limiti'). Verificate con sympy dove
applicabile.
"""
import random
import sympy as sp

n = sp.symbols('n', positive=True)


def wrap(s):
    return f"\\({s}\\)"


def coef_n(c):
    if c == 1:
        return "n"
    if c == -1:
        return "-n"
    return f"{c}n"


def num_distractors(correct_val, extra=()):
    cv = sp.nsimplify(correct_val)
    cands = list(extra) + [-cv, cv * 2, cv + 1, cv - 1, cv / 2, sp.Integer(0)]
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

    # ---- SU1: lim di successioni razionali a_n = P(n)/Q(n) ----
    count = 0
    for _ in range(40):
        if count >= 5:
            break
        deg = random.choice([2, 3])
        a_lead = random.choice([k for k in range(-6, 7) if k != 0])
        b_lead = random.choice([k for k in range(-6, 7) if k != 0])
        same_degree = random.choice([True, False])
        num = a_lead * n ** deg + random.randint(-5, 5) * n + random.randint(-5, 5)
        den_deg = deg if same_degree else deg + random.choice([1, -1])
        if den_deg < 1:
            den_deg = deg + 1
        den = b_lead * n ** den_deg + random.randint(-5, 5) * n + random.randint(-5, 5)
        expr = num / den
        val = sp.limit(expr, n, sp.oo)
        num_s = sp.latex(sp.expand(num))
        den_s = sp.latex(sp.expand(den))
        text = r"Sia \( a_n = \dfrac{%s}{%s} \). Calcolare \( \displaystyle\lim_{n\to +\infty} a_n \)." % (num_s, den_s)
        if val in (sp.oo, -sp.oo):
            correct = wrap("+\\infty" if val == sp.oo else "-\\infty")
            wrong = [wrap("-\\infty" if val == sp.oo else "+\\infty"), wrap("0"), wrap(sp.latex(sp.Rational(a_lead, b_lead)))]
        else:
            correct = wrap(sp.latex(val))
            wrong = [wrap(w) for w in num_distractors(val)]
        if add(text, correct, wrong):
            count += 1

    # ---- SU2: lim a^n al variare di a (dalla tabella di pagina 157) ----
    cases = [
        (sp.Rational(3, 2), "+\\infty"), (2, "+\\infty"), (5, "+\\infty"), (3, "+\\infty"),
        (1, "1"),
        (sp.Rational(1, 2), "0"), (sp.Rational(-1, 3), "0"), (sp.Rational(2, 3), "0"), (sp.Rational(-1, 2), "0"),
        (-1, "\\text{non esiste}"), (-2, "\\text{non esiste}"), (-3, "\\text{non esiste}"),
    ]
    random.shuffle(cases)
    for a, res in cases[:7]:
        a = sp.sympify(a)
        a_latex = sp.latex(a) if (a.is_Integer and a >= 0) else f"\\left({sp.latex(a)}\\right)"
        text = r"Sia \( a_n = %s^n \). Quanto vale \( \displaystyle\lim_{n\to+\infty} a_n \)?" % a_latex
        correct = wrap(res)
        pool = ["+\\infty", "0", "1", "\\text{non esiste}", "-\\infty"]
        wrong = [wrap(w) for w in pool if w != res][:3]
        add(text, correct, wrong)

    # ---- SU3: il numero di Nepero, lim (1+k/n)^n = e^k ----
    for k in random.sample([j for j in range(-5, 6) if j != 0] + [1], 6):
        expr = (1 + sp.Rational(k) / n) ** n
        val = sp.limit(expr, n, sp.oo)
        assert sp.simplify(val - sp.exp(k)) == 0
        text = r"Calcolare \( \displaystyle\lim_{n\to +\infty} \left(1+\dfrac{%d}{n}\right)^{n} \)." % k
        correct = wrap(f"e^{{{k}}}" if k != 1 else "e")
        wrong_vals = [f"e^{{{-k}}}" if -k != 1 else "e", f"{k}e", "1"]
        wrong = []
        seen = {correct}
        for w in wrong_vals:
            ww = wrap(w)
            if ww not in seen:
                wrong.append(ww)
                seen.add(ww)
        if len(wrong) == 3:
            add(text, correct, wrong)

    # ---- SU4: radici n-esime, lim n-esima_radice(a) = 1, lim n-esima_radice(n^b) = 1 ----
    for a in random.sample([2, 3, 5, 7, 10, 100, sp.Rational(1, 2)], 3):
        val = sp.limit(a ** (1 / n), n, sp.oo)
        assert val == 1
        text = r"Calcolare \( \displaystyle\lim_{n\to +\infty} \sqrt[n]{%s} \)." % sp.latex(a)
        correct = wrap("1")
        wrong = [wrap(w) for w in [sp.latex(a), "0", "+\\infty"]]
        add(text, correct, wrong)

    for b in random.sample([1, 2, 3, sp.Rational(1, 2), 5], 3):
        expr = (n ** b) ** (1 / n)
        val = sp.limit(expr, n, sp.oo)
        assert val == 1
        text = r"Calcolare \( \displaystyle\lim_{n\to +\infty} \sqrt[n]{n^{%s}} \)." % sp.latex(b)
        correct = wrap("1")
        wrong = [wrap(w) for w in ["+\\infty", "0", sp.latex(b)]]
        add(text, correct, wrong)

    # ---- SU5: teoria (enumerate, fedele alle slide) ----
    theory = [
        (r"Una successione \( (a_n)_{n\in\mathbb{N}} \) si dice convergente a \(\ell\in\mathbb{R}\) se:",
         "per ogni \\(\\varepsilon>0\\) esiste \\(n_0\\in\\mathbb{N}\\) tale che \\(|a_n-\\ell|<\\varepsilon\\) per ogni \\(n\\ge n_0\\)",
         ["esiste \\(n_0\\) tale che \\(a_{n_0}=\\ell\\)", "\\(a_n=\\ell\\) per ogni \\(n\\)", "la successione è limitata"]),
        (r"Una successione convergente o divergente si dice:",
         "regolare", ["monotona", "limitata", "infinitesima"]),
        (r"Una successione convergente a zero si dice:",
         "infinitesima", ["infinita", "regolare", "limitata"]),
        (r"La successione \( a_n = (-1)^n \) è:",
         "limitata ma non regolare (non converge né diverge)",
         ["convergente a 0", "divergente a \\(+\\infty\\)", "infinitesima"]),
        (r"Il Teorema sulla limitatezza delle successioni convergenti afferma che:",
         "ogni successione convergente è limitata (ma non vale il viceversa, es. \\(a_n=(-1)^n\\))",
         ["ogni successione limitata è convergente", "ogni successione convergente è monotona", "ogni successione limitata è monotona"]),
        (r"Il Teorema di regolarità delle successioni monotòne afferma che ogni successione monotòna è regolare, e se è crescente il limite vale:",
         "\\(\\sup_{n} a_n\\)", ["\\(\\inf_{n} a_n\\)", "\\(\\max_n a_n\\)", "non è detto che esista"]),
        (r"Una successione monotòna e limitata è:",
         "convergente", ["divergente", "non regolare", "necessariamente costante"]),
        (r"Il Teorema del confronto (dei carabinieri) per successioni afferma che se \(a_n \le c_n \le b_n\) definitivamente e \(a_n, b_n \to \ell \in \mathbb{R}\), allora:",
         "\\(c_n\\) è convergente e \\(\\lim_n c_n = \\ell\\)",
         ["\\(c_n\\) è divergente", "\\(c_n\\) non è regolare", "non si può concludere nulla su \\(c_n\\)"]),
        (r"Se \(a_n \to +\infty\) e \((b_n)\) è limitata inferiormente, allora \(a_n+b_n\):",
         "tende a \\(+\\infty\\)", ["tende a \\(0\\)", "è limitata", "non è regolare"]),
        (r"Se \(a_n \to 0\) e \((b_n)\) è limitata, il prodotto \(a_n \cdot b_n\):",
         "tende a \\(0\\)", ["tende a \\(+\\infty\\)", "non è regolare", "è costante"]),
        (r"Una successione \((a_n)\) si dice strettamente crescente se:",
         "\\(a_n < a_{n+1}\\) per ogni \\(n\\in\\mathbb{N}\\)", ["\\(a_n \\le a_{n+1}\\) per ogni \\(n\\)", "\\(a_n > a_{n+1}\\) per ogni \\(n\\)", "\\(a_n = a_{n+1}\\) per ogni \\(n\\)"]),
    ]
    for text, correct, wrong in theory:
        add(text, correct, wrong)

    return items


if __name__ == "__main__":
    random.seed(808)
    items = build()
    print("Totale domande successioni:", len(items))
    bad = 0
    for it in items:
        opts = [it["correct"]] + it["wrong"]
        if len(set(opts)) != 4:
            bad += 1
            print("PROBLEMA:", it["text"], opts)
    print("Domande con problemi:", bad)
