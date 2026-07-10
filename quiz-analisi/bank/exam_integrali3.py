# -*- coding: utf-8 -*-
"""Nuovi integrali nello stile delle 7 tracce d'esame caricate (punto 3 di
ciascuna traccia): \\(\\int (3x+1)/(2x+5)\\,dx\\), \\(\\int e^x\\tan(e^x)\\,dx\\),
\\(\\int e^x\\sin(2x)\\,dx\\), \\(\\int \\ln x/(x(1+\\ln^2x))\\,dx\\),
\\(\\int e^x/\\sqrt{e^x+1}\\cdot\\sin(\\sqrt{e^x+1})\\,dx\\),
\\(\\int x\\arcsin(x^2)/\\sqrt{1-x^4}\\,dx\\),
\\(\\int x\\ln^3(6x^2+1)/(2+12x^2)\\,dx\\).

Ogni primitiva viene calcolata con sympy (o in forma chiusa derivata a
mano quando sympy non riesce) e SEMPRE verificata numericamente
derivandola e confrontandola con l'integranda in piu' punti del dominio
(stesso metodo robusto di exam_integrali.py), cosi' da scartare qualsiasi
errore di segno o di costante.
"""
import random
import sympy as sp

x = sp.symbols('x', real=True)
xp = sp.symbols('x', positive=True)


def wrap(s):
    return f"\\({s}\\)"


def verify_integral(integrand, F, points, var=x):
    for xv in points:
        try:
            d = complex(sp.N(sp.diff(F, var).subs(var, xv), 25))
            i = complex(sp.N(integrand.subs(var, xv), 25))
        except Exception:
            return False
        if abs(d - i) > 1e-7:
            return False
    return True


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


# ---------------------------------------------------------------
# 1) integrale di funzione razionale lineare/lineare: (ax+b)/(cx+d)
# ---------------------------------------------------------------
def gen_linear_over_linear(add, n=8):
    count = 0
    tries = 0
    while count < n and tries < 200:
        tries += 1
        a = random.choice([1, 2, 3, -1, -2])
        b = random.randint(-5, 5)
        c = random.choice([1, 2, 3, -1, -2])
        d = random.randint(-6, 6)
        if c == 0 or sp.gcd(a, c) == max(abs(a), abs(c)):  # evita a/c intero banale troppo semplice a volte ok comunque
            pass
        if d == 0:
            continue
        integrand = (a * x + b) / (c * x + d)
        try:
            F = sp.integrate(integrand, x)
        except Exception:
            continue
        if F.has(sp.Integral):
            continue
        root = sp.nsimplify(sp.Rational(-d, c))
        pts = [float(root) + 0.7, float(root) - 1.3, float(root) + 3.1, float(root) - 2.4]
        if not verify_integral(integrand, F, pts):
            continue
        b_s = f"+{b}" if b > 0 else (str(b) if b < 0 else "")
        d_s = f"+{d}" if d > 0 else (str(d) if d < 0 else "")
        a_s = "" if a == 1 else ("-" if a == -1 else str(a))
        c_s = "" if c == 1 else ("-" if c == -1 else str(c))
        text = r"Calcolare l'integrale \( \displaystyle\int \frac{%sx%s}{%sx%s}\,dx \)." % (a_s, b_s, c_s, d_s)
        F_s = sp.latex(sp.simplify(F), ln_notation=True)
        correct = F_s + " + C"
        wrong1 = sp.latex(-sp.simplify(F), ln_notation=True) + " + C"
        wrong2 = sp.latex(sp.simplify(F) / 2, ln_notation=True) + " + C"
        wrong3 = sp.latex(sp.Rational(a, c) * x, ln_notation=True) + " + C"
        if add(text, correct, [wrong1, wrong2, wrong3]):
            count += 1


# ---------------------------------------------------------------
# 2) ∫ e^x tan(k e^x) dx   (sost. u = k e^x)
# ---------------------------------------------------------------
def gen_exp_tan(add, n=6):
    count = 0
    for k in [1, 2, 3, sp.Rational(1, 2), sp.Rational(3, 2)]:
        if count >= n:
            break
        integrand = sp.exp(x) * sp.tan(k * sp.exp(x))
        F = -sp.log(sp.cos(k * sp.exp(x))) / k  # forma chiusa: u=k e^x, du=k e^x dx => (1/k)∫tan(u)du = -(1/k)ln|cos u|
        # punti campione con k*e^x < 1.4 (margine di sicurezza sotto pi/2)
        import math
        bound = math.log(1.4 / float(k))
        pts = [bound - 2.0, bound - 1.2, bound - 0.6, bound - 0.15]
        if not verify_integral(integrand, F, pts):
            continue
        k_s = "" if k == 1 else sp.latex(k)
        text = r"Calcolare l'integrale \( \displaystyle\int e^{x}\tan(%se^{x})\,dx \)." % k_s
        F_s = sp.latex(F, ln_notation=True)
        correct = F_s + " + C"
        pool = [
            sp.latex(-F, ln_notation=True) + " + C",  # segno cambiato
            sp.latex(sp.log(sp.sin(k * sp.exp(x))) / k, ln_notation=True) + " + C",  # sin invece di cos
            sp.latex(-sp.log(sp.cos(k * sp.exp(x))) * k, ln_notation=True) + " + C",  # moltiplica per k invece di dividere
            sp.latex(-sp.log(sp.cos(sp.exp(x))) / k, ln_notation=True) + " + C",  # dimentica k dentro l'argomento
            sp.latex(F * 2, ln_notation=True) + " + C",
        ]
        wrongs = []
        seenw = {correct}
        for w in pool:
            if w in seenw:
                continue
            wrongs.append(w)
            seenw.add(w)
            if len(wrongs) == 3:
                break
        if len(wrongs) == 3 and add(text, correct, wrongs):
            count += 1


# ---------------------------------------------------------------
# 3) ∫ e^{a x} sin(b x) dx  (formula di riduzione classica)
# ---------------------------------------------------------------
def gen_exp_sin(add, n=8):
    count = 0
    tries = 0
    used = set()
    while count < n and tries < 100:
        tries += 1
        a = random.choice([1, 2, -1])
        b = random.choice([1, 2, 3, -2])
        if (a, b) in used:
            continue
        used.add((a, b))
        integrand = sp.exp(a * x) * sp.sin(b * x)
        F = sp.exp(a * x) * (a * sp.sin(b * x) - b * sp.cos(b * x)) / (a**2 + b**2)
        if not verify_integral(integrand, F, [0.3, -0.7, 1.5, -1.9]):
            continue
        a_s = "" if a == 1 else ("-" if a == -1 else str(a))
        b_s = "" if b == 1 else ("-" if b == -1 else str(b))
        text = r"Calcolare l'integrale \( \displaystyle\int e^{%sx}\sin(%sx)\,dx \)." % (a_s, b_s)
        F_s = sp.latex(sp.simplify(F))
        correct = F_s + " + C"
        wrong1 = sp.latex(-sp.simplify(F)) + " + C"
        F_cos_swap = sp.exp(a * x) * (b * sp.sin(b * x) + a * sp.cos(b * x)) / (a**2 + b**2)
        wrong2 = sp.latex(sp.simplify(F_cos_swap)) + " + C"
        wrong3 = sp.latex(sp.simplify(F) * 2) + " + C"
        if add(text, correct, [wrong1, wrong2, wrong3]):
            count += 1


# ---------------------------------------------------------------
# 4) ∫ ln x / (x (k + ln^2 x)) dx = (1/2) ln(k+ln^2 x)   (x>0)
# ---------------------------------------------------------------
def gen_ln_over_x_quad(add, n=6):
    count = 0
    for k in [1, 2, 3, 4, sp.Rational(1, 2)]:
        if count >= n:
            break
        integrand = sp.log(xp) / (xp * (k + sp.log(xp)**2))
        F = sp.log(k + sp.log(xp)**2) / 2
        if not verify_integral(integrand, F, [0.5, 1.0, 2.0, 3.5, 5.0], var=xp):
            continue
        k_s = sp.latex(k)
        text = r"Calcolare l'integrale \( \displaystyle\int \frac{\ln x}{x\left(%s+\ln^2 x\right)}\,dx \) (per \(x>0\))." % k_s
        F_s = sp.latex(F, ln_notation=True)
        correct = F_s + " + C"
        wrong1 = sp.latex(-F, ln_notation=True) + " + C"
        wrong2 = sp.latex(sp.log(k + sp.log(xp)**2), ln_notation=True) + " + C"
        wrong3 = sp.latex(sp.log(xp)**2 / 2, ln_notation=True) + " + C"
        if add(text, correct, [wrong1, wrong2, wrong3]):
            count += 1


# ---------------------------------------------------------------
# 5) ∫ e^x / sqrt(e^x + c) * sin(sqrt(e^x + c)) dx = -2 cos(sqrt(e^x+c))
# ---------------------------------------------------------------
def gen_exp_sqrt_sin(add, n=6):
    count = 0
    for c in [1, 2, 3, 4, sp.Rational(1, 2)]:
        if count >= n:
            break
        u = sp.sqrt(sp.exp(x) + c)
        integrand = sp.exp(x) / u * sp.sin(u)
        F = -2 * sp.cos(u)
        if not verify_integral(integrand, F, [-1.5, -0.3, 0.4, 1.6, 2.5]):
            continue
        c_s = f"+{sp.latex(c)}" if c != 0 else ""
        text = r"Calcolare l'integrale \( \displaystyle\int \frac{e^{x}}{\sqrt{e^{x}%s}}\sin\!\left(\sqrt{e^{x}%s}\right)dx \)." % (c_s, c_s)
        F_s = sp.latex(F)
        correct = F_s + " + C"
        wrong1 = sp.latex(-F) + " + C"
        wrong2 = sp.latex(2 * sp.sin(u)) + " + C"
        wrong3 = sp.latex(-sp.cos(u)) + " + C"
        if add(text, correct, [wrong1, wrong2, wrong3]):
            count += 1


# ---------------------------------------------------------------
# 6) ∫ x arcsin(a x^2)/sqrt(1-a^2 x^4) dx = arcsin(a x^2)^2/(4a)
# ---------------------------------------------------------------
def gen_x_arcsin_x2(add, n=6):
    count = 0
    for a in [1, 2, 3, sp.Rational(1, 2), sp.Rational(1, 4)]:
        if count >= n:
            break
        integrand = x * sp.asin(a * x**2) / sp.sqrt(1 - a**2 * x**4)
        F = sp.asin(a * x**2)**2 / (4 * a)
        bound = float(sp.sqrt(1 / a)) ** 0.5 if False else (1 / float(a)) ** 0.5
        pts = [0.2 * bound, 0.45 * bound, 0.7 * bound, -0.3 * bound, -0.6 * bound]
        if not verify_integral(integrand, F, pts):
            continue
        a_s = "" if a == 1 else sp.latex(a)
        text = r"Calcolare l'integrale \( \displaystyle\int \frac{x\arcsin(%sx^2)}{\sqrt{1-%sx^4}}\,dx \) (nel dominio di definizione)." % (a_s, sp.latex(a**2) if a != 1 else "")
        F_s = sp.latex(F)
        correct = F_s + " + C"
        wrong1 = sp.latex(-F) + " + C"
        wrong2 = sp.latex(sp.asin(a * x**2)**2 / 2) + " + C"
        wrong3 = sp.latex(sp.asin(a * x**2) / (2 * a)) + " + C"
        if add(text, correct, [wrong1, wrong2, wrong3]):
            count += 1


# ---------------------------------------------------------------
# 7) ∫ x ln^3(a x^2+1) / (m + a m x^2) dx = ln^4(a x^2+1) / (8 a m)
#    (stile "x ln^3(6x^2+1)/(2+12x^2)": qui a=6, m=2)
# ---------------------------------------------------------------
def gen_x_ln3_over_quad(add, n=6):
    count = 0
    for a, m in [(6, 2), (2, 1), (3, 1), (4, 2), (2, 3), (1, 1)]:
        if count >= n:
            break
        u = a * x**2 + 1
        integrand = x * sp.log(u)**3 / (m + a * m * x**2)
        F = sp.log(u)**4 / (8 * a * m)
        if not verify_integral(integrand, F, [0.3, 0.7, 1.2, -0.5, -1.1]):
            continue
        m_s = str(m)
        am = a * m
        am_s = "" if am == 1 else str(am)
        a_s = "" if a == 1 else str(a)
        text = r"Calcolare l'integrale \( \displaystyle\int \frac{x\ln^3(%sx^2+1)}{%s+%sx^2}\,dx \)." % (a_s, m_s, am_s)
        F_s = sp.latex(F, ln_notation=True)
        correct = F_s + " + C"
        wrong1 = sp.latex(-F, ln_notation=True) + " + C"
        wrong2 = sp.latex(sp.log(u)**4 / (2 * a * m), ln_notation=True) + " + C"
        wrong3 = sp.latex(sp.log(u)**3 / (8 * a * m), ln_notation=True) + " + C"
        if add(text, correct, [wrong1, wrong2, wrong3]):
            count += 1


def build():
    items, add = make_list()
    gen_linear_over_linear(add, n=8)
    gen_exp_tan(add, n=5)
    gen_exp_sin(add, n=8)
    gen_ln_over_x_quad(add, n=5)
    gen_exp_sqrt_sin(add, n=5)
    gen_x_arcsin_x2(add, n=5)
    gen_x_ln3_over_quad(add, n=6)
    return items


if __name__ == "__main__":
    random.seed(999)
    items = build()
    print("Totale nuovi integrali:", len(items))
    bad = 0
    for it in items:
        opts = [it["correct"]] + it["wrong"]
        if len(set(opts)) != 4:
            bad += 1
            print("PROBLEMA:", it["text"])
    print("Domande con problemi:", bad)
    for it in items:
        print("-", it["text"])
        print("  =>", it["correct"])
