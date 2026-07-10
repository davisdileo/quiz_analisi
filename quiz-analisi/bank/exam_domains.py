# -*- coding: utf-8 -*-
"""Domande sull'insieme di definizione (dominio) di funzioni composte con
log/arcsin/radici, accoppiate a domande sulle proprietà topologiche
dell'insieme trovato (intervallo? limitato? aperto/chiuso? compatto?
punti di frontiera Fr? punti di accumulazione Dr? sup/inf/max/min?) —
esattamente come il punto 1.(a) di ciascuna delle 7 tracce d'esame
caricate (es. dominio di \\(1/\\log x\\), \\(\\log_{1/2}(\\arcsin x)\\),
\\(1/((x+1)^2(\\log|x|+1)^3)\\), \\(\\log(e^{2x}-e^x+1)\\),
\\(1/\\sqrt{1-\\log^2 x}\\)).

Ogni famiglia genera SIA la domanda "trova il dominio" SIA la domanda
"quale proprieta' topologica ha l'insieme trovato" — la seconda sfrutta
il fatto che la forma topologica (intervallo aperto/chiuso/semiaperto,
limitato/illimitato, R privato di punti isolati, tutto R) e' fissata
per costruzione della famiglia, quindi le affermazioni vere/false sono
valide per OGNI istanza della famiglia (solo i numeri cambiano).

Ogni dominio derivato simbolicamente viene ri-verificato numericamente
campionando punti interni/esterni/di frontiera con le vere funzioni
Python (math.log, math.asin, math.sqrt) per scartare errori di segno.
"""
import math
import random
import sympy as sp


def wrap(s):
    return f"\\({s}\\)"


def make_list():
    out = []
    seen = set()

    def add(text, correct, wrong_candidates, chapter, prose=False):
        """Se prose=False (domande 'trova il dominio'), correct/wrong sono
        espressioni matematiche pure e vengono avvolte in \\( \\). Se
        prose=True (domande sulle proprieta' topologiche), correct/wrong
        sono gia' frasi complete con \\( \\) incorporati e NON vanno
        avvolte di nuovo."""
        fmt = (lambda s: s) if prose else wrap
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
        out.append({"text": text, "correct": fmt(correct), "wrong": [fmt(w) for w in wrongs], "chapter": chapter})
        return True

    return out, add


def frac_latex(val):
    val = sp.nsimplify(val)
    return sp.latex(val)


# ---------------------------------------------------------------
# Famiglia A: g(x) = log_{1/2}(arcsin(a x + b))  con a>0
# dominio: 0 < a x + b <= 1  =>  x in (-b/a, (1-b)/a]   (semiaperto, limitato)
# ---------------------------------------------------------------
def gen_family_A(add, n=8):
    count = 0
    tries = 0
    used = set()
    while count < n and tries < 300:
        tries += 1
        a = random.choice([1, 2, 3])
        b = random.randint(-4, 4)
        if (a, b) in used:
            continue
        p = sp.nsimplify(sp.Rational(-b, a))
        q = sp.nsimplify(sp.Rational(1 - b, a))

        # verifica numerica indipendente con math.asin/math.log
        def defined(t, a=a, b=b):
            u = a * t + b
            if not (-1 <= u <= 1):
                return False
            v = math.asin(u)
            if v <= 0:
                return False
            return True

        pf, qf = float(p), float(q)
        eps = (qf - pf) * 0.001 if qf > pf else 1e-6
        ok = (not defined(pf)) and defined(pf + eps) and defined(qf) and (not defined(qf + eps))
        if not ok:
            continue
        used.add((a, b))
        sign_b = "+" if b >= 0 else "-"
        a_s = "" if a == 1 else str(a)
        text = r"Determinare l'insieme di definizione \(D\) di \( g(x)=\log_{1/2}\left(\arcsin(%sx%s%d)\right) \)." % (a_s, sign_b, abs(b))
        correct = r"\left(%s,\ %s\right]" % (frac_latex(p), frac_latex(q))
        candidates = [
            r"\left[%s,\ %s\right)" % (frac_latex(p), frac_latex(q)),
            r"\left(%s,\ %s\right)" % (frac_latex(p), frac_latex(q)),
            r"\left[%s,\ %s\right]" % (frac_latex(p), frac_latex(q)),
            r"\left(%s,\ %s\right]" % (frac_latex(-p if p != 0 else 1), frac_latex(q)),
            r"\left(-\infty,\ %s\right]" % frac_latex(q),
        ]
        if add(text, correct, candidates, chapter=3):
            count += 1
            # domanda gemella sulla proprieta' topologica di D (sempre vera per questa forma)
            prop_text = (r"Sia \(D=\left(%s,\ %s\right]\) l'insieme di definizione trovato al punto precedente "
                         r"(con \(%s<%s\)). Quale affermazione e' corretta?") % (frac_latex(p), frac_latex(q), frac_latex(p), frac_latex(q))
            prop_correct = (r"\(D\) è limitato e ammette massimo (\(\max D=%s\)), ma non ammette minimo "
                             r"(\(\inf D=%s\) non è un punto di \(D\)); \(D\) non è né aperto né chiuso, quindi non è compatto") % (frac_latex(q), frac_latex(p))
            prop_wrong = [
                r"\(D\) è chiuso e limitato, quindi compatto per il teorema di Heine-Borel",
                r"\(D\) è aperto, quindi non ammette né massimo né minimo",
                r"\(D\) è illimitato superiormente, quindi non ammette massimo",
                r"\(D\) è chiuso ma non limitato",
            ]
            add(prop_text, prop_correct, prop_wrong, chapter=1, prose=True)
    return count


# ---------------------------------------------------------------
# Famiglia B: g(x) = 1/((x-c)^2 (log|x|+1)^k)
# dominio: R \ {0, c, -1/e, 1/e}  (aperto, illimitato, NON e' un intervallo)
# ---------------------------------------------------------------
def gen_family_B(add, n=6):
    count = 0
    tries = 0
    used = set()
    while count < n and tries < 300:
        tries += 1
        c = random.choice([-3, -2, 2, 3, 4, -4])
        if abs(c) < 0.5 or abs(abs(c) - 1 / math.e) < 0.05:
            continue
        if c in used:
            continue

        def defined(t, c=c):
            if t == 0 or abs(t - c) < 1e-9:
                return False
            base = math.log(abs(t)) + 1
            if abs(base) < 1e-9:
                return False
            return True

        inv_e = 1 / math.e
        test_pts = [c - 0.1, c + 0.1, -inv_e - 0.05, -inv_e + 0.05, inv_e - 0.05, inv_e + 0.05, 0.001, -0.001, 1.0, -1.0]
        boundary_pts = [0.0, float(c), -inv_e, inv_e]
        if any(defined(bp) for bp in boundary_pts):
            continue
        if not all(defined(t) for t in test_pts if abs(t) > 1e-9 and abs(t - c) > 1e-9):
            continue
        used.add(c)
        c_l = sp.latex(sp.Integer(c))
        text = (r"Determinare l'insieme di definizione \(D\) di \( g(x)=\dfrac{1}{(x-%s)^2\left(\log|x|+1\right)^3} \).") % c_l
        correct = r"\mathbb{R}\setminus\left\{-\frac{1}{e},\ 0,\ \frac{1}{e},\ %s\right\}" % c_l
        candidates = [
            r"\mathbb{R}\setminus\left\{0,\ %s\right\}" % c_l,
            r"\mathbb{R}\setminus\left\{-e,\ 0,\ e,\ %s\right\}" % c_l,
            r"\left(0,+\infty\right)\setminus\left\{\frac{1}{e},\ %s\right\}" % c_l,
            r"\mathbb{R}\setminus\left\{-\frac{1}{e},\ \frac{1}{e},\ %s\right\}" % c_l,
        ]
        if add(text, correct, candidates, chapter=3):
            count += 1
            prop_text = (r"L'insieme \(D=\mathbb{R}\setminus\{p_1,p_2,p_3,p_4\}\) (complementare di un insieme finito di punti) "
                         r"trovato al punto precedente: quale affermazione e' corretta?")
            prop_correct = (r"\(D\) è aperto (unione di intervalli aperti) ma non è un intervallo; è illimitato, non è chiuso "
                             r"e quindi non è compatto; l'insieme dei punti di accumulazione è \(D_r D=\mathbb{R}\) (include anche i 4 punti esclusi)")
            prop_wrong = [
                r"\(D\) è chiuso poiché il complementare di un insieme finito è sempre chiuso",
                r"\(D\) è compatto poiché è unione finita di intervalli",
                r"\(D\) è un intervallo illimitato",
                r"L'insieme dei punti di accumulazione è \(D_r D=D\), cioè i 4 punti esclusi non sono di accumulazione per \(D\)",
            ]
            add(prop_text, prop_correct, prop_wrong, chapter=1, prose=True)
    return count


# ---------------------------------------------------------------
# Famiglia C: g(x) = log(e^{2x} - e^x + m),  m > 1/4  =>  dominio = R
# (il trinomio t^2-t+m in t=e^x ha discriminante 1-4m<0, quindi e' sempre positivo)
# ---------------------------------------------------------------
def gen_family_C(add, n=5):
    count = 0
    for m in [1, 2, 3, 5, 8]:
        if count >= n:
            break
        disc = 1 - 4 * m
        if disc >= 0:
            continue
        # verifica numerica: e^{2x}-e^x+m > 0 per ogni x campionato
        ok = True
        for xv in [-5, -1, -0.1, 0, 0.1, 1, 5]:
            val = math.exp(2 * xv) - math.exp(xv) + m
            if val <= 0:
                ok = False
                break
        if not ok:
            continue
        text = r"Determinare l'insieme di definizione \(D\) di \( g(x)=\log\left(e^{2x}-e^{x}+%d\right) \)." % m
        correct = r"\mathbb{R}"
        candidates = [
            r"\left(0,+\infty\right)",
            r"\mathbb{R}\setminus\{0\}",
            r"\left(-\infty,0\right)",
            r"\emptyset",
        ]
        if add(text, correct, candidates, chapter=3):
            count += 1
            prop_text = (r"Il dominio \(D\) trovato al punto precedente coincide con \(\mathbb{R}\) poiché "
                         r"\(t^2-t+%d>0\ \forall t\in\mathbb{R}\) (discriminante negativo, con \(t=e^x\)). "
                         r"Quale affermazione su \(D=\mathbb{R}\) è corretta?") % m
            prop_correct = r"\(D=\mathbb{R}\) è sia aperto che chiuso (insieme chiuso-aperto), illimitato, quindi non compatto, e ha frontiera \(\operatorname{Fr}D=\emptyset\)"
            prop_wrong = [
                r"\(D=\mathbb{R}\) è compatto poiché è chiuso",
                r"\(D=\mathbb{R}\) è limitato",
                r"\(D=\mathbb{R}\) è aperto ma non chiuso",
                r"\(\operatorname{Fr}D=\mathbb{R}\)",
            ]
            add(prop_text, prop_correct, prop_wrong, chapter=1, prose=True)
    return count


# ---------------------------------------------------------------
# Famiglia D: g(x) = 1/sqrt(k - log^2(x)),  k=n^2 perfetto  =>  dominio (e^-n, e^n), aperto limitato
# ---------------------------------------------------------------
def gen_family_D(add, n=6):
    count = 0
    for nn in [1, 2, 3]:
        if count >= n:
            break
        k = nn * nn
        p_exact = sp.exp(-nn)
        q_exact = sp.exp(nn)

        def defined(t, k=k):
            if t <= 0:
                return False
            v = k - math.log(t) ** 2
            return v > 0

        pf, qf = float(p_exact), float(q_exact)
        eps = (qf - pf) * 0.001
        ok = (not defined(pf)) and defined(pf + eps) and defined(qf - eps) and (not defined(qf))
        if not ok:
            continue
        text = r"Determinare l'insieme di definizione \(D\) di \( g(x)=\dfrac{1}{\sqrt{%d-\log^2 x}} \)." % k
        p_l, q_l = sp.latex(sp.exp(-nn)), sp.latex(sp.exp(nn))
        correct = r"\left(%s,\ %s\right)" % (p_l, q_l)
        candidates = [
            r"\left[%s,\ %s\right]" % (p_l, q_l),
            r"\left(0,\ %s\right)" % q_l,
            r"\left(%s,\ %s\right]" % (p_l, q_l),
            r"\left(-%s,\ %s\right)" % (q_l, q_l),
        ]
        if add(text, correct, candidates, chapter=3):
            count += 1
            prop_text = (r"L'intervallo \(D=\left(e^{-%d},\ e^{%d}\right)\) trovato al punto precedente: quale affermazione è corretta?") % (nn, nn)
            prop_correct = r"\(D\) è un intervallo aperto e limitato, ma non è chiuso: non è compatto, non ammette né massimo né minimo, e \(\operatorname{Fr}D=\{e^{-%d},e^{%d}\}\)" % (nn, nn)
            prop_wrong = [
                r"\(D\) è compatto poiché è limitato",
                r"\(D\) ammette massimo \(e^{%d}\) e minimo \(e^{-%d}\)" % (nn, nn),
                r"\(D\) è chiuso e limitato, quindi compatto",
                r"\(\operatorname{Fr}D=\emptyset\) poiché \(D\) è aperto",
            ]
            add(prop_text, prop_correct, prop_wrong, chapter=1, prose=True)
    return count


# ---------------------------------------------------------------
# Famiglia E: g(x) = sqrt(k - log^2(x)),  k=n^2  =>  dominio [e^-n, e^n], CHIUSO e limitato -> compatto
# (variante "gemella" della famiglia D, senza il denominatore: mostra la
# differenza cruciale fra <= e < ai fini di compattezza)
# ---------------------------------------------------------------
def gen_family_E(add, n=6):
    count = 0
    for nn in [1, 2, 3]:
        if count >= n:
            break
        k = nn * nn

        def defined(t, k=k):
            if t <= 0:
                return False
            v = k - math.log(t) ** 2
            return v >= 0

        pf, qf = math.exp(-nn), math.exp(nn)
        ok = defined(pf) and defined((pf + qf) / 2) and defined(qf) and (not defined(pf * 0.999)) and (not defined(qf * 1.001))
        if not ok:
            continue
        text = r"Determinare l'insieme di definizione \(D\) di \( g(x)=\sqrt{%d-\log^2 x} \)." % k
        p_l, q_l = sp.latex(sp.exp(-nn)), sp.latex(sp.exp(nn))
        correct = r"\left[%s,\ %s\right]" % (p_l, q_l)
        candidates = [
            r"\left(%s,\ %s\right)" % (p_l, q_l),
            r"\left[0,\ %s\right]" % q_l,
            r"\left[%s,\ %s\right)" % (p_l, q_l),
            r"\left(%s,\ %s\right]" % (p_l, q_l),
        ]
        if add(text, correct, candidates, chapter=3):
            count += 1
            prop_text = (r"L'intervallo \(D=\left[e^{-%d},\ e^{%d}\right]\) trovato al punto precedente: quale affermazione è corretta?") % (nn, nn)
            prop_correct = r"\(D\) è chiuso e limitato, quindi compatto per il teorema di Heine-Borel; ammette massimo \(e^{%d}\) e minimo \(e^{-%d}\), e \(\operatorname{Fr}D=\{e^{-%d},e^{%d}\}\subset D\)" % (nn, nn, nn, nn)
            prop_wrong = [
                r"\(D\) è aperto, quindi non compatto",
                r"\(D\) è limitato ma non chiuso, quindi non compatto",
                r"\(D\) non ammette né massimo né minimo poiché è un intervallo",
                r"\(\operatorname{Fr}D=\emptyset\)",
            ]
            add(prop_text, prop_correct, prop_wrong, chapter=1, prose=True)
    return count


def build_by_chapter():
    items, add = make_list()
    gen_family_A(add, n=8)
    gen_family_B(add, n=6)
    gen_family_C(add, n=5)
    gen_family_D(add, n=6)
    gen_family_E(add, n=6)
    by_ch = {}
    for it in items:
        ch = it["chapter"]
        by_ch.setdefault(ch, []).append({"text": it["text"], "correct": it["correct"], "wrong": it["wrong"]})
    return by_ch


def build():
    by_ch = build_by_chapter()
    flat = []
    for ch, lst in by_ch.items():
        flat.extend(lst)
    return flat


if __name__ == "__main__":
    random.seed(777)
    by_ch = build_by_chapter()
    total = sum(len(v) for v in by_ch.values())
    print("Totale domande domini/topologia:", total)
    print("Per capitolo:", {k: len(v) for k, v in by_ch.items()})
    bad = 0
    for ch, lst in by_ch.items():
        for it in lst:
            opts = [it["correct"]] + it["wrong"]
            if len(set(opts)) != 4:
                bad += 1
                print("PROBLEMA:", it["text"])
    print("Domande con problemi:", bad)
    for ch, lst in by_ch.items():
        print(f"--- capitolo {ch} ---")
        for it in lst[:2]:
            print(" -", it["text"])
            print("   =>", it["correct"])
