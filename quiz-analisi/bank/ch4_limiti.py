# -*- coding: utf-8 -*-
"""Capitolo 4 - Limiti: generazione verificata con sympy (sp.limit su ogni istanza)."""
import random
import sympy as sp

x = sp.symbols('x')


def wrap(s):
    return f"\\({s}\\)"


def sgn_num(n):
    return f"{n}" if n >= 0 else f"({n})"


def coef_x(n, var="x"):
    """n*var formattato senza '1x'/'−1x'."""
    if n == 1:
        return var
    if n == -1:
        return f"-{var}"
    return f"{n}{var}"


def one_plus_ax(a):
    """'1+ax' formattato correttamente anche per a negativo (es. '1-2x')."""
    if a == 1:
        return "1+x"
    if a == -1:
        return "1-x"
    return f"1+{a}x" if a > 0 else f"1-{-a}x"


def num_distractors(correct_val, extra=()):
    """Genera distrattori numerici plausibili (segno cambiato, doppio, metà, +1)."""
    cv = sp.nsimplify(correct_val)
    cands = [-cv, cv * 2, cv / 2, cv + 1, cv - 1, sp.Integer(0)]
    cands = list(extra) + cands
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

    # ---- L1: lim x->0 sin(ax)/(bx) = a/b ----
    combos = [(a, b) for a in range(1, 8) for b in range(1, 8) if a != b]
    random.shuffle(combos)
    count = 0
    for a, b in combos:
        if count >= 6:
            break
        expr = sp.sin(a * x) / (b * x)
        val = sp.limit(expr, x, 0)
        assert val == sp.Rational(a, b)
        text = r"Calcolare \( \displaystyle\lim_{x\to 0} \dfrac{\sin(%s)}{%s} \)." % (coef_x(a), coef_x(b))
        correct = wrap(sp.latex(val))
        wrong = [wrap(w) for w in num_distractors(val, extra=[sp.Rational(b, a)])]
        if add(text, correct, wrong):
            count += 1

    # ---- L2: lim x->0 (1-cos(ax))/x^2 = a^2/2 ----
    for a in random.sample(range(1, 9), 6):
        expr = (1 - sp.cos(a * x)) / x ** 2
        val = sp.limit(expr, x, 0)
        assert val == sp.Rational(a ** 2, 2)
        text = r"Calcolare \( \displaystyle\lim_{x\to 0} \dfrac{1-\cos(%dx)}{x^2} \)." % a
        correct = wrap(sp.latex(val))
        wrong = [wrap(w) for w in num_distractors(val, extra=[sp.Integer(a ** 2)])]
        add(text, correct, wrong)

    # ---- L3: lim x->0 (e^{ax}-1)/x = a ----
    for a in random.sample([n for n in range(-6, 7) if n != 0], 6):
        expr = (sp.exp(a * x) - 1) / x
        val = sp.limit(expr, x, 0)
        assert val == a
        text = r"Calcolare \( \displaystyle\lim_{x\to 0} \dfrac{e^{%s}-1}{x} \)." % coef_x(a)
        correct = wrap(sp.latex(val))
        wrong = [wrap(w) for w in num_distractors(val)]
        add(text, correct, wrong)

    # ---- L4: lim x->0 ln(1+ax)/x = a ----
    for a in random.sample([n for n in range(-6, 7) if n != 0], 6):
        expr = sp.ln(1 + a * x) / x
        val = sp.limit(expr, x, 0)
        assert val == a
        text = r"Calcolare \( \displaystyle\lim_{x\to 0} \dfrac{\ln(%s)}{x} \)." % one_plus_ax(a)
        correct = wrap(sp.latex(val))
        wrong = [wrap(w) for w in num_distractors(val)]
        add(text, correct, wrong)

    # ---- L5: lim x->+inf (1+a/x)^x = e^a ----
    for a in random.sample([n for n in range(-6, 7) if n != 0], 6):
        expr = (1 + sp.Rational(a) / x) ** x
        val = sp.limit(expr, x, sp.oo)
        assert sp.simplify(val - sp.exp(a)) == 0
        text = r"Calcolare \( \displaystyle\lim_{x\to +\infty} \left(1+\dfrac{%d}{x}\right)^{x} \)." % a
        correct = wrap(f"e^{{{a}}}" if a != 1 else "e")
        wrong_vals = [f"e^{{{-a}}}" if -a != 1 else "e", f"{a}e", "1"]
        wrong = []
        seen = {correct}
        for w in wrong_vals:
            ww = wrap(w)
            if ww not in seen:
                wrong.append(ww)
                seen.add(ww)
        if len(wrong) == 3:
            add(text, correct, wrong)

    # ---- L6: lim x->+inf di funzioni razionali (stesso grado, grado diverso) ----
    count = 0
    for _ in range(30):
        if count >= 8:
            break
        deg = random.choice([2, 3])
        a_lead = random.choice([n for n in range(-6, 7) if n != 0])
        b_lead = random.choice([n for n in range(-6, 7) if n != 0])
        same_degree = random.choice([True, False])
        num = a_lead * x ** deg + random.randint(-5, 5) * x + random.randint(-5, 5)
        den_deg = deg if same_degree else deg + random.choice([1, -1])
        if den_deg < 1:
            den_deg = deg + 1
        den = b_lead * x ** den_deg + random.randint(-5, 5) * x + random.randint(-5, 5)
        expr = num / den
        val = sp.limit(expr, x, sp.oo)
        num_s = sp.sstr(sp.expand(num)).replace('**', '^').replace('*', '')
        den_s = sp.sstr(sp.expand(den)).replace('**', '^').replace('*', '')
        text = (r"Calcolare \( \displaystyle\lim_{x\to +\infty} \dfrac{%s}{%s} \)." %
                (sp.latex(sp.expand(num)), sp.latex(sp.expand(den))))
        if val in (sp.oo, -sp.oo):
            correct = wrap("+\\infty" if val == sp.oo else "-\\infty")
            wrong = [wrap("-\\infty" if val == sp.oo else "+\\infty"), wrap("0"), wrap(sp.latex(sp.Rational(a_lead, b_lead)))]
        else:
            correct = wrap(sp.latex(val))
            wrong = [wrap(w) for w in num_distractors(val, extra=[sp.Integer(0)])]
        if add(text, correct, wrong):
            count += 1

    # ---- L7: lim x->0 (e^{ax}-1-ax)/x^2 = a^2/2 (Taylor) ----
    for a in random.sample([n for n in range(1, 9)], 6):
        expr = (sp.exp(a * x) - 1 - a * x) / x ** 2
        val = sp.limit(expr, x, 0)
        assert val == sp.Rational(a ** 2, 2)
        text = (r"Usando gli sviluppi di Taylor, calcolare \( \displaystyle\lim_{x\to 0} "
                r"\dfrac{e^{%s}-1-%s}{x^2} \).") % (coef_x(a), coef_x(a))
        correct = wrap(sp.latex(val))
        wrong = [wrap(w) for w in num_distractors(val, extra=[sp.Integer(a ** 2)])]
        add(text, correct, wrong)

    # ---- L8: lim x->+inf sqrt(x^2+ax) - x = a/2 ----
    for a in random.sample([n for n in range(-9, 10) if n != 0], 8):
        expr = sp.sqrt(x ** 2 + a * x) - x
        val = sp.limit(expr, x, sp.oo)
        assert val == sp.Rational(a, 2)
        sign = "+" if a >= 0 else "-"
        text = (r"Calcolare \( \displaystyle\lim_{x\to +\infty} \left( \sqrt{x^2 %s %dx} - x \right) \)." %
                (sign, abs(a)))
        correct = wrap(sp.latex(val))
        wrong = [wrap(w) for w in num_distractors(val, extra=[sp.Integer(a)])]
        add(text, correct, wrong)

    # ---- L9: teoria / confronti asintotici (enumerate) ----
    theory = [
        (r"Per \( x \to +\infty \), quale delle seguenti funzioni tende all'infinito più velocemente?",
         r"\( x! \)", [r"\( 2^x \)", r"\( x^{100} \)", r"\( \ln x \)"]),
        (r"Per \( x \to +\infty \), quale delle seguenti funzioni tende all'infinito più lentamente?",
         r"\( \ln x \)", [r"\( \sqrt{x} \)", r"\( x \)", r"\( x^2 \)"]),
        (r"Per \( x \to 0^+ \), quanto vale \( \displaystyle\lim_{x\to0^+} x \ln x \)?",
         r"\(0\)", [r"\(1\)", r"\(-\infty\)", r"\(+\infty\)"]),
        (r"Se \( f(x) \sim g(x) \) per \( x \to x_0 \) (sono asintoticamente equivalenti), allora per definizione:",
         r"\( \displaystyle\lim_{x\to x_0} \dfrac{f(x)}{g(x)} = 1 \)",
         [r"\( f(x) = g(x) \) per ogni \(x\)", r"\( \displaystyle\lim_{x\to x_0} (f(x)-g(x)) = 0 \)", r"\( f \) e \( g \) hanno lo stesso dominio"]),
        (r"Il simbolo di Landau \( o(g(x)) \) per \( x \to x_0 \) indica una funzione \( f \) tale che:",
         r"\( \displaystyle\lim_{x\to x_0} \dfrac{f(x)}{g(x)} = 0 \)",
         [r"\( \displaystyle\lim_{x\to x_0} \dfrac{f(x)}{g(x)} = 1 \)", r"\( f(x) = g(x) \)", r"\( f(x) \geq g(x) \) per ogni \(x\)"]),
        (r"Per \( x \to +\infty \), il rapporto \( \dfrac{\ln x}{x^{0{,}01}} \) tende a:",
         r"\(0\)", [r"\(1\)", r"\(+\infty\)", "non esiste"]),
    ]
    for text, correct, wrong in theory:
        add(text, correct, wrong)

    return items


if __name__ == "__main__":
    random.seed(404)
    items = build()
    print("Totale domande generate (Capitolo 4):", len(items))
    bad = 0
    for it in items:
        opts = [it["correct"]] + it["wrong"]
        if len(set(opts)) != 4:
            bad += 1
            print("PROBLEMA:", it["text"], opts)
    print("Domande con problemi:", bad)
