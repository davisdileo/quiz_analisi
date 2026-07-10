# -*- coding: utf-8 -*-
"""Capitolo 3 - Funzioni reali: generazione verificata con sympy."""
import random
import sympy as sp

x = sp.symbols('x', real=True)


def wrap(s):
    return f"\\({s}\\)"


def signed_term(coef, var="x"):
    if coef == 0:
        return ""
    if coef == 1:
        return f"+ {var}"
    if coef == -1:
        return f"- {var}"
    return f"+ {coef}{var}" if coef > 0 else f"- {-coef}{var}"


def lin_expr(a, b, var="x"):
    """a*var + b, con formattazione pulita (niente 1x, niente +0)."""
    parts = []
    if a == 1:
        parts.append(var)
    elif a == -1:
        parts.append(f"-{var}")
    else:
        parts.append(f"{a}{var}")
    if b > 0:
        parts.append(f"+ {b}")
    elif b < 0:
        parts.append(f"- {-b}")
    return " ".join(parts)


def interval_str(lo, hi, left_open, right_open):
    lb = r"\left(" if left_open else r"\left["
    rb = r"\right)" if right_open else r"\right]"
    return f"{lb} {sp.latex(lo)},\\ {sp.latex(hi)} {rb}"


def ray_str(bound, is_lower, closed):
    # es. [a, +infty) oppure (-infty, a]
    if is_lower:
        lb = r"\left[" if closed else r"\left("
        return f"{lb} {sp.latex(bound)},\\ +\\infty \\right)"
    else:
        rb = r"\right]" if closed else r"\right)"
        return f"\\left( -\\infty,\\ {sp.latex(bound)} {rb}"


def build():
    items = []
    seen_texts = set()

    def add(text, correct, wrong):
        if len(set([correct] + wrong)) != 4:
            return False
        if text in seen_texts:
            return False
        seen_texts.add(text)
        items.append({"text": text, "correct": correct, "wrong": wrong})
        return True

    # ---- F1: dominio di sqrt(ax+b) ----
    combos = [(a, b) for a in [1, 2, 3, -1, -2, -3] for b in range(-9, 10)]
    random.shuffle(combos)
    count = 0
    for a, b in combos:
        if count >= 8:
            break
        bound = sp.Rational(-b, a)
        text = r"Determinare il dominio di \( f(x) = \sqrt{%s} \)." % lin_expr(a, b)
        if a > 0:
            correct = wrap(ray_str(bound, True, True))
            wrong = [wrap(ray_str(bound, False, True)), wrap(ray_str(bound, True, False)), wrap(ray_str(bound, False, False))]
        else:
            correct = wrap(ray_str(bound, False, True))
            wrong = [wrap(ray_str(bound, True, True)), wrap(ray_str(bound, False, False)), wrap(ray_str(bound, True, False))]
        if add(text, correct, wrong):
            count += 1

    # ---- F2: dominio di 1/(x^2-k), k = quadrato perfetto ----
    ks = [1, 4, 9, 16, 25, 36, 49, 64]
    random.shuffle(ks)
    count = 0
    for k in ks[:6]:
        r = int(sp.sqrt(k))
        text = r"Determinare il dominio di \( f(x) = \dfrac{1}{x^2 - %d} \)." % k
        correct = wrap(r"\mathbb{R} \setminus \{-%d, %d\}" % (r, r))
        wrong = [
            wrap(r"\mathbb{R} \setminus \{%d\}" % r),
            wrap(r"\mathbb{R}"),
            wrap(r"\left( -%d, %d \right)" % (r, r)),
        ]
        if add(text, correct, wrong):
            count += 1

    # ---- F3: dominio di ln(ax+b) ----
    combos = [(a, b) for a in [1, 2, 3, -1, -2] for b in range(-8, 9)]
    random.shuffle(combos)
    count = 0
    for a, b in combos:
        if count >= 8:
            break
        bound = sp.Rational(-b, a)
        text = r"Determinare il dominio di \( f(x) = \ln(%s) \)." % lin_expr(a, b)
        if a > 0:
            correct = wrap(ray_str(bound, True, False))
            wrong = [wrap(ray_str(bound, True, True)), wrap(ray_str(bound, False, False)), wrap(ray_str(bound, False, True))]
        else:
            correct = wrap(ray_str(bound, False, False))
            wrong = [wrap(ray_str(bound, False, True)), wrap(ray_str(bound, True, False)), wrap(ray_str(bound, True, True))]
        if add(text, correct, wrong):
            count += 1

    # ---- F4: dominio di ln(x-a) + sqrt(b-x), a<b ----
    pairs = [(a, b) for a in range(-6, 5) for b in range(a + 1, a + 8)]
    random.shuffle(pairs)
    count = 0
    for a, b in pairs:
        if count >= 8:
            break
        a_term = f"x - {a}" if a >= 0 else f"x + {-a}"
        b_term = f"{b} - x"
        text = r"Determinare il dominio di \( f(x) = \ln(%s) + \sqrt{%s} \)." % (a_term, b_term)
        correct = wrap(interval_str(a, b, True, False))
        wrong = [
            wrap(interval_str(a, b, False, False)),
            wrap(interval_str(a, b, True, True)),
            wrap(r"\left( -\infty,\ %d \right)" % b),
        ]
        if add(text, correct, wrong):
            count += 1

    # ---- F8: dominio di arcsin(ax+b) ----
    combos = [(a, b) for a in [1, 2, 3] for b in range(-4, 5)]
    random.shuffle(combos)
    count = 0
    for a, b in combos:
        if count >= 8:
            break
        lo = sp.Rational(-1 - b, a)
        hi = sp.Rational(1 - b, a)
        if lo > hi:
            lo, hi = hi, lo
        text = r"Determinare il dominio di \( f(x) = \arcsin(%s) \)." % lin_expr(a, b)
        correct = wrap(interval_str(lo, hi, False, False))
        wrong = [
            wrap(interval_str(-hi, -lo, False, False)),
            wrap(interval_str(lo - 1, hi + 1, False, False)),
            wrap(r"\mathbb{R}"),
        ]
        if add(text, correct, wrong):
            count += 1

    # ---- F5: parità/disparità (enumerate) ----
    parity = [
        (r"f(x) = x^4 - 3x^2", "pari (f(-x) = f(x) per ogni x)", ["dispari", "né pari né dispari", "periodica"]),
        (r"f(x) = x^3 + x", "dispari (f(-x) = -f(x) per ogni x)", ["pari", "né pari né dispari", "costante"]),
        (r"f(x) = x^2 + x", "né pari né dispari", ["pari", "dispari", "periodica"]),
        (r"f(x) = |x|", "pari (f(-x) = f(x) per ogni x)", ["dispari", "né pari né dispari", "monotona su \\(\\mathbb{R}\\)"]),
        (r"f(x) = \sin x + x", "dispari (f(-x) = -f(x) per ogni x)", ["pari", "né pari né dispari", "limitata"]),
        (r"f(x) = \cos x + x^2", "pari (f(-x) = f(x) per ogni x)", ["dispari", "né pari né dispari", "illimitata inferiormente"]),
        (r"f(x) = x \cdot \sin x", "pari (prodotto di due funzioni dispari)", ["dispari", "né pari né dispari", "periodica"]),
        (r"f(x) = x^3 \cdot \cos x", "dispari (prodotto di una funzione dispari per una pari)", ["pari", "né pari né dispari", "limitata"]),
        (r"f(x) = e^x", "né pari né dispari", ["pari", "dispari", "periodica"]),
        (r"f(x) = x^5 - 2x^3 + x", "dispari (f(-x) = -f(x) per ogni x)", ["pari", "né pari né dispari", "costante"]),
        (r"f(x) = \tan x", "dispari (f(-x) = -f(x) per ogni x)", ["pari", "né pari né dispari", "limitata"]),
        (r"f(x) = x^2 + 1", "pari (f(-x) = f(x) per ogni x)", ["dispari", "né pari né dispari", "iniettiva su \\(\\mathbb{R}\\)"]),
    ]
    for expr, correct, wrong in parity:
        text = r"La funzione \( %s \), \( x \in \mathbb{R} \), è:" % expr
        add(text, correct, wrong)

    # ---- F6: funzione inversa di f(x) = a + ln(x-b) ----
    def plus_minus(n):
        """'+ n' o '- |n|', da usare dopo un termine esistente."""
        return f"+ {n}" if n >= 0 else f"- {-n}"

    def x_minus_b(b):
        return "x" + (f" - {b}" if b > 0 else (f" + {-b}" if b < 0 else ""))

    def x_pm_exp(n):
        """'x' con eventuale +n/-n per un esponente (n=0 => solo 'x')."""
        if n == 0:
            return "x"
        return f"x + {n}" if n > 0 else f"x - {-n}"

    combos = [(a, b) for a in range(-3, 4) for b in range(-4, 5)]
    random.shuffle(combos)
    count = 0
    for a, b in combos:
        if count >= 8:
            break
        a_prefix = f"{a} + " if a != 0 else ""
        text = r"Determinare la funzione inversa di \( f(x) = %s\ln(%s) \), per \( x > %s \)." % (
            a_prefix, x_minus_b(b), b)
        # y = a + ln(x-b)  =>  x = b + e^{y-a}
        correct = wrap(r"f^{-1}(x) = %s + e^{%s}" % (b, x_pm_exp(-a)))
        wrong = [
            wrap(r"f^{-1}(x) = %s + e^{%s}" % (b, x_pm_exp(a))),
            wrap(r"f^{-1}(x) = e^{%s} %s" % (x_pm_exp(-a), plus_minus(-b))),
            wrap(r"f^{-1}(x) = \ln(%s) %s" % (x_minus_b(b), plus_minus(-a))),
        ]
        if add(text, correct, wrong):
            count += 1

    # ---- F7: funzione inversa di Möbius f(x) = (x+a)/(x+b) ----
    def x_plus(n):
        return "x" + (f" + {n}" if n > 0 else (f" - {-n}" if n < 0 else ""))

    combos = [(a, b) for a in range(-5, 6) for b in range(-5, 6) if a != b and b != 0]
    random.shuffle(combos)
    count = 0
    y = sp.symbols('y')
    for a, b in combos:
        if count >= 8:
            break
        f_expr = (x + a) / (x + b)
        sol = sp.solve(sp.Eq(y, f_expr), x)
        if not sol:
            continue
        inv = sp.simplify(sol[0])
        inv_latex = sp.latex(inv).replace('y', 'x')
        text = r"Determinare la funzione inversa di \( f(x) = \dfrac{%s}{%s} \), \( x \neq %s \)." % (
            x_plus(a), x_plus(b), -b)
        correct = wrap(r"f^{-1}(x) = %s" % inv_latex)
        wrong_exprs = [
            (x + b) / (x + a),          # scambia a e b
            -(x + a) / (x + b),
            (x - a) / (x - b),
        ]
        wrong_s = []
        seen = {sp.simplify(inv)}
        for we in wrong_exprs:
            we_s = sp.simplify(we)
            if we_s not in seen:
                wrong_s.append(sp.latex(we_s).replace('y', 'x'))
                seen.add(we_s)
        wrong = [wrap(f"f^{{-1}}(x) = {w}") for w in wrong_s[:3]]
        if len(wrong) == 3 and add(text, correct, wrong):
            count += 1

    return items


if __name__ == "__main__":
    random.seed(303)
    items = build()
    print("Totale domande generate (Capitolo 3):", len(items))
    bad = 0
    for it in items:
        opts = [it["correct"]] + it["wrong"]
        if len(set(opts)) != 4 or len(it["wrong"]) != 3:
            bad += 1
            print("PROBLEMA:", it["text"], opts)
    print("Domande con problemi:", bad)
