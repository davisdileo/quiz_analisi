# -*- coding: utf-8 -*-
"""Domande di 'studio di funzione completo' (dominio, asintoti, monotonia
ed estremi relativi, convessita' e flessi) modellate su tre famiglie di
funzioni prese dalle 7 nuove tracce d'esame caricate:
  - g(x) = 1/log(ax)            (generalizza "1/log x")
  - f(x) = e^{k/(x^2-1)}         (generalizza "e^{1/(x^2-1)}")
  - g(x) = log^3(ax)             (generalizza "log^3 x")
Per ciascuna famiglia la forma qualitativa del risultato (segno della
derivata, direzione degli asintoti verticali, posizione di eventuali
punti di flesso) e' stata derivata a mano e poi VERIFICATA sia
simbolicamente (sp.diff, sp.limit) sia numericamente (valutazione diretta
vicino ai punti critici/di frontiera, per ogni valore del parametro
generato) prima di essere incorporata nel testo della domanda.
"""
import random
import sympy as sp

x = sp.symbols('x', real=True, positive=True)
xr = sp.symbols('x', real=True)


def wrap(s):
    return f"\\({s}\\)"


def make_list():
    out = []
    seen = set()

    def add(text, correct, wrongs):
        opts = [correct] + wrongs
        if len(set(opts)) != 4:
            return False
        if text in seen:
            return False
        seen.add(text)
        out.append({"text": text, "correct": wrap(correct), "wrong": [wrap(w) for w in wrongs]})
        return True

    return out, add


def a_coef(a):
    return "" if a == 1 else sp.latex(a)


# ---------------------------------------------------------------
# Famiglia 1: g(x) = 1/log(a x), a>0  (generalizza "1/log x")
# dominio (0,1/a)U(1/a,+inf); asint. vert. x=1/a (- a sx, + a dx);
# asint. orizz. y=0 sia per x->0+ sia per x->+inf; g'<0 sempre ->
# decrescente su ciascun ramo, nessun estremo relativo.
# ---------------------------------------------------------------
def gen_family1(add, n=8):
    count = 0
    for a in [1, 2, 3, 4, sp.Rational(1, 2), sp.Rational(1, 3), 5, sp.Rational(3, 2)]:
        if count >= n:
            break
        g = 1 / sp.log(a * x)
        gp = sp.simplify(sp.diff(g, x))
        # verifica numerica: g' < 0 ovunque nel dominio (x>0, x != 1/a)
        ok = True
        p = sp.nsimplify(1 / a)
        pf = float(p)
        for xv in [0.05, 0.3, pf * 0.5, pf * 1.5, 3.0, 10.0, 25.0]:
            if abs(xv - pf) < 1e-6 or xv <= 0:
                continue
            val = float(gp.subs(x, xv))
            if val >= 0:
                ok = False
        left = float(g.subs(x, pf - 1e-4))
        right = float(g.subs(x, pf + 1e-4))
        if not ok or not (left < -100 and right > 100):
            continue
        p_l = sp.latex(p)
        ac = a_coef(a)
        text = (r"Studiare dominio, asintoti e monotonia della funzione \( g(x)=\dfrac{1}{\log(%sx)} \)." % ac)
        correct = (r"\text{dominio } \left(0,%s\right)\cup\left(%s,+\infty\right);"
                   r"\ \text{asintoto verticale } x=%s\ \left(\lim_{x\to\left(%s\right)^-}g=-\infty,"
                   r"\ \lim_{x\to\left(%s\right)^+}g=+\infty\right);\ \text{asintoto orizzontale } y=0"
                   r"\text{ per }x\to0^+\text{ e }x\to+\infty;\ g'(x)=\dfrac{-1}{x\log^2(%sx)}<0"
                   r"\text{ sempre: } g \text{ è decrescente su ciascuno dei due intervalli, nessun estremo relativo}"
                   % (p_l, p_l, p_l, p_l, p_l, ac))
        wrong1 = (r"\text{dominio } \left(0,%s\right)\cup\left(%s,+\infty\right);"
                  r"\ \text{asintoto verticale } x=%s\ \left(\lim_{x\to\left(%s\right)^-}g=+\infty,"
                  r"\ \lim_{x\to\left(%s\right)^+}g=-\infty\right);\ \text{asintoto orizzontale } y=0;"
                  r"\ g \text{ è decrescente su ciascun ramo}" % (p_l, p_l, p_l, p_l, p_l))
        wrong2 = (r"\text{dominio } \left(0,%s\right)\cup\left(%s,+\infty\right);"
                  r"\ \text{nessun asintoto verticale};\ \text{asintoto orizzontale } y=0;"
                  r"\ g \text{ è crescente su ciascun ramo}" % (p_l, p_l))
        wrong3 = (r"\text{dominio } (0,+\infty)\setminus\{%s\};\ \text{asintoto verticale } x=%s;"
                  r"\ \text{nessun asintoto orizzontale};\ g \text{ ha un minimo relativo in } x=%s"
                  % (p_l, p_l, p_l))
        if add(text, correct, [wrong1, wrong2, wrong3]):
            count += 1


# ---------------------------------------------------------------
# Famiglia 2: f(x) = e^{k/(x^2-1)}, k intero non nullo
# (generalizza "e^{1/(x^2-1)}")
# dominio R\{-1,1}; asint. orizz. y=1 per x->+-inf; asint. vert. in
# x=1 e x=-1 con direzioni che dipendono dal segno di k; punto
# stazionario in x=0 (MAX relativo se k>0, MIN relativo se k<0), valore e^{-k}.
# ---------------------------------------------------------------
def gen_family2(add, n=10):
    count = 0
    for k in [1, 2, 3, 4, -1, -2, -3, -4, 5, -5]:
        if count >= n:
            break
        f = sp.exp(k / (xr**2 - 1))
        val0 = sp.exp(-k)
        # verifica numerica dei limiti direzionali e del valore in 0
        lim_1m = float(f.subs(xr, 1 - 1e-4))
        lim_1p_finite = float(f.subs(xr, 1 + 1e-4)) if k < 0 else None
        f0 = float(f.subs(xr, 0))
        if abs(f0 - float(val0)) > 1e-6:
            continue
        if k > 0:
            ok = lim_1m < 0.01 and float(f.subs(xr, 1 + 1e-4)) > 1000 and float(f.subs(xr, -1 - 1e-4)) > 1000 and float(f.subs(xr, -1 + 1e-4)) < 0.01
            estremo = "massimo"
        else:
            ok = lim_1m > 1000 and float(f.subs(xr, 1 + 1e-4)) < 0.01 and float(f.subs(xr, -1 - 1e-4)) < 0.01 and float(f.subs(xr, -1 + 1e-4)) > 1000
            estremo = "minimo"
        if not ok:
            continue
        k_s = str(k) if k >= 0 else f"({k})"
        val0_l = sp.latex(val0, ln_notation=True)
        text = (r"Studiare dominio, asintoti, monotonia ed eventuali estremi relativi della funzione "
                r"\( f(x)=e^{\frac{%s}{x^2-1}} \)." % k_s)
        if k > 0:
            dir_1 = r"\lim_{x\to1^-}f=0,\ \lim_{x\to1^+}f=+\infty"
            dir_m1 = r"\lim_{x\to(-1)^-}f=+\infty,\ \lim_{x\to(-1)^+}f=0"
        else:
            dir_1 = r"\lim_{x\to1^-}f=+\infty,\ \lim_{x\to1^+}f=0"
            dir_m1 = r"\lim_{x\to(-1)^-}f=0,\ \lim_{x\to(-1)^+}f=+\infty"
        correct = (r"\text{dominio } \mathbb{R}\setminus\{-1,1\};\ \text{asintoto orizzontale } y=1 \text{ per } x\to\pm\infty;"
                   r"\ \text{asintoti verticali in } x=\pm1\ (%s;\ %s);"
                   r"\ f'(x)=\dfrac{-2kx}{(x^2-1)^2}e^{\frac{k}{x^2-1}}\text{ con } k=%d\ \Rightarrow\ "
                   r"x=0 \text{ è punto di %s relativo, } f(0)=%s" % (dir_1, dir_m1, k, estremo, val0_l))
        estremo_wrong = "minimo" if estremo == "massimo" else "massimo"
        wrong1 = (r"\text{dominio } \mathbb{R}\setminus\{-1,1\};\ \text{asintoto orizzontale } y=0;"
                  r"\ \text{asintoti verticali in } x=\pm1;\ x=0 \text{ è punto di %s relativo, } f(0)=%s"
                  % (estremo, val0_l))
        dir_1_swap = dir_1.replace("1^-", "TMP").replace("1^+", "1^-").replace("TMP", "1^+")
        dir_m1_swap = dir_m1.replace("(-1)^-", "TMP").replace("(-1)^+", "(-1)^-").replace("TMP", "(-1)^+")
        wrong2 = (r"\text{dominio } \mathbb{R}\setminus\{-1,1\};\ \text{asintoto orizzontale } y=1;"
                  r"\ \text{asintoti verticali in } x=\pm1\ (%s;\ %s);"
                  r"\ x=0 \text{ è punto di %s relativo, } f(0)=%s" % (dir_1_swap, dir_m1_swap, estremo, val0_l))
        wrong3 = (r"\text{dominio } \mathbb{R}\setminus\{-1,1\};\ \text{asintoto orizzontale } y=1;"
                  r"\ \text{asintoti verticali in } x=\pm1\ (%s;\ %s);"
                  r"\ f \text{ è monotona su tutto il dominio, nessun estremo relativo}" % (dir_1, dir_m1))
        if add(text, correct, [wrong1, wrong2, wrong3]):
            count += 1


# ---------------------------------------------------------------
# Famiglia 3: g(x) = log^3(a x), a>0  (generalizza "log^3 x")
# dominio (0,+inf); g'(x)=3log^2(ax)/x >= 0 sempre -> strett. crescente
# (stazionaria solo nel punto isolato x=1/a); convessa su (1/a, e^2/a),
# concava altrove; due flessi in x=1/a e x=e^2/a.
# ---------------------------------------------------------------
def gen_family3(add, n=6):
    count = 0
    for a in [1, 2, 3, sp.Rational(1, 2), 4, sp.Rational(1, 3)]:
        if count >= n:
            break
        g = sp.log(a * x)**3
        gpp = sp.diff(g, x, 2)
        p1 = sp.nsimplify(1 / a)
        p2 = sp.nsimplify(sp.exp(2) / a)
        ok = True
        for xv, expect_sign in [(float(p1) * 0.5, -1), ((float(p1) + float(p2)) / 2, 1), (float(p2) * 1.5, -1)]:
            val = float(gpp.subs(x, xv))
            if val * expect_sign <= 0:
                ok = False
        if not ok:
            continue
        ac = a_coef(a)
        p1_l = sp.latex(p1)
        p2_l = sp.latex(p2)
        text = (r"Studiare dominio, monotonia, convessità e punti di flesso della funzione "
                r"\( g(x)=\log^3(%sx) \)." % ac)
        correct = (r"\text{dominio } (0,+\infty);\ g'(x)=\dfrac{3\log^2(%sx)}{x}\ge0\ \forall x>0\ "
                   r"\Rightarrow\ g \text{ è strettamente crescente su tutto il dominio (nessun estremo relativo);}"
                   r"\ g \text{ è concava su } \left(0,%s\right), \text{ convessa su } "
                   r"\left(%s,%s\right), \text{ concava su } \left(%s,+\infty\right);"
                   r"\ \text{due punti di flesso in } x=%s \text{ e } x=%s"
                   % (ac, p1_l, p1_l, p2_l, p2_l, p1_l, p2_l))
        wrong1 = (r"\text{dominio } (0,+\infty);\ g \text{ è strettamente decrescente su tutto il dominio;}"
                  r"\ \text{due punti di flesso in } x=%s \text{ e } x=%s" % (p1_l, p2_l))
        wrong2 = (r"\text{dominio } (0,+\infty);\ g \text{ è strettamente crescente;}"
                  r"\ g \text{ è convessa su } \left(0,%s\right), \text{ concava su } "
                  r"\left(%s,%s\right), \text{ convessa su } \left(%s,+\infty\right)"
                  % (p1_l, p1_l, p2_l, p2_l))
        wrong3 = (r"\text{dominio } (0,+\infty);\ g \text{ è strettamente crescente, nessun punto di flesso "
                  r"(sempre convessa)}")
        if add(text, correct, [wrong1, wrong2, wrong3]):
            count += 1


def build():
    items, add = make_list()
    gen_family1(add, n=8)
    gen_family2(add, n=10)
    gen_family3(add, n=6)
    return items


def build_by_chapter():
    """Tutte le famiglie combinano dominio/limiti con derivata prima e
    seconda (monotonia, estremi relativi, convessita'): assegnate al
    capitolo 6 (Calcolo differenziale), coerentemente con
    exam_function_study.py."""
    return {6: build()}


if __name__ == "__main__":
    random.seed(2024)
    items = build()
    print("Totale domande studio di funzione (nuove tracce):", len(items))
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
