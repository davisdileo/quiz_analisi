# -*- coding: utf-8 -*-
"""Integrali nello stile esatto delle tracce d'esame del docente:
∫x^3/sqrt(9+x^2)dx, ∫cos(ln x)dx, ∫x^2/(sqrt(x)(x+1))dx,
∫(tan^4x-4)/(tanx+sqrt2)dx, ∫(x+1)/sqrt(x^2+6x+10)dx, ∫1/sin^2(x)dx,
∫(x^2+x)/(3-2x+x^2)dx. Ogni primitiva viene calcolata con sympy e
verificata numericamente derivandola e confrontandola con l'integranda in
piu' punti del dominio (metodo robusto, indipendente dalla forma in cui
sympy restituisce il risultato).
"""
import random
import sympy as sp

x = sp.symbols('x', real=True)


def wrap(s):
    return f"\\({s}\\)"


def verify_integral(integrand, F, points):
    for xv in points:
        try:
            d = complex(sp.N(sp.diff(F, x).subs(x, xv), 25))
            i = complex(sp.N(integrand.subs(x, xv), 25))
        except Exception:
            return False
        if abs(d - i) > 1e-8:
            return False
    return True


def latex_ln(expr):
    return sp.latex(expr, ln_notation=True)


def clean_latex(s):
    s = s.replace(r"\operatorname{atan}", r"\arctan")
    s = s.replace(r"\left(1\ln", r"\left(\ln")
    s = s.replace(r" 1\ln", r" \ln")
    s = s.replace(r"+1\ln", r"+\ln")
    s = s.replace(r"-1\ln", r"-\ln")
    return s


def make_list():
    out = []
    seen = set()

    def add(text, correct, wrongs):
        correct = clean_latex(correct)
        wrongs = [clean_latex(w) for w in wrongs]
        opts = [correct] + wrongs
        if len(set(opts)) != 4:
            return False
        if text in seen:
            return False
        seen.add(text)
        out.append({"text": text, "correct": wrap(correct), "wrong": [wrap(w) for w in wrongs]})
        return True

    return out, add


def num_distractor_forms(F_latex, integrand=None):
    """Genera varianti plausibili ma sbagliate di una primitiva (segno,
    coefficiente, dimenticare +C non serve dato che lo aggiungiamo sempre
    in coda separatamente)."""
    pass


# ---------------------------------------------------------------
# A) integrali con sqrt(a+x^2): x^3/sqrt(a+x^2)
# ---------------------------------------------------------------
def gen_x3_sqrt(add, n=10):
    count = 0
    for a in [1, 4, 9, 16, 25, 2, 3, 5, 6, 7, 10, 11, 13]:
        if count >= n:
            break
        integrand = x**3 / sp.sqrt(a + x**2)
        F = sp.integrate(integrand, x)
        if not verify_integral(integrand, F, [0.3, 1.7, -2.3, 5.1, -6.6]):
            continue
        F_s = sp.latex(sp.simplify(F))
        text = r"Calcolare l'integrale \( \displaystyle\int \frac{x^3}{\sqrt{%d+x^2}}\,dx \)." % a
        correct = F_s + " + C"
        wrong1 = sp.latex(-sp.simplify(F)) + " + C"
        wrong2 = sp.latex(sp.simplify(F) / 3) + " + C"
        wrong3 = sp.latex(sp.simplify(x**2 * sp.sqrt(a + x**2) / 3)) + " + C"
        if add(text, correct, [wrong1, wrong2, wrong3]):
            count += 1


# ---------------------------------------------------------------
# B) ∫cos(ln x)dx e ∫sin(ln x)dx
# ---------------------------------------------------------------
def gen_cos_ln(add, n=6):
    count = 0
    for fn, fname in [(sp.cos, "\\cos"), (sp.sin, "\\sin")]:
        if count >= n:
            break
        integrand = fn(sp.log(x))
        F = sp.integrate(integrand, x)
        if not verify_integral(integrand, F, [0.5, 1.3, 2.7, 5.0]):
            continue
        F_s = sp.latex(F)
        text = r"Calcolare l'integrale \( \displaystyle\int %s(\ln(x))\,dx \)." % fname
        correct = F_s + " + C"
        wrong1 = sp.latex(-F) + " + C"
        other_fn = sp.sin if fn is sp.cos else sp.cos
        F_other = sp.integrate(other_fn(sp.log(x)), x)
        wrong2 = sp.latex(F_other) + " + C"
        wrong3 = sp.latex(x * fn(sp.log(x))) + " + C"
        if add(text, correct, [wrong1, wrong2, wrong3]):
            count += 1
    # variante con ln(kx)
    for k in [2, 3, sp.Rational(1, 2)]:
        if count >= n:
            break
        integrand = sp.cos(sp.log(k * x))
        F = sp.integrate(integrand, x)
        if not verify_integral(integrand, F, [0.5, 1.1, 2.2]):
            continue
        F_s = sp.latex(F)
        text = r"Calcolare l'integrale \( \displaystyle\int \cos(\ln(%sx))\,dx \)." % sp.latex(k)
        correct = F_s + " + C"
        wrong1 = sp.latex(-F) + " + C"
        wrong2 = sp.latex(x * sp.cos(sp.log(k * x))) + " + C"
        wrong3 = sp.latex(F.subs(x, x / k) if k != 1 else F) + " + C"
        if add(text, correct, [wrong1, wrong2, wrong3]):
            count += 1


# ---------------------------------------------------------------
# C) ∫x^n/(sqrt(x)(x+b))dx , sostituzione u=sqrt(x)
# ---------------------------------------------------------------
def gen_sqrtx_rational(add, n=10):
    count = 0
    xp = sp.symbols('x', positive=True)
    for b in [1, 2, 3, 4, 5, 6]:
        for p in (1, 2):
            if count >= n:
                break
            integrand = xp**p / (sp.sqrt(xp) * (xp + b))
            F = sp.integrate(integrand, xp)
            ok = True
            for xv in [0.3, 1.7, 4.1, 9.3]:
                d = complex(sp.N(sp.diff(F, xp).subs(xp, xv), 25))
                i = complex(sp.N(integrand.subs(xp, xv), 25))
                if abs(d - i) > 1e-8:
                    ok = False
                    break
            if not ok:
                continue
            F_s = sp.latex(sp.simplify(F))
            num_s = "x" if p == 1 else "x^2"
            text = r"Calcolare l'integrale \( \displaystyle\int \frac{%s}{\sqrt{x}\,(x+%d)}\,dx \) (per \(x>0\))." % (num_s, b)
            correct = F_s + " + C"
            wrong1 = sp.latex(-sp.simplify(F)) + " + C"
            wrong2 = sp.latex(sp.simplify(F) * 2) + " + C"
            wrong3 = sp.latex(sp.sqrt(xp) - sp.atan(sp.sqrt(xp))) + " + C"
            if add(text, correct, [wrong1, wrong2, wrong3]):
                count += 1


# ---------------------------------------------------------------
# D) ∫(x+p)/sqrt(x^2+ax+b)dx  con b - a^2/4 > 0 (radicando sempre positivo)
# ---------------------------------------------------------------
def gen_linear_over_sqrt_quad(add, n=10):
    count = 0
    tries = 0
    while count < n and tries < 100:
        tries += 1
        a = random.randint(-8, 8)
        b = random.randint(max(1, (a * a) // 4 + 1), (a * a) // 4 + 12)
        p = random.randint(-4, 4)
        m = sp.Rational(a, 2)
        k = b - m**2
        if k <= 0:
            continue
        coef = p - m
        quad_s = f"x^2{'+' if a>=0 else ''}{a}x{'+' if b>=0 else ''}{b}" if a != 0 else f"x^2{'+' if b>=0 else ''}{b}"
        p_s = f"+{p}" if p > 0 else (str(p) if p < 0 else "")
        text = r"Calcolare l'integrale \( \displaystyle\int \frac{x%s}{\sqrt{%s}}\,dx \)." % (p_s, quad_s)
        sqrt_term = f"\\sqrt{{{quad_s}}}"
        m_s = sp.latex(m)
        if coef == 0:
            correct = sqrt_term + " + C"
        else:
            correct = (r"%s %s %s\ln\left(x%s+%s\right)" %
                       (sqrt_term, "+" if coef > 0 else "-", sp.latex(abs(coef)),
                        ("+" if m >= 0 else "") + m_s if m != 0 else "", sqrt_term)) + " + C"
        # verifica numerica della formula "correct" costruita a mano
        F_manual = sp.sqrt(x**2 + a * x + b) + coef * sp.log(x + m + sp.sqrt(x**2 + a * x + b)) if coef != 0 else sp.sqrt(x**2 + a * x + b)
        integrand = (x + p) / sp.sqrt(x**2 + a * x + b)
        if not verify_integral(integrand, F_manual, [0.5, -1.2, 3.4, -4.7, 7.1]):
            continue
        wrong1 = sqrt_term + " + C"
        wrong2 = (r"%s %s %s\ln\left(x%s+%s\right)" %
                  (sqrt_term, "-" if coef > 0 else "+", sp.latex(abs(coef)),
                   ("+" if m >= 0 else "") + m_s if m != 0 else "", sqrt_term)) + " + C"
        wrong3 = (r"2%s %s %s\ln\left(x%s+%s\right)" %
                  (sqrt_term, "+" if coef > 0 else "-", sp.latex(abs(coef)),
                   ("+" if m >= 0 else "") + m_s if m != 0 else "", sqrt_term)) + " + C"
        if add(text, correct, [wrong1, wrong2, wrong3]):
            count += 1


# ---------------------------------------------------------------
# E) ∫(quadratica)/(quadratica)dx  (divisione polinomiale + arctan/ln)
# ---------------------------------------------------------------
def gen_quad_over_quad(add, n=10):
    count = 0
    tries = 0
    while count < n and tries < 150:
        tries += 1
        a1 = random.choice([1, 2, -1])
        b1 = random.randint(-5, 5)
        c1 = random.randint(-5, 5)
        num = a1 * x**2 + b1 * x + c1
        a2 = random.randint(-6, 6) or 1
        b2 = random.randint(-6, 6)
        den = x**2 + a2 * x + (b2 * b2 // 4 + random.randint(1, 8))  # discriminante negativo -> sempre >0
        if sp.simplify(den) == 0:
            continue
        integrand = num / den
        try:
            F = sp.integrate(integrand, x)
        except Exception:
            continue
        if F.has(sp.Integral):
            continue
        if not verify_integral(integrand, F, [0.4, -1.1, 2.3, -3.6]):
            continue
        num_s = f"{a1}x^2" if a1 not in (1, -1) else ("x^2" if a1 == 1 else "-x^2")
        if b1 == 1:
            num_s += "+x"
        elif b1 == -1:
            num_s += "-x"
        elif b1 > 0:
            num_s += f"+{b1}x"
        elif b1 < 0:
            num_s += f"{b1}x"
        num_s += (f"+{c1}" if c1 > 0 else (str(c1) if c1 < 0 else ""))
        a2v = den.coeff(x, 1)
        c2v = den.coeff(x, 0)
        if a2v == 1:
            den_s = "x^2+x"
        elif a2v == -1:
            den_s = "x^2-x"
        elif a2v > 0:
            den_s = f"x^2+{a2v}x"
        elif a2v < 0:
            den_s = f"x^2{a2v}x"
        else:
            den_s = "x^2"
        den_s += (f"+{c2v}" if c2v > 0 else (str(c2v) if c2v < 0 else ""))
        text = r"Calcolare l'integrale \( \displaystyle\int \frac{%s}{%s}\,dx \)." % (num_s, den_s)
        F_s = sp.latex(sp.simplify(F), ln_notation=True)
        correct = F_s + " + C"
        wrong1 = sp.latex(-sp.simplify(F), ln_notation=True) + " + C"
        wrong2 = sp.latex(sp.simplify(F) / 2, ln_notation=True) + " + C"
        wrong3 = sp.latex(sp.simplify(F).subs(x, 2 * x), ln_notation=True) + " + C"
        if add(text, correct, [wrong1, wrong2, wrong3]):
            count += 1


# ---------------------------------------------------------------
# F) integrali trigonometrici razionali: 1/sin^2, 1/cos^2, (tan^4x - c)/(tan x + k)
# ---------------------------------------------------------------
def gen_trig_rational(add, n=12):
    count = 0
    for fn, fname, F_manual in [
        (lambda t: 1 / sp.sin(t)**2, "\\sin^2", -sp.cos(x) / sp.sin(x)),
        (lambda t: 1 / sp.cos(t)**2, "\\cos^2", sp.sin(x) / sp.cos(x)),
    ]:
        if count >= n:
            break
        integrand = fn(x)
        if not verify_integral(integrand, F_manual, [0.5, 1.2, 2.5, 4.0]):
            continue
        text = r"Calcolare l'integrale \( \displaystyle\int \frac{1}{%s(x)}\,dx \)." % fname
        correct = sp.latex(F_manual) + " + C"
        wrong1 = sp.latex(-F_manual) + " + C"
        other = sp.sin(x) / sp.cos(x) if fname == "\\sin^2" else -sp.cos(x) / sp.sin(x)
        wrong2 = sp.latex(other) + " + C"
        wrong3 = sp.latex(sp.tan(x)) + " + C"
        if add(text, correct, [wrong1, wrong2, wrong3]):
            count += 1

    for c, k in [(4, sp.sqrt(2)), (1, 1), (2, 1), (1, 2), (9, 3), (4, 1)]:
        if count >= n:
            break
        integrand = (sp.tan(x)**4 - c) / (sp.tan(x) + k)
        try:
            F = sp.integrate(integrand, x)
        except Exception:
            continue
        if F.has(sp.Integral):
            continue
        if not verify_integral(integrand, F, [0.2, 0.5, 0.9, -0.3]):
            continue
        k_s = sp.latex(k)
        c_s = str(c)
        text = r"Calcolare l'integrale \( \displaystyle\int \frac{\tan^4(x)-%s}{\tan(x)+%s}\,dx \)." % (c_s, k_s)
        F_s = sp.latex(sp.simplify(F), ln_notation=True)
        correct = F_s + " + C"
        wrong1 = sp.latex(-sp.simplify(F), ln_notation=True) + " + C"
        wrong2 = sp.latex(sp.simplify(F) / 2, ln_notation=True) + " + C"
        wrong3 = sp.latex(sp.tan(x)**3 / 3 - k * sp.tan(x)**2 / 2, ln_notation=True) + " + C"
        if add(text, correct, [wrong1, wrong2, wrong3]):
            count += 1


def build():
    items, add = make_list()
    gen_x3_sqrt(add, n=10)
    gen_cos_ln(add, n=6)
    gen_sqrtx_rational(add, n=10)
    gen_linear_over_sqrt_quad(add, n=10)
    gen_quad_over_quad(add, n=10)
    gen_trig_rational(add, n=12)
    return items


if __name__ == "__main__":
    random.seed(555)
    items = build()
    print("Totale domande integrali stile esame:", len(items))
    bad = 0
    for it in items:
        opts = [it["correct"]] + it["wrong"]
        if len(set(opts)) != 4:
            bad += 1
            print("PROBLEMA:", it["text"])
    print("Domande con problemi:", bad)
    for it in items[:6]:
        print("-", it["text"])
        print("  =>", it["correct"])
