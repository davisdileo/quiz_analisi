# -*- coding: utf-8 -*-
"""Semplificazione di espressioni trigonometriche/trigonometriche-inverse
composte, esattamente nello stile delle tracce d'esame del docente:
sin(arctan(-1/3)), sin(arccos(-1/3)), cos(arctan(1/2)), arctan(tan(2pi/3)),
arctan(tan(3pi/4)). I valori esatti sono calcolati numericamente ad alta
precisione e riconosciuti in forma chiusa con sp.nsimplify (poi verificati
di nuovo per sicurezza), cosi' da coprire in automatico tutte le identita'
di riduzione al primo/quarto quadrante senza doverle scrivere a mano.
"""
import random
import sympy as sp

RADICALS = [sp.sqrt(n) for n in (2, 3, 5, 6, 7, 10, 11, 13, 14, 17, 19, 21, 26)]


def wrap(s):
    return f"\\({s}\\)"


def exact_value(expr):
    v = sp.N(expr, 40)
    cand = sp.nsimplify(v, RADICALS + [sp.pi], rational=False)
    if cand is not None and abs(sp.N(cand, 40) - v) < sp.Float(10) ** -25:
        return sp.radsimp(cand)
    cand2 = sp.nsimplify(v, RADICALS + [sp.pi], rational=True)
    if cand2 is not None and abs(sp.N(cand2, 40) - v) < sp.Float(10) ** -25:
        return sp.radsimp(cand2)
    return None


def make_list():
    out = []
    seen = set()

    def add(text, correct_expr, wrong_exprs):
        correct_latex = sp.latex(correct_expr)
        wl = []
        seenw = {correct_latex}
        for w in wrong_exprs:
            try:
                ws = sp.latex(sp.nsimplify(w))
            except Exception:
                continue
            if ws not in seenw:
                wl.append(ws)
                seenw.add(ws)
            if len(wl) == 3:
                break
        if len(wl) != 3:
            return False
        if text in seen:
            return False
        seen.add(text)
        out.append({"text": text, "correct": wrap(correct_latex), "wrong": [wrap(w) for w in wl]})
        return True

    return out, add


# ---------------------------------------------------------------
# 1) sin/cos/tan di arctan/arcsin/arccos di un razionale
# ---------------------------------------------------------------
def gen_composed(add, n=22):
    outer_of_inner = {
        "atan": ["sin", "cos", "tan"],
        "asin": ["cos", "tan"],
        "acos": ["sin", "tan"],
    }
    inner_names = {"atan": "\\arctan", "asin": "\\arcsin", "acos": "\\arccos"}
    outer_names = {"sin": "\\sin", "cos": "\\cos", "tan": "\\tan"}
    rationals = [sp.Rational(a, b) for a in range(-3, 4) for b in (2, 3, 4) if a != 0 and sp.gcd(abs(a), b) == 1 and abs(sp.Rational(a, b)) < 1] \
        + [sp.Rational(a, 1) for a in (-3, -2, -1, 1, 2, 3)]
    count = 0
    tries = 0
    seen_pairs = set()
    while count < n and tries < 300:
        tries += 1
        inner = random.choice(list(outer_of_inner.keys()))
        k = random.choice(rationals)
        if inner in ("asin", "acos") and abs(k) >= 1:
            continue
        outer = random.choice(outer_of_inner[inner])
        key = (inner, outer, k)
        if key in seen_pairs:
            continue
        inner_fn = getattr(sp, inner)
        outer_fn = getattr(sp, outer)
        expr = outer_fn(inner_fn(k))
        val = exact_value(expr)
        if val is None:
            continue
        seen_pairs.add(key)

        k_latex = sp.latex(k)
        text = (r"Semplificare l'espressione \( %s\left(%s\left(%s\right)\right) \)." %
                (outer_names[outer], inner_names[inner], k_latex))

        candidates = []
        # errore: segno opposto
        candidates.append(-val)
        # errore: usa l'altra funzione trig sullo stesso angolo (scambia le formule)
        for oo in outer_of_inner[inner]:
            if oo != outer:
                v = exact_value(getattr(sp, oo)(inner_fn(k)))
                if v is not None:
                    candidates.append(v)
        # errore: dimentica il segno di k (usa |k|)
        v = exact_value(outer_fn(inner_fn(abs(k))))
        if v is not None:
            candidates.append(v)
        # errore: confonde la funzione inversa (arctan/arcsin/arccos scambiate)
        for other_inner in outer_of_inner:
            if other_inner != inner:
                try:
                    v = exact_value(outer_fn(getattr(sp, other_inner)(k)))
                except Exception:
                    v = None
                if v is not None:
                    candidates.append(v)
        # errore di riserva: reciproco del valore corretto
        if val != 0:
            candidates.append(1 / val)

        if add(text, val, candidates):
            count += 1


# ---------------------------------------------------------------
# 2) Riduzione di angoli: arctan(tan(theta)), arccos(cos(theta)), arcsin(sin(theta))
#    per theta fuori dal range principale
# ---------------------------------------------------------------
def gen_reduction(add, n=16):
    thetas = [sp.pi * sp.Rational(a, b) for b in (3, 4, 6) for a in range(1, 4 * b)
              if sp.gcd(a, b) == 1]
    funcs = [("atan", "tan", "\\arctan", "\\tan"), ("acos", "cos", "\\arccos", "\\cos"), ("asin", "sin", "\\arcsin", "\\sin")]
    count = 0
    tries = 0
    seen_pairs = set()
    while count < n and tries < 400:
        tries += 1
        inv, fwd, inv_name, fwd_name = random.choice(funcs)
        theta = random.choice(thetas)
        # scarta gli angoli gia' nel range principale (nessuna vera riduzione)
        if inv == "atan" and -sp.pi / 2 < theta < sp.pi / 2:
            continue
        if inv == "acos" and 0 <= theta <= sp.pi:
            continue
        if inv == "asin" and -sp.pi / 2 <= theta <= sp.pi / 2:
            continue
        if inv == "atan" and theta % sp.pi == sp.pi / 2:
            continue
        key = (inv, theta)
        if key in seen_pairs:
            continue
        seen_pairs.add(key)

        expr = getattr(sp, inv)(getattr(sp, fwd)(theta))
        val = exact_value(expr)
        if val is None:
            continue

        theta_latex = sp.latex(theta)
        text = (r"Semplificare l'espressione \( %s\left(%s\left(%s\right)\right) \)." %
                (inv_name, fwd_name, theta_latex))

        wrongs = [theta, -val, val + sp.pi if inv != "acos" else val - sp.pi]
        if add(text, val, wrongs):
            count += 1


def build():
    items, add = make_list()
    gen_composed(add, n=22)
    gen_reduction(add, n=16)
    return items


if __name__ == "__main__":
    random.seed(4242)
    items = build()
    print("Totale domande trig inverse stile esame:", len(items))
    bad = 0
    for it in items:
        opts = [it["correct"]] + it["wrong"]
        if len(set(opts)) != 4:
            bad += 1
            print("PROBLEMA:", it["text"])
    print("Domande con problemi:", bad)
    for it in items[:10]:
        print("-", it["text"], "=>", it["correct"])
