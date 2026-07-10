# -*- coding: utf-8 -*-
"""Domande di 'studio di funzione' modellate esattamente sulle quattro
famiglie di funzioni viste nelle tracce d'esame del docente:
  - f(x) = |x^2 - x - 2|                      (immagine, massimo/minimo assoluto)
  - f(x) = (x-1)^(1/3) - (x+1)^(1/3)           (monotonia, estremo assoluto)
  - f(x) = |x| * e^(1/(x-1))                   (dominio, asintoti)
  - f(x) = ln(|ln(x)|) - 2*ln^2(|x|)           (dominio, asintoti, immagine, massimo assoluto)
Per ciascuna famiglia e' stata ricavata (e verificata con sympy) una forma
chiusa valida per QUALSIASI scelta dei parametri interi, cosi' da poter
generare molte varianti mantenendo intatta la tecnica risolutiva richiesta
dal docente.
"""
import random
import sympy as sp

x = sp.symbols('x', real=True)


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


def signed(n, plus_ok=True):
    if n == 0:
        return ""
    if n > 0:
        return f"+{n}" if plus_ok else str(n)
    return str(n)


# ---------------------------------------------------------------
# Famiglia 1: f(x) = |x^2 + bx + c|  con radici intere distinte r1<r2
# ---------------------------------------------------------------
def gen_family1(add, n=16):
    count = 0
    tries = 0
    seen_pairs = set()
    while count < n and tries < 200:
        tries += 1
        r1 = random.randint(-6, 5)
        r2 = random.randint(r1 + 1, r1 + 8)
        if (r1, r2) in seen_pairs:
            continue
        seen_pairs.add((r1, r2))
        b = -(r1 + r2)
        c = r1 * r2
        if b == 0:
            bx_s = ""
        elif b == 1:
            bx_s = "+x"
        elif b == -1:
            bx_s = "-x"
        else:
            bx_s = f"{signed(b)}x"
        fx_s = f"x^2{bx_s}{signed(c)}"
        text = (r"Calcolare l'immagine della funzione \( f(x)=\left|%s\right| \) e i suoi eventuali "
                r"punti di massimo e minimo assoluto." % fx_s)
        correct = (r"\operatorname{Im}(f)=[0,+\infty);\ \text{minimo assoluto } 0 \text{ in } x=%d \text{ e } x=%d;"
                   r"\ \text{nessun massimo assoluto}" % (r1, r2))
        wrong1 = (r"\operatorname{Im}(f)=[0,+\infty);\ \text{massimo assoluto in } x=\frac{%d}{2},"
                  r"\ \text{nessun minimo assoluto}" % (r1 + r2))
        wrong2 = r"\operatorname{Im}(f)=\mathbb{R};\ \text{nessun punto di massimo o minimo assoluto}"
        wrong3 = (r"\operatorname{Im}(f)=\left[%s,+\infty\right);\ \text{minimo assoluto in } x=\frac{%d}{2}" %
                  (sp.latex(sp.nsimplify(-((r2 - r1) ** 2) / 4)), r1 + r2))
        if add(text, correct, [wrong1, wrong2, wrong3]):
            count += 1


# ---------------------------------------------------------------
# Famiglia 2: f(x) = (x-a)^(1/3) - (x-b)^(1/3), a > b interi
# ---------------------------------------------------------------
def gen_family2(add, n=14):
    count = 0
    tries = 0
    seen_pairs = set()
    while count < n and tries < 200:
        tries += 1
        a = random.randint(-4, 5)
        b = random.randint(a - 6, a - 1)
        if (a, b) in seen_pairs:
            continue
        seen_pairs.add((a, b))
        d = a - b
        m = sp.Rational(a + b, 2)
        m_latex = sp.latex(m)
        minval = sp.radsimp(-((4 * d)) ** sp.Rational(1, 3))
        a_s = str(a) if a >= 0 else f"+{-a}"
        a_s = str(a) if a >= 0 else f"({a})"
        b_s = str(-b) if b < 0 else f"({-b})" if b > 0 else "0"
        expr2 = f"\\sqrt[3]{{x-{a}}}" if a >= 0 else f"\\sqrt[3]{{x+{-a}}}"
        expr2b = f"-\\sqrt[3]{{x-{b}}}" if b >= 0 else f"-\\sqrt[3]{{x+{-b}}}"
        text = (r"Determinare la monotonia della funzione \( f(x)=%s%s \) "
                r"e i suoi eventuali punti di estremo assoluto." % (expr2, expr2b))
        correct = (r"f \text{ è decrescente su } \left(-\infty,%s\right) \text{ e crescente su "
                   r"} \left(%s,+\infty\right);\ \text{minimo assoluto in } x=%s,"
                   r"\ \text{nessun massimo assoluto}" % (m_latex, m_latex, m_latex))
        wrong1 = (r"f \text{ è crescente su } \left(-\infty,%s\right) \text{ e decrescente su "
                  r"} \left(%s,+\infty\right);\ \text{massimo assoluto in } x=%s" %
                  (m_latex, m_latex, m_latex))
        wrong2 = r"f \text{ è strettamente crescente su tutto } \mathbb{R},\ \text{nessun estremo assoluto}"
        wrong3 = (r"f \text{ è decrescente su } \left(-\infty,%s\right) \text{ e crescente su "
                  r"} \left(%s,+\infty\right);\ \text{minimo assoluto } %s" %
                  (m_latex, m_latex, sp.latex(sp.nsimplify(minval))))
        if add(text, correct, [wrong1, wrong2, wrong3]):
            count += 1


# ---------------------------------------------------------------
# Famiglia 3: f(x) = |x| * e^(k/(x-1)), k intero non nullo
# ---------------------------------------------------------------
def gen_family3(add, n=12):
    count = 0
    for k in list(range(-6, 0)) + list(range(1, 7)):
        if count >= n:
            break
        k_s = str(k) if k >= 0 else f"({k})"
        text = (r"Determinare il dominio e gli eventuali asintoti della funzione "
                r"\( f(x)=|x|\,e^{\frac{%s}{x-1}} \)." % k_s)
        if k > 0:
            vert = (r"\text{asintoto verticale in } x=1 \text{ (solo da destra: } "
                    r"\lim_{x\to1^+}f(x)=+\infty,\ \lim_{x\to1^-}f(x)=0\text{)}")
        else:
            vert = (r"\text{asintoto verticale in } x=1 \text{ (solo da sinistra: } "
                    r"\lim_{x\to1^-}f(x)=+\infty,\ \lim_{x\to1^+}f(x)=0\text{)}")
        obl_p = f"y=x{signed(k)}"
        obl_m = f"y=-x{signed(-k)}"
        correct = (r"\text{dominio } \mathbb{R}\setminus\{1\};\ %s;\ \text{asintoto obliquo per }x\to+\infty:\ %s;"
                   r"\ \text{per }x\to-\infty:\ %s" % (vert, obl_p, obl_m))
        wrong1 = (r"\text{dominio } \mathbb{R}\setminus\{1\};\ \text{asintoto orizzontale } y=0 \text{ per } "
                  r"x\to\pm\infty;\ \text{nessun asintoto verticale}")
        vert_wrong = vert.replace("destra", "SINISTRA_TMP").replace("sinistra", "destra").replace("SINISTRA_TMP", "sinistra")
        wrong2 = (r"\text{dominio } \mathbb{R}\setminus\{1\};\ %s;\ \text{asintoto obliquo per }x\to+\infty:\ %s;"
                  r"\ \text{per }x\to-\infty:\ %s" % (vert_wrong, obl_p, obl_m))
        wrong3 = (r"\text{dominio } \mathbb{R}\setminus\{0,1\};\ %s;\ \text{nessun asintoto obliquo}" % vert)
        if add(text, correct, [wrong1, wrong2, wrong3]):
            count += 1


# ---------------------------------------------------------------
# Famiglia 4: f(x) = ln(|ln(x)|) - c*ln^2(|x|), c razionale positivo
# ---------------------------------------------------------------
def gen_family4(add, n=12):
    count = 0
    for c in [1, 2, 3, 4, 5, sp.Rational(1, 2), sp.Rational(3, 2), 6, 7, sp.Rational(5, 2)]:
        if count >= n:
            break
        c_s = sp.latex(c) if c != 1 else ""
        maxval = sp.radsimp(-sp.Rational(1, 2) - sp.log(2 * c) / 2)
        maxval_latex = sp.latex(maxval, ln_notation=True)
        xstar = sp.latex(sp.exp(1 / sp.sqrt(2 * c)))
        text = (r"Calcolare dominio, asintoti e immagine della funzione "
                r"\( f(x)=\ln\bigl(|\ln(x)|\bigr) - %s\ln^2(|x|) \)." %
                (f"{c_s}\\," if c_s else ""))
        correct = (r"\text{dominio } (0,1)\cup(1,+\infty);\ \text{asintoti verticali } x=0^+,\ x=1;"
                   r"\ \lim_{x\to+\infty}f(x)=-\infty \text{ (nessun asintoto orizz./obliquo)};"
                   r"\ \operatorname{Im}(f)=\left(-\infty,%s\right],\ \text{massimo assoluto in } "
                   r"x=e^{\pm 1/\sqrt{2\cdot%s}}" % (maxval_latex, sp.latex(c)))
        wrong1 = (r"\text{dominio } (0,+\infty)\setminus\{1\};\ \text{nessun asintoto};"
                  r"\ \operatorname{Im}(f)=\mathbb{R};\ \text{nessun massimo assoluto}")
        wrong2 = (r"\text{dominio } (0,1)\cup(1,+\infty);\ \text{asintoti verticali } x=0^+,\ x=1;"
                  r"\ \operatorname{Im}(f)=\left[%s,+\infty\right);\ \text{minimo assoluto in } "
                  r"x=e^{\pm 1/\sqrt{2\cdot%s}}" % (maxval_latex, sp.latex(c)))
        wrong3 = (r"\text{dominio } (0,1)\cup(1,+\infty);\ \text{nessun asintoto verticale};"
                  r"\ \operatorname{Im}(f)=\left(-\infty,%s\right]" % maxval_latex)
        if add(text, correct, [wrong1, wrong2, wrong3]):
            count += 1


def build():
    items, add = make_list()
    gen_family1(add, n=16)
    gen_family2(add, n=14)
    gen_family3(add, n=12)
    gen_family4(add, n=12)
    return items


def build_by_chapter():
    """Assegna ciascuna famiglia al capitolo piu' pertinente: famiglia 1
    (immagine di |quadratica|, no calcolo differenziale) -> cap. 3 Funzioni
    reali; famiglia 2 (monotonia via derivata) -> cap. 6 Calcolo
    differenziale; famiglia 3 (asintoti, dominio) -> cap. 4 Limiti;
    famiglia 4 (asintoti + massimo assoluto via derivata) -> cap. 6 Calcolo
    differenziale."""
    result = {}
    items1, add1 = make_list()
    gen_family1(add1, n=16)
    result[3] = items1

    items2, add2 = make_list()
    gen_family2(add2, n=14)
    result[6] = items2

    items3, add3 = make_list()
    gen_family3(add3, n=12)
    result[4] = items3

    items4, add4 = make_list()
    gen_family4(add4, n=12)
    result[6] = result[6] + items4

    return result


if __name__ == "__main__":
    random.seed(7)
    items = build()
    print("Totale domande studio di funzione stile esame:", len(items))
    bad = 0
    for it in items:
        opts = [it["correct"]] + it["wrong"]
        if len(set(opts)) != 4:
            bad += 1
            print("PROBLEMA:", it["text"])
    print("Domande con problemi:", bad)
    for it in items[:4]:
        print("-", it["text"])
        print("  =>", it["correct"])
