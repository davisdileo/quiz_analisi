# -*- coding: utf-8 -*-
"""Disequazioni esponenziali e logaritmiche nello stile esatto delle tracce
d'esame del docente (es. "1/4^(x^2-3) <= 1/2^x", "log_{1/pi}(2x^2-4) >=
log_{1/pi}(9-3x)", "log_{1/4}(x+4) - 2log_{1/4}(x+1) <= 1/2",
"log_x(x^2+6x+9) <= 0"). Ogni risposta corretta viene calcolata con sympy
(solve_univariate_inequality + intersezione dei domini); i distrattori sono
ottenuti applicando errori tipici (dimenticare il dominio, non invertire il
verso con base <1, ecc.), quindi restano sempre matematicamente distinti
dalla risposta corretta.
"""
import random
import sympy as sp

x = sp.symbols('x', real=True)


def set_to_latex(s):
    if s == sp.EmptySet:
        return r"\emptyset"
    if s == sp.Reals or s == sp.S.Reals:
        return r"\mathbb{R}"
    return sp.latex(sp.simplify(s))


def wrap(s):
    return f"\\({s}\\)"


def make_list():
    out = []
    seen = set()

    def add(text, correct_set, wrong_sets):
        correct = wrap(set_to_latex(correct_set))
        wrongs = []
        seenw = {correct}
        for w in wrong_sets:
            ws = wrap(set_to_latex(w))
            if ws not in seenw:
                wrongs.append(ws)
                seenw.add(ws)
            if len(wrongs) == 3:
                break
        if len(wrongs) != 3:
            return False
        if text in seen:
            return False
        seen.add(text)
        out.append({"text": text, "correct": correct, "wrong": wrongs})
        return True

    return out, add


# ---------------------------------------------------------------
# 1) Disequazioni esponenziali a^(P(x)) R b^(Q(x)) ridotte a base comune
# ---------------------------------------------------------------
def gen_exp_ineq(add, n=14):
    count = 0
    tries = 0
    while count < n and tries < 400:
        tries += 1
        base = random.choice([2, 3])
        # scrive i due membri come potenze di 'base' con esponente frazionario
        p1 = random.choice([1, 2])   # (base)^(-p1) è la "frazione" a sinistra, es 1/base^(...)
        p2 = random.choice([1, 2])
        # esponente sinistro: lineare o quadratico
        left_quad = random.choice([True, False])
        if left_quad:
            a1 = random.choice([1, 2])
            b1 = random.randint(-3, 3)
            exp_left = a1 * x**2 + b1
            exp_left_s = f"x^2{'+' if b1>=0 else ''}{b1}" if b1 != 0 else "x^2"
            if a1 != 1:
                exp_left_s = f"{a1}x^2{'+' if b1>=0 else ''}{b1}" if b1 != 0 else f"{a1}x^2"
        else:
            a1 = random.choice([1, -1, 2])
            b1 = random.randint(-4, 4)
            exp_left = a1 * x + b1
            lin = ("x" if a1 == 1 else ("-x" if a1 == -1 else f"{a1}x"))
            exp_left_s = lin + (f"+{b1}" if b1 > 0 else (str(b1) if b1 < 0 else ""))
        a2 = random.choice([1, -1, 2])
        b2 = random.randint(-4, 4)
        exp_right = a2 * x + b2
        lin2 = ("x" if a2 == 1 else ("-x" if a2 == -1 else f"{a2}x"))
        exp_right_s = lin2 + (f"+{b2}" if b2 > 0 else (str(b2) if b2 < 0 else ""))

        left_pow_base = sp.Rational(1, base)  # membro sinistro sempre (1/base)^exp_left
        right_pow_base = sp.Rational(1, base**p2) if random.random() < 0.5 else sp.Integer(base)

        direction = random.choice(["<=", ">="])

        # esponente equivalente in base 2 (o 'base'): trasformiamo entrambi i membri
        # in potenze di 'base' con esponente e sinistro/destro
        left_exponent = -exp_left  # perché (1/base)^e = base^{-e}
        if right_pow_base == sp.Integer(base):
            right_exponent = exp_right
            right_latex = f"{base}^{{{exp_right_s}}}"
        else:
            right_exponent = -p2 * exp_right
            right_latex = f"\\left(\\frac{{1}}{{{base**p2}}}\\right)^{{{exp_right_s}}}"

        left_latex = f"\\left(\\frac{{1}}{{{base}}}\\right)^{{{exp_left_s}}}"

        # la disequazione tra esponenti, sapendo che 'base' > 1: stesso verso
        core_expr = left_exponent - right_exponent  # <=0 o >=0 a seconda di direction
        if direction == "<=":
            ineq = sp.Le(left_exponent, right_exponent)
            wrong_ineq = sp.Ge(left_exponent, right_exponent)  # verso scambiato per errore
        else:
            ineq = sp.Ge(left_exponent, right_exponent)
            wrong_ineq = sp.Le(left_exponent, right_exponent)

        try:
            sol = sp.solve_univariate_inequality(ineq, x, relational=False)
            wrong_sol = sp.solve_univariate_inequality(wrong_ineq, x, relational=False)
        except Exception:
            continue

        if sol in (sp.EmptySet, sp.Reals) or sol.is_finite_set:
            continue

        text = (r"Risolvere la disequazione \( %s %s %s \)." %
                (left_latex, direction.replace("<=", "\\le").replace(">=", "\\ge"), right_latex))

        wrong2 = sp.Complement(sp.Reals, sol)
        wrong3 = sp.solve_univariate_inequality(sp.Le(left_exponent, -right_exponent), x, relational=False)
        if add(text, sol, [wrong_sol, wrong2, wrong3]):
            count += 1


# ---------------------------------------------------------------
# 2) Disequazioni logaritmiche log_a(F(x)) R log_a(G(x)) (stessa base)
# ---------------------------------------------------------------
def gen_log_same_base(add, n=14):
    count = 0
    tries = 0
    bases_lt1 = [(r"\frac{1}{\pi}", False), (r"\frac{1}{2}", False), (r"\frac{1}{4}", False), (r"\frac{1}{3}", False)]
    bases_gt1 = [("2", True), ("3", True), ("5", True), (r"\pi", True)]
    while count < n and tries < 400:
        tries += 1
        base_latex, gt1 = random.choice(bases_lt1 + bases_gt1)

        kind = random.choice(["quad_lin", "lin_lin", "quad_const"])
        if kind == "quad_lin":
            a = random.choice([1, 2])
            c = random.randint(2, 8)
            F = a * x**2 - c
            F_s = f"{a}x^2-{c}" if a != 1 else f"x^2-{c}"
            d = random.randint(3, 12)
            e = random.choice([1, 2, 3])
            G = d - e * x
            G_s = f"{d}-{e}x" if e != 1 else f"{d}-x"
        elif kind == "lin_lin":
            a = random.choice([1, 2, 3])
            b = random.randint(1, 6)
            F = a * x + b
            F_s = (f"{a}x+{b}" if a != 1 else f"x+{b}")
            d = random.randint(1, 5)
            e = random.choice([1, 2])
            G = d * x + random.randint(1, 6)
            const2 = G - d * x
            G_s = (f"{d}x+{const2}" if d != 1 else f"x+{const2}")
        else:  # quad_const: log_a(F) R c  (confrontato con base^c)
            a = random.choice([1, 2])
            b = random.randint(-4, 4)
            c0 = random.randint(2, 10)
            F = a * x**2 + b * x + c0
            F_s = f"{a}x^2" + (f"+{b}x" if b > 0 else (f"{b}x" if b < 0 else "")) + f"+{c0}"
            expo = random.choice([sp.Rational(1, 2), sp.Integer(1), sp.Integer(2)])
            G = sp.nsimplify(base_latex_to_val(base_latex)) ** expo
            G_s = None  # useremo direttamente il numero come confronto

        direction = random.choice(["<=", ">="])
        try:
            if kind == "quad_const":
                base_val = base_latex_to_val(base_latex)
                bound = base_val ** expo
                dom = sp.solve_univariate_inequality(sp.Gt(F, 0), x, relational=False)
                if gt1:
                    core = sp.Le(F, bound) if direction == "<=" else sp.Ge(F, bound)
                else:
                    core = sp.Ge(F, bound) if direction == "<=" else sp.Le(F, bound)
                core_sol = sp.solve_univariate_inequality(core, x, relational=False)
                sol = dom.intersect(core_sol)
                text = (r"Risolvere la disequazione \( \log_{%s}\left(%s\right) %s %s \)." %
                        (base_latex, F_s, direction.replace("<=", "\\le").replace(">=", "\\ge"),
                         sp.latex(expo)))
                wrong_a = dom.intersect(sp.solve_univariate_inequality(sp.Ge(F, bound) if direction == "<=" else sp.Le(F, bound), x, relational=False))
                wrong_b = core_sol  # senza dominio
                wrong_c = sp.Complement(sp.Reals, sol)
            else:
                domF = sp.solve_univariate_inequality(sp.Gt(F, 0), x, relational=False)
                domG = sp.solve_univariate_inequality(sp.Gt(G, 0), x, relational=False)
                if gt1:
                    core = sp.Ge(F, G) if direction == ">=" else sp.Le(F, G)
                else:
                    core = sp.Le(F, G) if direction == ">=" else sp.Ge(F, G)
                core_sol = sp.solve_univariate_inequality(core, x, relational=False)
                sol = domF.intersect(domG).intersect(core_sol)
                text = (r"Risolvere la disequazione \( \log_{%s}\left(%s\right) %s \log_{%s}\left(%s\right) \)." %
                        (base_latex, F_s, direction.replace("<=", "\\le").replace(">=", "\\ge"), base_latex, G_s))
                wrong_core = sp.Ge(F, G) if core == sp.Le(F, G) else sp.Le(F, G)
                wrong_sol = sp.solve_univariate_inequality(wrong_core, x, relational=False)
                wrong_a = wrong_sol
                wrong_b = core_sol  # senza intersecare il dominio
                wrong_c = domF.intersect(domG)
        except Exception:
            continue

        if sol in (sp.EmptySet,) or (hasattr(sol, "is_finite_set") and sol.is_finite_set):
            continue

        if add(text, sol, [wrong_a, wrong_b, wrong_c]):
            count += 1


def base_latex_to_val(s):
    return {
        r"\frac{1}{\pi}": 1 / sp.pi, r"\frac{1}{2}": sp.Rational(1, 2),
        r"\frac{1}{4}": sp.Rational(1, 4), r"\frac{1}{3}": sp.Rational(1, 3),
        "2": sp.Integer(2), "3": sp.Integer(3), "5": sp.Integer(5), r"\pi": sp.pi,
    }[s]


# ---------------------------------------------------------------
# 3) log_x((x+k)^2) R 0  con base variabile (caso "firma" delle tracce)
# ---------------------------------------------------------------
def gen_log_varbase(add):
    for k in range(1, 7):
        for direction, sol_desc in [("<=", "(0,1)"), (">=", "(1,+\\infty)")]:
            F_s = f"(x+{k})^2" if k != 0 else "x^2"
            text = (r"Risolvere la disequazione \( \log_x\left((x+%d)^2\right) %s 0 \) (con \(x>0,\ x\neq 1\))." %
                    (k, "\\le" if direction == "<=" else "\\ge"))
            if direction == "<=":
                sol = sp.Interval.open(0, 1)
                wrong = [sp.Interval.open(1, sp.oo), sp.Interval.open(0, sp.oo), sp.Interval.Ropen(0, 1)]
            else:
                sol = sp.Interval.open(1, sp.oo)
                wrong = [sp.Interval.open(0, 1), sp.Interval.open(0, sp.oo), sp.Interval.Lopen(1, sp.oo)]
            add(text, sol, wrong)


def build():
    items, add = make_list()
    gen_exp_ineq(add, n=14)
    gen_log_same_base(add, n=16)
    gen_log_varbase(add)
    return items


if __name__ == "__main__":
    random.seed(2026)
    items = build()
    print("Totale domande algebra stile esame:", len(items))
    bad = 0
    for it in items:
        opts = [it["correct"]] + it["wrong"]
        if len(set(opts)) != 4:
            bad += 1
            print("PROBLEMA:", it["text"])
    print("Domande con problemi:", bad)
    for it in items[:6]:
        print("-", it["text"], "=>", it["correct"])
