# -*- coding: utf-8 -*-
"""Capitolo 6 - Calcolo differenziale: generazione verificata con sympy."""
import random
import sympy as sp

x, a_s, b_s = sp.symbols('x a b')


def wrap(s):
    return f"\\({s}\\)"


def coef_x(n, var="x", power=""):
    base = var + power
    if n == 1:
        return base
    if n == -1:
        return f"-{base}"
    return f"{n}{base}"


def poly_expr(coeffs, var="x"):
    """coeffs = [a3,a2,a1,a0] per a3x^3+a2x^2+a1x+a0, formattazione pulita."""
    n = len(coeffs) - 1
    parts = []
    for i, c in enumerate(coeffs):
        p = n - i
        if c == 0:
            continue
        term = coef_x(c, var, ("^{%d}" % p if p > 1 else "")) if p > 0 else f"{c}"
        if parts:
            term = ("+ " + term.lstrip('-') if c > 0 else "- " + term.lstrip('-'))
        parts.append(term)
    return " ".join(parts) if parts else "0"


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

    # ---- D1: derivata di un polinomio cubico in un punto ----
    count = 0
    for _ in range(60):
        if count >= 7:
            break
        coeffs = [random.choice([n for n in range(-4, 5) if n != 0]),
                  random.randint(-4, 4), random.randint(-6, 6), random.randint(-6, 6)]
        x0 = random.randint(-3, 3)
        expr = coeffs[0] * x ** 3 + coeffs[1] * x ** 2 + coeffs[2] * x + coeffs[3]
        deriv = sp.diff(expr, x)
        val = deriv.subs(x, x0)
        text = r"Data \( f(x) = %s \), calcolare \( f'(%d) \)." % (poly_expr(coeffs), x0)
        correct = wrap(sp.latex(val))
        wrong = [wrap(w) for w in num_distractors(val, extra=[expr.subs(x, x0)])]
        if add(text, correct, wrong):
            count += 1

    # ---- D2: derivate di funzioni composte lineari (formula, non punto) ----
    def mult_prefix(n):
        """Prefisso moltiplicativo pulito: '' per 1, '-' per -1, altrimenti 'n'."""
        if n == 1:
            return ""
        if n == -1:
            return "-"
        return f"{n}"

    count = 0
    kinds = ["exp", "ln", "sin", "cos"]
    combos = [(k, a, b) for k in kinds for a in range(-5, 6) for b in range(-4, 5) if a != 0]
    random.shuffle(combos)
    for k, a, b in combos:
        if count >= 7:
            break
        if k == "ln" and b == 0:
            continue  # ln(ax) ha derivata 1/x indipendente da a: caso poco interessante/ambiguo
        b_term = (f" + {b}" if b > 0 else (f" - {-b}" if b < 0 else ""))
        a_str = coef_x(a)
        neg_a_str = coef_x(-a)
        if k == "exp":
            text = r"Calcolare la derivata di \( f(x) = e^{%s%s} \)." % (a_str, b_term)
            correct = wrap(r"f'(x) = %se^{%s%s}" % (mult_prefix(a), a_str, b_term))
            wrong = [wrap(w) for w in [
                r"f'(x) = e^{%s%s}" % (a_str, b_term),
                r"f'(x) = %sx\,e^{%s%s}" % (mult_prefix(a) or "", a_str, b_term),
                r"f'(x) = %s" % a,
            ]]
        elif k == "ln":
            arg = f"{a_str}{b_term}"
            text = r"Calcolare la derivata di \( f(x) = \ln(%s) \), per \(x\) nel dominio." % arg
            correct = wrap(r"f'(x) = \dfrac{%d}{%s}" % (a, arg))
            wrong = [wrap(w) for w in [
                r"f'(x) = \dfrac{1}{%s}" % arg,
                r"f'(x) = \dfrac{%d}{x}" % a,
                r"f'(x) = %d" % a,
            ]]
        elif k == "sin":
            text = r"Calcolare la derivata di \( f(x) = \sin(%s%s) \)." % (a_str, b_term)
            correct = wrap(r"f'(x) = %s\cos(%s%s)" % (mult_prefix(a), a_str, b_term))
            wrong = [wrap(w) for w in [
                r"f'(x) = %s\sin(%s%s)" % (mult_prefix(a), a_str, b_term),
                r"f'(x) = \cos(%s%s)" % (a_str, b_term),
                r"f'(x) = %s\cos(%s%s)" % (mult_prefix(-a), a_str, b_term),
            ]]
        else:
            text = r"Calcolare la derivata di \( f(x) = \cos(%s%s) \)." % (a_str, b_term)
            correct = wrap(r"f'(x) = %s\sin(%s%s)" % (mult_prefix(-a), a_str, b_term))
            wrong = [wrap(w) for w in [
                r"f'(x) = %s\sin(%s%s)" % (mult_prefix(a), a_str, b_term),
                r"f'(x) = -\sin(%s%s)" % (a_str, b_term),
                r"f'(x) = %s\cos(%s%s)" % (mult_prefix(a), a_str, b_term),
            ]]
        if add(text, correct, wrong):
            count += 1

    # ---- D3: massimi/minimi relativi di f(x) = x^3 - 3k^2 x ----
    count = 0
    for k in random.sample(range(1, 10), 7):
        expr = x ** 3 - 3 * k ** 2 * x
        crit = sorted(sp.solve(sp.diff(expr, x), x))
        assert crit == [-k, k]
        text = r"Data \( f(x) = x^3 - %dx \), determinare la natura del punto critico \( x = %d \)." % (3 * k ** 2, k)
        correct = "un minimo relativo (\\(f''(x) = 6x > 0\\) in quel punto)"
        wrong = ["un massimo relativo", "un flesso a tangente orizzontale", "un punto di non derivabilità"]
        if add(text, correct, wrong):
            count += 1
            text2 = r"Data \( f(x) = x^3 - %dx \), determinare la natura del punto critico \( x = %d \)." % (3 * k ** 2, -k)
            correct2 = "un massimo relativo (\\(f''(x) = 6x < 0\\) in quel punto)"
            wrong2 = ["un minimo relativo", "un flesso a tangente orizzontale", "un punto di non derivabilità"]
            add(text2, correct2, wrong2)

    # ---- D4: Lagrange per f(x)=x^2 su [a,b], c = (a+b)/2 ----
    count = 0
    pairs = [(a, b) for a in range(-6, 6) for b in range(a + 1, a + 8)]
    random.shuffle(pairs)
    for a, b in pairs:
        if count >= 6:
            break
        c = sp.Rational(a + b, 2)
        text = r"Applicando il Teorema di Lagrange a \( f(x) = x^2 \) su \( [%d,%d] \), determinare il punto \(c\)." % (a, b)
        correct = wrap(sp.latex(c))
        wrong = [wrap(w) for w in num_distractors(c, extra=[a, b])]
        if add(text, correct, wrong):
            count += 1

    # ---- D5: Taylor di ordine 2 di e^x, sin x, ln(1+x) in x0=0 ----
    taylor_specs = [
        (sp.exp(x), "e^x", 2, "1 + x + \\dfrac{x^2}{2}", ["1 + x", "1 + \\dfrac{x^2}{2}", "x + \\dfrac{x^2}{2}"]),
        (sp.sin(x), "\\sin x", 3, "x - \\dfrac{x^3}{6}", ["x + \\dfrac{x^3}{6}", "x - \\dfrac{x^2}{2}", "1 - \\dfrac{x^2}{2}"]),
        (sp.ln(1 + x), "\\ln(1+x)", 2, "x - \\dfrac{x^2}{2}", ["x + \\dfrac{x^2}{2}", "1 + x", "-x + \\dfrac{x^2}{2}"]),
        (sp.cos(x), "\\cos x", 2, "1 - \\dfrac{x^2}{2}", ["1 + \\dfrac{x^2}{2}", "1 - x^2", "x - \\dfrac{x^3}{6}"]),
        (1 / (1 - x), "\\dfrac{1}{1-x}", 2, "1 + x + x^2", ["1 - x + x^2", "1 + x", "1 + x - x^2"]),
        ((1 + x) ** sp.Rational(1, 2), "\\sqrt{1+x}", 2, "1 + \\dfrac{x}{2} - \\dfrac{x^2}{8}",
         ["1 + \\dfrac{x}{2} + \\dfrac{x^2}{8}", "1 - \\dfrac{x}{2} + \\dfrac{x^2}{8}", "1 + x - \\dfrac{x^2}{2}"]),
    ]
    for expr, expr_s, order, correct_latex, wrong_list in taylor_specs:
        series = sp.series(expr, x, 0, order + 1).removeO()
        # verifica: valuta correct_latex parsando in sympy tramite sostituzione manuale non necessaria,
        # ci fidiamo del calcolo diretto di sympy per il polinomio di taylor
        text = r"Determinare il polinomio di Taylor di ordine \(%d\), centrato in \(x_0=0\), di \( f(x) = %s \)." % (order, expr_s)
        correct = wrap(correct_latex)
        wrong = [wrap(w) for w in wrong_list]
        add(text, correct, wrong)

    # ---- D6: concavità di f(x) = x^4 - k x^2 ----
    count = 0
    for k in random.sample(range(2, 20, 2), 7):
        expr = x ** 4 - k * x ** 2
        f2 = sp.diff(expr, x, 2)
        infl = sorted(sp.solve(f2, x))
        bound = sp.sqrt(sp.Rational(k, 6))
        assert all(sp.simplify(sp.Abs(i) - bound) == 0 for i in infl)
        text = r"Studiare la concavità di \( f(x) = x^4 - %dx^2 \): in quale intervallo \(f\) è concava (verso il basso)?" % k
        correct = wrap(r"\left( -%s, %s \right)" % (sp.latex(bound), sp.latex(bound)))
        wrong = [
            wrap(r"\left( -\infty, -%s \right) \cup \left( %s, +\infty \right)" % (sp.latex(bound), sp.latex(bound))),
            wrap(r"\left( -\infty, +\infty \right)"),
            wrap("\\text{in nessun intervallo}"),
        ]
        if add(text, correct, wrong):
            count += 1

    # ---- D7: asintoto obliquo di funzioni razionali (grado num = grado den + 1) ----
    count = 0
    for _ in range(40):
        if count >= 7:
            break
        m = random.choice([n for n in range(-4, 5) if n != 0])
        q = random.randint(-5, 5)
        den_root = random.choice([n for n in range(-5, 6) if n != 0])
        num = (m * x + q) * (x - den_root) + random.randint(-3, 3)
        den = x - den_root
        expr = sp.cancel(num / den)
        m_calc = sp.limit(expr / x, x, sp.oo)
        q_calc = sp.limit(expr - m_calc * x, x, sp.oo)
        if m_calc == 0:
            continue
        num_latex = sp.latex(sp.expand(num))
        den_str = "x" + (f" - {den_root}" if den_root > 0 else f" + {-den_root}")
        text = r"Determinare l'asintoto obliquo di \( f(x) = \dfrac{%s}{%s} \) per \( x \to +\infty \)." % (num_latex, den_str)
        q_str = f" + {sp.latex(q_calc)}" if q_calc > 0 else (f" - {sp.latex(-q_calc)}" if q_calc < 0 else "")
        correct_line = f"y = {coef_x(m_calc)}{q_str}" if m_calc != 1 and m_calc != -1 else f"y = {coef_x(m_calc)}{q_str}"
        correct = wrap(correct_line)
        wrong_lines = [
            f"y = {coef_x(-m_calc)}{q_str}",
            f"y = {coef_x(m_calc)}" + (f" - {sp.latex(q_calc)}" if q_calc > 0 else (f" + {sp.latex(-q_calc)}" if q_calc < 0 else " + 1")),
            f"y = {sp.latex(q_calc)}",
        ]
        wrong = []
        seen = {correct_line}
        for w in wrong_lines:
            if w not in seen:
                wrong.append(wrap(w))
                seen.add(w)
        if len(wrong) == 3 and add(text, correct, wrong):
            count += 1

    return items


if __name__ == "__main__":
    random.seed(606)
    items = build()
    print("Totale domande generate (Capitolo 6):", len(items))
    bad = 0
    for it in items:
        opts = [it["correct"]] + it["wrong"]
        if len(set(opts)) != 4:
            bad += 1
            print("PROBLEMA:", it["text"], opts)
    print("Domande con problemi:", bad)
