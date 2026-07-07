# -*- coding: utf-8 -*-
"""Capitolo 7 - Calcolo integrale: generazione verificata con sympy."""
import random
import sympy as sp

x, t = sp.symbols('x t')


def wrap(s):
    return f"\\({s}\\)"


def latex_ln(expr):
    """Come sp.latex ma con \\ln invece di \\log (convenzione dei libri di testo)."""
    return sp.latex(expr, ln_notation=True)


def coef_x(n, var="x", power=""):
    base = var + power
    if n == 1:
        return base
    if n == -1:
        return f"-{base}"
    return f"{n}{base}"


def num_distractors(correct_val, extra=()):
    cv = sp.nsimplify(correct_val)
    cands = list(extra) + [-cv, cv * 2, cv + 1, cv - 1, cv / 2, sp.Integer(0)]
    out, seen = [], {latex_ln(cv)}
    for c in cands:
        cs = latex_ln(sp.nsimplify(c))
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

    # ---- I1: integrale indefinito di a*x^n ----
    count = 0
    combos = [(a, n) for a in range(-6, 7) for n in range(1, 6) if a != 0]
    random.shuffle(combos)
    for a, n in combos:
        if count >= 6:
            break
        prim = sp.integrate(a * x ** n, x)
        text = r"Calcolare \( \displaystyle\int %s\,dx \)." % coef_x(a, power=("^{%d}" % n if n > 1 else ""))
        correct = wrap(sp.latex(prim) + " + C")
        wrong = [
            wrap(sp.latex(a * x ** (n + 1)) + " + C"),
            wrap(sp.latex(a * (n + 1) * x ** (n + 1)) + " + C"),
            wrap(sp.latex(sp.integrate(a * x ** n, x) / (n + 1)) + " + C"),
        ]
        if add(text, correct, wrong):
            count += 1

    # ---- I2: integrale definito di un polinomio quadratico ----
    count = 0
    combos = [(a, b, c, lo, hi) for a in range(-4, 5) for b in range(-3, 4) for c in range(-3, 4)
              for lo in range(-3, 3) for hi in range(lo + 1, lo + 4) if a != 0]
    random.shuffle(combos)
    for a, b, c, lo, hi in combos:
        if count >= 6:
            break
        expr = a * x ** 2 + b * x + c
        val = sp.integrate(expr, (x, lo, hi))
        expr_s = sp.latex(sp.expand(expr))
        text = r"Calcolare \( \displaystyle\int_{%d}^{%d} \left( %s \right) dx \)." % (lo, hi, expr_s)
        correct = wrap(sp.latex(val))
        wrong = [wrap(w) for w in num_distractors(val)]
        if add(text, correct, wrong):
            count += 1

    # ---- I3: integrazione per parti ∫ x e^{ax} dx ----
    count = 0
    for a in random.sample([n for n in range(-5, 6) if n != 0], 6):
        prim = sp.integrate(x * sp.exp(a * x), x)
        prim = sp.simplify(prim)
        text = r"Calcolare \( \displaystyle\int x\,e^{%s}\,dx \)." % coef_x(a)
        correct = wrap(sp.latex(prim) + " + C")
        wrong = [
            wrap(sp.latex(sp.exp(a * x) / a) + " + C"),
            wrap(sp.latex(x * sp.exp(a * x)) + " + C"),
            wrap(sp.latex(-prim) + " + C"),
        ]
        if add(text, correct, wrong):
            count += 1

    # ---- I4: integrali notevoli 1/(x^2+a^2) e simili ----
    count = 0
    for a in random.sample(range(1, 10), 6):
        prim = sp.integrate(1 / (x ** 2 + a ** 2), x)
        # verifica: la primitiva "canonica" (1/a) arctan(x/a) deve avere la stessa derivata
        canonical = sp.Rational(1, a) * sp.atan(x / a)
        assert sp.simplify(sp.diff(canonical, x) - 1 / (x ** 2 + a ** 2)) == 0
        text = r"Calcolare \( \displaystyle\int \dfrac{dx}{x^2 + %d} \)." % (a ** 2)
        correct = wrap(f"\\dfrac{{1}}{{{a}}}\\arctan\\left(\\dfrac{{x}}{{{a}}}\\right) + C")
        wrong = [
            wrap(r"\arctan(x) + C"),
            wrap(f"{a}\\arctan\\left(\\dfrac{{x}}{{{a}}}\\right) + C"),
            wrap(r"\dfrac{1}{x^2+%d} \cdot x + C" % (a ** 2)),
        ]
        if add(text, correct, wrong):
            count += 1

    # ---- I5: integrale definito con sostituzione, ∫0^b (2ax)/(1+a x^2) dx tipo log ----
    count = 0
    combos = [(a, b) for a in range(1, 6) for b in range(1, 5)]
    random.shuffle(combos)
    for a, b in combos:
        if count >= 6:
            break
        expr = (2 * a * x) / (1 + a * x ** 2)
        val = sp.simplify(sp.integrate(expr, (x, 0, b)))
        num_str = coef_x(2 * a) if a != 1 else "2x"
        den_str = f"1+{a}x^2" if a != 1 else "1+x^2"
        text = r"Calcolare \( \displaystyle\int_0^{%d} \dfrac{%s}{%s}\,dx \)." % (b, num_str, den_str)
        correct = wrap(latex_ln(val))
        wrong = [wrap(w) for w in num_distractors(val)]
        if add(text, correct, wrong):
            count += 1

    # ---- I6: area tra parabola y=x^2+k e retta y=mx+q ----
    count = 0
    combos = [(k, m, q) for k in range(-3, 4) for m in range(-3, 4) for q in range(0, 6)]
    random.shuffle(combos)
    for k, m, q in combos:
        if count >= 6:
            break
        # intersezioni di x^2+k = mx+q  =>  x^2 - mx + (k-q) = 0
        disc = m ** 2 - 4 * (k - q)
        if disc <= 0:
            continue
        sqrt_disc = sp.sqrt(disc)
        if sqrt_disc != int(sqrt_disc):
            continue  # vogliamo intersezioni razionali, per un'area "pulita"
        inter = sp.solve(sp.Eq(x ** 2 + k, m * x + q), x)
        if len(inter) != 2:
            continue
        lo, hi = sorted(inter)
        if not (lo.is_real and hi.is_real) or hi - lo < 1:
            continue
        area = sp.integrate((m * x + q) - (x ** 2 + k), (x, lo, hi))
        if area <= 0:
            continue
        k_term = (f" + {k}" if k > 0 else (f" - {-k}" if k < 0 else ""))
        line_s = f"{coef_x(m)} + {q}" if m != 0 else f"{q}"
        text = (r"Calcolare l'area della regione compresa tra le curve \( y=x^2%s \) e \( y=%s \)." %
                (k_term, line_s))
        correct = wrap(sp.latex(area))
        wrong = [wrap(w) for w in num_distractors(area)]
        if add(text, correct, wrong):
            count += 1

    # ---- I7: integrali impropri ∫1^inf 1/x^n dx (n>1) ----
    count = 0
    for n in random.sample(range(2, 9), 6):
        val = sp.integrate(1 / x ** n, (x, 1, sp.oo))
        text = r"Calcolare \( \displaystyle\int_1^{+\infty} \dfrac{dx}{x^{%d}} \)." % n
        correct = wrap(sp.latex(val))
        wrong_s = num_distractors(val)[:2] + ["\\text{diverge}"]
        wrong = [wrap(w) for w in wrong_s]
        if add(text, correct, wrong):
            count += 1

    # ---- I8: Teorema fondamentale, derivata di funzione integrale con estremo variabile ----
    # Verifica simbolica esplicita (regola di Leibniz: d/dx int_0^g(x) f(t) dt = f(g(x)) g'(x))
    specs = [
        (sp.exp(-t ** 2), "e^{-t^2}", x ** 3, "x^3", "3x^2"),
        (sp.cos(t), "\\cos t", x ** 2, "x^2", "2x"),
        (1 / (1 + t ** 2), "\\dfrac{1}{1+t^2}", x ** 2, "x^2", "2x"),
        (sp.sin(t ** 2), "\\sin(t^2)", 2 * x, "2x", "2"),
    ]
    for f_t, f_s, g_expr, g_s, gprime_s in specs:
        expected = sp.diff(sp.Integral(f_t, (t, 0, g_expr)), x).doit()
        candidate = f_t.subs(t, g_expr) * sp.diff(g_expr, x)
        assert sp.simplify(expected - candidate) == 0
        f_at_g_s = f_s.replace('t', '(%s)' % g_s)
        text = (r"Usando il Teorema fondamentale del calcolo, calcolare \( \dfrac{d}{dx} "
                r"\displaystyle\int_0^{%s} %s\,dt \).") % (g_s, f_s)
        correct = wrap(f"{f_at_g_s} \\cdot {gprime_s}" if gprime_s != "1" else f_at_g_s)
        wrong = [
            wrap(f_at_g_s),
            wrap(f_s.replace('t', 'x')),
            wrap(f"{f_s.replace('t','x')} \\cdot {gprime_s}"),
        ]
        add(text, correct, wrong)

    # ---- I9: ∫0^pi sin^2(ax) o cos^2(ax) su un periodo (valori notevoli) ----
    count = 0
    trig_specs = [(sp.sin(x) ** 2, "\\sin^2 x", 0, sp.pi), (sp.cos(x) ** 2, "\\cos^2 x", 0, sp.pi),
                  (sp.sin(x) ** 2, "\\sin^2 x", 0, 2 * sp.pi), (sp.cos(x) ** 2, "\\cos^2 x", 0, 2 * sp.pi)]
    for expr, expr_s, lo, hi in trig_specs:
        val = sp.integrate(expr, (x, lo, hi))
        hi_s = "\\pi" if hi == sp.pi else "2\\pi"
        text = r"Calcolare \( \displaystyle\int_0^{%s} %s\,dx \)." % (hi_s, expr_s)
        correct = wrap(sp.latex(val))
        wrong = [wrap(w) for w in num_distractors(val, extra=[sp.pi, 2 * sp.pi])]
        add(text, correct, wrong)

    return items


if __name__ == "__main__":
    random.seed(707)
    items = build()
    print("Totale domande generate (Capitolo 7):", len(items))
    bad = 0
    for it in items:
        opts = [it["correct"]] + it["wrong"]
        if len(set(opts)) != 4:
            bad += 1
            print("PROBLEMA:", it["text"], opts)
    print("Domande con problemi:", bad)
