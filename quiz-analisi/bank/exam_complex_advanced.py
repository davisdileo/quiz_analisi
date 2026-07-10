# -*- coding: utf-8 -*-
"""Equazioni in \\(\\mathbb{C}\\) che mescolano \\(z\\), il coniugato
\\(\\bar z\\), il modulo \\(|z|\\), \\(\\operatorname{Re}(z)\\) e
\\(\\operatorname{Im}(z)\\) — esattamente come nel punto 1.(b) di ciascuna
delle 7 tracce d'esame caricate (es. \\(z+|z|^2=2\\), \\(z^2+i\\operatorname{Im}z+2\\bar z=0\\),
\\(iz^2-|z|^2=0\\), \\(z^2-z\\bar z+4iz=0\\), \\(|z|(z^3+8)=0\\)). Ogni
equazione viene risolta ponendo \\(z=x+iy\\) (x,y reali), separando parte
reale e immaginaria e risolvendo il sistema con sympy; le opzioni sbagliate
sono le soluzioni di varianti corrotte della stessa equazione (segno
cambiato, coefficiente diverso), quindi restano sempre matematicamente
distinte da quella corretta.
"""
import random
import sympy as sp

x, y = sp.symbols('x y', real=True)


def zexpr():
    return x + sp.I * y, x - sp.I * y, x**2 + y**2  # z, zbar, |z|^2


def wrap(s):
    return f"\\({s}\\)"


def solve_system(expr):
    expr = sp.expand(expr)
    re_part, im_part = expr.as_real_imag()
    try:
        sols = sp.solve([sp.Eq(re_part, 0), sp.Eq(im_part, 0)], [x, y], dict=True)
    except Exception:
        return None
    return sols


def format_solutions(sols):
    """Restituisce la stringa LaTeX dell'insieme delle soluzioni (solo se
    tutte numeriche/finite; altrimenti None)."""
    if sols is None or len(sols) == 0:
        return None
    zs = []
    for s in sols:
        if x not in s or y not in s:
            return None  # famiglia parametrica (infinite soluzioni) -> scarta
        xv, yv = sp.nsimplify(s[x]), sp.nsimplify(s[y])
        if xv.free_symbols or yv.free_symbols:
            return None
        if not (xv.is_real and yv.is_real):
            return None  # soluzione spuria non reale (x,y devono essere reali)
        zs.append((xv, yv))
    # dedup e ordina
    zs = sorted(set(zs), key=lambda t: (sp.N(t[0]), sp.N(t[1])))
    parts = []
    for xv, yv in zs:
        if yv == 0:
            parts.append(sp.latex(xv))
        elif xv == 0:
            parts.append(f"{sp.latex(yv)}i" if yv != 1 and yv != -1 else ("i" if yv == 1 else "-i"))
        else:
            yv_l = sp.latex(abs(yv))
            sign = "+" if yv > 0 else "-"
            coef = "" if abs(yv) == 1 else yv_l
            parts.append(f"{sp.latex(xv)}{sign}{coef}i")
    if not parts:
        return "\\emptyset"
    return "\\left\\{" + ",\\ ".join(parts) + "\\right\\}"


def verify_solutions(expr, sols):
    for s in sols:
        if x not in s or y not in s:
            return False
        val = sp.expand(expr.subs({x: s[x], y: s[y]}))
        if sp.simplify(sp.N(val)) != 0 and abs(complex(sp.N(val))) > 1e-9:
            return False
    return True


def make_list():
    out = []
    seen = set()

    def add(text, correct, wrong_candidates):
        """wrong_candidates può contenere più di 3 elementi (ed eventuali
        duplicati/None): si scelgono i primi 3 distinti dalla risposta
        corretta e tra loro."""
        wrongs = []
        seenw = {correct}
        for w in wrong_candidates:
            if not w or w in seenw:
                continue
            wrongs.append(w)
            seenw.add(w)
            if len(wrongs) == 3:
                break
        if len(wrongs) != 3:
            return False
        if text in seen:
            return False
        seen.add(text)
        out.append({"text": text, "correct": wrap(correct), "wrong": [wrap(w) for w in wrongs]})
        return True

    return out, add


# ---------------------------------------------------------------
# Famiglia 1: z + k|z|^2 = c   (stile "z + |z|^2 = 2")
# ---------------------------------------------------------------
def gen_family1(add, n=10):
    count = 0
    tries = 0
    while count < n and tries < 200:
        tries += 1
        k = random.choice([1, -1, 2, -2])
        c = random.randint(-6, 6)
        z, zbar, mod2 = zexpr()
        expr = z + k * mod2 - c
        sols = solve_system(expr)
        s_latex = format_solutions(sols)
        if s_latex is None or not verify_solutions(expr, sols):
            continue
        text = r"Risolvere in \(\mathbb{C}\) l'equazione \( z%s|z|^2=%d \)." % (("+" if k == 1 else ("-" if k == -1 else ("+" + str(k) if k > 0 else str(k)))), c)
        candidates = []
        for mod_variant, c_variant in [
            (-k, c), (k, c + 1), (k, c - 1), (2 * k, c), (k, -c), (-k, c + 1), (k + 1, c), (k - 1, c),
        ]:
            if mod_variant == 0:
                continue
            wsols = solve_system(z + mod_variant * mod2 - c_variant)
            candidates.append(format_solutions(wsols) or "\\emptyset")
        if add(text, s_latex, candidates):
            count += 1


# ---------------------------------------------------------------
# Famiglia 2: z^2 - z*zbar + k*i*z = 0   (stile "z^2 - z*zbar + 4iz = 0")
# Fattorizzando: z^2-z*zbar+kiz = (2y+k)(ix-y), quindi l'insieme delle
# soluzioni è SEMPRE la retta Im(z)=-k/2 unita al punto z=0 (verificato
# simbolicamente qui sotto per ogni k generato).
# ---------------------------------------------------------------
def gen_family2(add, n=8):
    count = 0
    for k in [1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, -6]:
        if count >= n:
            break
        z, zbar, mod2 = zexpr()
        expr = sp.expand(z**2 - z * zbar + k * sp.I * z)
        factored = sp.factor(expr / sp.I) * sp.I  # forza la forma fattorizzata attesa
        # verifica simbolica: l'espressione si annulla su tutta la retta y=-k/2 e nel punto (0,0)
        check_line = sp.simplify(expr.subs(y, -sp.Rational(k, 2)))
        check_origin = sp.simplify(expr.subs({x: 0, y: 0}))
        if check_line != 0 or check_origin != 0:
            continue
        k_half = sp.Rational(k, 2)

        def kterm(kk):
            """Formatta '+ki' con segno corretto, senza doppio segno, per il testo dell'equazione."""
            if kk == 1:
                return "+i"
            if kk == -1:
                return "-i"
            return ("+%di" % kk) if kk > 0 else ("%di" % kk)

        def yi_term(val):
            """Formatta '-val*i' (val può essere negativo) come singolo termine con segno pulito,
            per l'insieme soluzione 'z = x + (termine)'."""
            if val == 0:
                return ""
            av = abs(val)
            coef = "" if av == 1 else sp.latex(av)
            sign = "-" if val > 0 else "+"
            return f"{sign}{coef}i"

        text = r"Determinare le soluzioni \(z\in\mathbb{C}\) dell'equazione \( z^2-z\bar z%s z=0 \)." % kterm(k)
        correct = r"\left\{z=x%s\,:\,x\in\mathbb{R}\right\}\cup\{0\}" % yi_term(k_half)
        candidates = [
            r"\left\{z=x%s\,:\,x\in\mathbb{R}\right\}\cup\{0\}" % yi_term(-k_half),
            r"\left\{z=%s+iy\,:\,y\in\mathbb{R}\right\}\cup\{0\}" % sp.latex(k_half),
            r"\left\{z=x%s\,:\,x\in\mathbb{R}\right\}" % yi_term(k_half),
            r"\{0\}",
            r"\left\{z=x%s\,:\,x\in\mathbb{R}\right\}\cup\{0\}" % yi_term(2 * k_half),
        ]
        if add(text, correct, candidates):
            count += 1


# ---------------------------------------------------------------
# Famiglia 3: z + a*i + Re(z)*(i + Im(z)^2) = 0
# ---------------------------------------------------------------
def gen_family3(add, n=8):
    count = 0
    tries = 0
    while count < n and tries < 200:
        tries += 1
        a = random.randint(-5, 5)
        if a == 0:
            continue
        z, zbar, mod2 = zexpr()
        expr = z + a * sp.I + x * (sp.I + y**2)
        sols = solve_system(expr)
        s_latex = format_solutions(sols)
        if s_latex is None or not verify_solutions(expr, sols):
            continue
        if a == 1:
            a_s = "+i"
        elif a == -1:
            a_s = "-i"
        else:
            a_s = (f"+{a}i" if a > 0 else f"{a}i")
        text = r"Risolvere in \(\mathbb{C}\) l'equazione \( z%s+\operatorname{Re}(z)\left(i+(\operatorname{Im}z)^2\right)=0 \)." % a_s
        candidates = []
        for av, expr_variant in [
            (-a, x * (sp.I + y**2)), (a, x * (sp.I - y**2)), (a, y * (sp.I + y**2)),
            (a + 1, x * (sp.I + y**2)), (a - 1, x * (sp.I + y**2)), (a, x * (sp.I + y**2) + 1),
        ]:
            wsols = solve_system(z + av * sp.I + expr_variant)
            candidates.append(format_solutions(wsols) or "\\emptyset")
        if add(text, s_latex, candidates):
            count += 1


# ---------------------------------------------------------------
# Famiglia 4: |z|(z^n + c) = 0   (stile "|z|(z^3+8) = 0")
# -> z=0 oppure z^n = -c (radici n-esime, forma trigonometrica se -c non
# è una potenza perfetta, altrimenti forma algebrica esatta)
# ---------------------------------------------------------------
def gen_family4(add, n=10):
    count = 0
    perfect_cases = [(3, 8), (3, -8), (3, -27), (3, 27), (3, 1), (3, -1), (3, 64), (3, -64), (3, 125), (3, -125)]
    random.shuffle(perfect_cases)
    for nn, c in perfect_cases:
        if count >= n:
            break
        target = -c
        # radice reale immediata se nn=2 o 3 e target è una potenza perfetta (positiva o negativa)
        if target >= 0:
            real_root = sp.nsimplify(target) ** sp.Rational(1, nn)
        else:
            real_root = -((-target) ** sp.Rational(1, nn))
        real_root = sp.nsimplify(real_root)
        if not real_root.is_rational:
            continue
        r = abs(target) ** sp.Rational(1, nn)
        theta = "0" if target >= 0 else "\\pi"
        text = r"Risolvere in \(\mathbb{C}\) l'equazione \( |z|\left(z^{%d}%s\right)=0 \)." % (nn, ("+" + str(c)) if c > 0 else str(c))
        # radici n-esime di target in forma trigonometrica generale + z=0
        correct = (r"\left\{0\right\}\cup\left\{\sqrt[%d]{%d}\left(\cos\frac{%s+2k\pi}{%d}+i\sin\frac{%s+2k\pi}{%d}\right),\ k=0,\dots,%d\right\}"
                   % (nn, abs(target), theta, nn, theta, nn, nn - 1))
        wrong1 = (r"\left\{\sqrt[%d]{%d}\left(\cos\frac{%s+2k\pi}{%d}+i\sin\frac{%s+2k\pi}{%d}\right),\ k=0,\dots,%d\right\}"
                  % (nn, abs(target), theta, nn, theta, nn, nn - 1))  # dimentica z=0
        wrong_theta = "\\pi" if theta == "0" else "0"
        wrong2 = (r"\left\{0\right\}\cup\left\{\sqrt[%d]{%d}\left(\cos\frac{%s+2k\pi}{%d}+i\sin\frac{%s+2k\pi}{%d}\right),\ k=0,\dots,%d\right\}"
                  % (nn, abs(target), wrong_theta, nn, wrong_theta, nn, nn - 1))  # segno di c sbagliato
        wrong3 = r"\left\{0\right\}"  # dimentica le radici n-esime
        if add(text, correct, [wrong1, wrong2, wrong3]):
            count += 1


def build():
    items, add = make_list()
    gen_family1(add, n=10)
    gen_family2(add, n=8)
    gen_family3(add, n=8)
    gen_family4(add, n=8)
    return items


if __name__ == "__main__":
    random.seed(321)
    items = build()
    print("Totale domande equazioni complesse avanzate:", len(items))
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
