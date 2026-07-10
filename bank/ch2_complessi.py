# -*- coding: utf-8 -*-
"""Capitolo 2 - Numeri complessi: generazione verificata con sympy."""
import random
import sympy as sp

I = sp.I


def fmt_complex(z):
    z = sp.nsimplify(sp.simplify(z))
    re, im = sp.re(z), sp.im(z)
    if im == 0:
        return sp.latex(re)
    if re == 0:
        if im == 1:
            return "i"
        if im == -1:
            return "-i"
        return f"{sp.latex(im)}i"
    sign = "+" if im > 0 else "-"
    im_abs = abs(im)
    im_str = "i" if im_abs == 1 else f"{sp.latex(im_abs)}i"
    return f"{sp.latex(re)} {sign} {im_str}"


def wrap(s):
    return f"\\({s}\\)"


def lin_term(coef, var="z"):
    if coef == 1:
        return var
    if coef == -1:
        return f"-{var}"
    return f"{coef}{var}"


def signed(n):
    if n == 0:
        return ""
    return f"+ {n}" if n > 0 else f"- {-n}"


def complex_distractors(val, n_wanted=3):
    """Genera candidati distrattori plausibili per un numero complesso val,
    filtra quelli coincidenti con la risposta corretta o tra loro."""
    re, im = sp.re(val), sp.im(val)
    candidates = [
        -re - im * I,      # segno opposto su entrambe le parti
        re - im * I,       # coniugato
        -re + im * I,      # segno opposto sulla sola parte reale
        im + re * I,       # parti scambiate
        -im + re * I,      # parti scambiate con segno
        re + im * I + 1,   # piccola perturbazione (fallback)
        re + im * I - 1,
        (re + 1) + im * I,
        re + (im + 1) * I,
    ]
    correct_s = fmt_complex(val)
    out, seen = [], {correct_s}
    for c in candidates:
        s = fmt_complex(c)
        if s not in seen:
            out.append(s)
            seen.add(s)
        if len(out) == n_wanted:
            break
    return out


def dedupe_wrong(correct, candidates):
    out, seen = [], {correct}
    for c in candidates:
        if c not in seen:
            out.append(c)
            seen.add(c)
        if len(out) == 3:
            return out
    return out  # potrebbe essere < 3 in rarissimi casi degeneri; gestito a monte


def build():
    items = []
    seen_texts = set()

    def add(text, correct, wrong):
        if len(set([correct] + wrong)) != 4:
            return False  # scarta domande con opzioni non tutte distinte
        if text in seen_texts:
            return False
        seen_texts.add(text)
        items.append({"text": text, "correct": correct, "wrong": wrong})
        return True

    def zlatex(a, b):
        if b == 0:
            return f"{a}"
        sign = "+" if b >= 0 else "-"
        bb = abs(b)
        bterm = "i" if bb == 1 else f"{bb}i"
        return f"{a} {sign} {bterm}" if a != 0 else (f"{bterm}" if b > 0 else f"-{bterm}")

    # ---- C1: potenza (a+bi)^n ----
    combos = [(a, b, n) for a in range(-4, 5) for b in range(-4, 5)
              for n in (2, 3, 4) if not (a == 0 and b == 0) and abs(a) + abs(b) <= 6]
    random.shuffle(combos)
    count = 0
    for a, b, n in combos:
        if count >= 10:
            break
        val = sp.expand((a + b * I) ** n)
        correct = wrap(fmt_complex(val))
        wrong = [wrap(w) for w in complex_distractors(val)]
        text = r"Calcolare \( (%s)^{%d} \)." % (zlatex(a, b), n)
        if add(text, correct, wrong):
            count += 1

    # ---- C2: modulo di z=a+bi ----
    combos = [(a, b) for a in range(-9, 10) for b in range(-9, 10) if not (a == 0 and b == 0)]
    random.shuffle(combos)
    count = 0
    for a, b in combos:
        if count >= 10:
            break
        mod = sp.sqrt(a ** 2 + b ** 2)
        text = r"Calcolare il modulo del numero complesso \( z = %s \)." % zlatex(a, b)
        correct = wrap(sp.latex(mod))
        cand = [sp.Abs(a) + sp.Abs(b), a ** 2 + b ** 2,
                sp.sqrt(sp.Abs(a * b)) if a * b != 0 else sp.sqrt(sp.Abs(a) + sp.Abs(b) + 1),
                sp.sqrt(sp.Abs(a - b))]
        wrong_s = []
        seen = {sp.latex(mod)}
        for w in cand:
            s = sp.latex(sp.simplify(w))
            if s not in seen:
                wrong_s.append(s)
                seen.add(s)
            if len(wrong_s) == 3:
                break
        wrong = [wrap(w) for w in wrong_s]
        if add(text, correct, wrong):
            count += 1

    # ---- C3: reciproco 1/z ----
    combos = [(a, b) for a in range(-6, 7) for b in range(-6, 7) if not (a == 0 and b == 0)]
    random.shuffle(combos)
    count = 0
    for a, b in combos:
        if count >= 8:
            break
        den = a ** 2 + b ** 2
        val = sp.Rational(a, den) - sp.Rational(b, den) * I
        text = r"Calcolare \( \dfrac{1}{z} \), dove \( z = %s \)." % zlatex(a, b)
        correct = wrap(fmt_complex(val))
        wrong = [wrap(w) for w in complex_distractors(val)]
        if add(text, correct, wrong):
            count += 1

    # ---- C4: radici n-esime di un numero reale ----
    reals_n = [(-8, 3), (8, 3), (-27, 3), (27, 3), (-1, 3), (1, 4), (-1, 4), (16, 4),
               (-16, 4), (81, 4), (-64, 3), (64, 3), (-125, 3), (125, 3), (4, 2), (9, 2),
               (-4, 2), (25, 2), (36, 2), (49, 2)]
    random.shuffle(reals_n)
    count = 0
    x = sp.symbols('x')
    nome = {2: "quadrata", 3: "cubica", 4: "quarta"}
    for r, n in reals_n:
        if count >= 10:
            break
        roots = [sp.nsimplify(sp.simplify(rt)) for rt in sp.solve(sp.Eq(x ** n, r), x)]
        roots_fmt = set(fmt_complex(rt) for rt in roots)
        # candidato "falso": una radice reale con il segno cambiato rispetto a quella vera,
        # verificata (con sympy) NON essere effettivamente una radice
        real_roots = [rt for rt in roots if sp.im(rt) == 0]
        if not real_roots:
            continue
        base = real_roots[0]
        fake_candidates = [-base, base + 1, base - 1, base * 2, base + 2, -base + 1, -base - 1]
        fake_val = None
        for fc in fake_candidates:
            if fc == 0:
                continue
            if sp.simplify(fc ** n - r) != 0:
                fake_val = fc
                break
        if fake_val is None:
            continue
        fake_s = fmt_complex(fake_val)
        if fake_s in roots_fmt:
            continue
        # 3 distrattori = 3 radici vere diverse (se sono almeno 3, altrimenti scarta)
        distractor_roots = [f for f in roots_fmt][:3]
        if len(distractor_roots) < 3:
            continue
        text = r"Quale dei seguenti NON è una radice %s di \( %d \)?" % (nome[n], r)
        correct = wrap(fake_s)
        wrong = [wrap(w) for w in distractor_roots]
        if add(text, correct, wrong):
            count += 1

    # ---- C5: forma algebrica da modulo/argomento ----
    angle_defs = [
        (sp.pi / 6, "\\pi/6"), (sp.pi / 4, "\\pi/4"), (sp.pi / 3, "\\pi/3"),
        (sp.pi / 2, "\\pi/2"), (2 * sp.pi / 3, "2\\pi/3"), (3 * sp.pi / 4, "3\\pi/4"),
        (5 * sp.pi / 6, "5\\pi/6"), (sp.pi, "\\pi"),
    ]
    rhos = [1, 2, 3, 4, 6]
    combos = [(rho, ang, s) for rho in rhos for ang, s in angle_defs]
    random.shuffle(combos)
    count = 0
    for rho, ang, ang_s in combos:
        if count >= 8:
            break
        val = sp.nsimplify(sp.simplify(rho * (sp.cos(ang) + I * sp.sin(ang))))
        text = (r"Scrivere in forma algebrica \( a+bi \) il numero complesso con modulo \( %d \) "
                r"e argomento \( %s \).") % (rho, ang_s)
        correct = wrap(fmt_complex(val))
        wrong = [wrap(w) for w in complex_distractors(val)]
        if add(text, correct, wrong):
            count += 1

    # ---- C6: equazioni quadratiche a discriminante negativo ----
    combos = [(p, q) for p in range(-8, 9) for q in range(1, 15)]
    random.shuffle(combos)
    count = 0
    z = sp.symbols('z')
    for p, q in combos:
        if count >= 8:
            break
        disc = p ** 2 - 4 * q
        if disc >= 0:
            continue
        roots = sp.solve(sp.Eq(z ** 2 + p * z + q, 0), z)
        r0 = sp.nsimplify(sp.simplify(roots[0]))
        expr = "z^2" + (" " + signed(p).replace(str(abs(p)), lin_term(abs(p) if p!=0 else 0)[0:] , 1) if False else "")
        # costruzione pulita del termine lineare (evita "1z"/"-1z")
        if p == 0:
            mid = ""
        elif p == 1:
            mid = " + z"
        elif p == -1:
            mid = " - z"
        else:
            mid = f" + {p}z" if p > 0 else f" - {-p}z"
        expr = "z^2" + mid + f" + {q}"
        text = r"Risolvere in \( \mathbb{C} \) l'equazione \( %s = 0 \) e indicare una soluzione." % expr
        correct = wrap(fmt_complex(r0))
        wrong = [wrap(w) for w in complex_distractors(r0)]
        if add(text, correct, wrong):
            count += 1

    # ---- C7: luogo |z - z1| = |z - z2| ----
    pts = [(-3, 0), (-2, 1), (-1, -2), (0, 3), (1, 1), (2, -1), (3, 2), (-2, -3), (4, 0), (0, -4), (1, -3), (-1, 4)]
    random.shuffle(pts)
    pairs = [(pts[i], pts[i + 1]) for i in range(0, len(pts) - 1, 2)]
    count = 0
    xs, ys = sp.symbols('x y', real=True)
    for (x1, y1), (x2, y2) in pairs:
        if count >= 6:
            break
        lhs = (xs - x1) ** 2 + (ys - y1) ** 2
        rhs = (xs - x2) ** 2 + (ys - y2) ** 2
        diff = sp.expand(lhs - rhs)
        A = diff.coeff(xs, 1).subs({ys: 0})
        B = diff.coeff(ys, 1).subs({xs: 0})
        C = diff.subs({xs: 0, ys: 0})
        if A == 0 and B == 0:
            continue
        g = sp.gcd(sp.gcd(A, B), C) if C != 0 else sp.gcd(A, B)
        if g != 0:
            A, B, C = A / g, B / g, C / g
        parts = []
        if A != 0:
            parts.append(f"{sp.latex(A)}x" if abs(A) != 1 else ("x" if A == 1 else "-x"))
        if B != 0:
            bterm = f"{sp.latex(abs(B))}y" if abs(B) != 1 else "y"
            parts.append((("+ " if B > 0 else "- ") + bterm) if parts else (bterm if B > 0 else f"-{bterm}"))
        if C != 0:
            parts.append((("+ " if C > 0 else "- ") + f"{sp.latex(abs(C))}") if parts else f"{sp.latex(C)}")
        eq_str = " ".join(parts) + " = 0"
        z1_s = zlatex(x1, y1)
        z2_s = zlatex(x2, y2)
        text = (r"Il luogo dei punti \( z=x+iy \) tali che \( |z-(%s)| = |z-(%s)| \) "
                r"è rappresentato dall'equazione:") % (z1_s, z2_s)
        correct = wrap(eq_str)
        base_no_eq = eq_str.rsplit(" = 0", 1)[0]
        wrong_candidates = [f"{base_no_eq} = 1", "x^2 + y^2 = 1", ("y = 0" if "y" in base_no_eq and A != 0 else "x = 0")]
        wrong = []
        seen = {eq_str}
        for w in wrong_candidates:
            if w not in seen:
                wrong.append(wrap(w))
                seen.add(w)
        if len(wrong) < 3:
            wrong.append(wrap("x + y = 0"))
        if add(text, correct, wrong[:3]):
            count += 1

    # ---- C8: potenze di i ----
    ns = [5, 6, 7, 9, 10, 11, 13, 14, 15, 18, 21, 22, 23, 26, 29, 33, 34, 37, 41, 50]
    random.shuffle(ns)
    count = 0
    for n in ns:
        if count >= 8:
            break
        val = sp.simplify(I ** n)
        text = r"Calcolare \( i^{%d} \)." % n
        correct = wrap(fmt_complex(val))
        all_vals = [1, I, -1, -I]
        wrong_s = [fmt_complex(v) for v in all_vals if fmt_complex(v) != fmt_complex(val)]
        wrong = [wrap(w) for w in wrong_s[:3]]
        if add(text, correct, wrong):
            count += 1

    return items


if __name__ == "__main__":
    random.seed(202)
    items = build()
    print("Totale domande generate (Capitolo 2):", len(items))
    bad = 0
    for it in items:
        opts = [it["correct"]] + it["wrong"]
        if len(set(opts)) != 4:
            bad += 1
            print("DUPLICATO:", it["text"], opts)
        if len(it["wrong"]) != 3:
            bad += 1
            print("MANCANO OPZIONI:", it["text"], it["wrong"])
    print("Domande con problemi:", bad)
