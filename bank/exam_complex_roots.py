# -*- coding: utf-8 -*-
"""Radici n-esime di un numero complesso, nello stile esatto delle tracce
d'esame del docente: "z^5=9i", "z^5=-2", "radici quinte di -8", "radici
quinte di -7", "z^4=-1+i*sqrt(3)", "z^4=1+i", "radici quarte di -1+i*sqrt(3)".
Poiche' il modulo r=|w| non e' quasi mai una potenza n-esima perfetta, la
risposta resta nella forma trigonometrica generale (esattamente come
richiesto dal Teorema/formula di De Moivre); le opzioni sbagliate
contengono gli errori tipici (dimenticare il "2" nel passo 2*pi/n,
sbagliare l'angolo di partenza, confondere radice n-esima con potenza
n-esima del modulo).
"""
import random
import sympy as sp

k_sym = sp.symbols('k', integer=True)


def wrap(s):
    return f"\\({s}\\)"


def formula(r, theta_latex, n, step_num=2, angle_wrong_num=False, root_wrong=False, div_wrong=False):
    """Costruisce la LaTeX della formula generale delle radici n-esime,
    con la possibilita' di introdurre i quattro errori tipici sopra elencati."""
    root_part = f"\\sqrt[{n}]{{{r}}}" if not root_wrong else f"{r}"
    step = f"{step_num}k\\pi" if step_num != 1 else "k\\pi"
    if angle_wrong_num:
        angle_num = f"-{theta_latex}+{step}" if not theta_latex.startswith("-") else f"{theta_latex[1:]}+{step}"
    else:
        angle_num = f"{theta_latex}+{step}"
    if div_wrong:
        arg = f"\\left({angle_num}\\right)"
    else:
        arg = f"\\dfrac{{{angle_num}}}{{{n}}}"
    return (r"%s\left(\cos%s+i\sin%s\right),\ k=0,1,\dots,%d" %
            (root_part, arg, arg, n - 1))


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


# w = r * (cos(theta) + i sin(theta)); definiti nello stile delle tracce d'esame
W_LIST = [
    # (descrizione testuale di w, r, theta_latex, theta_val_per_verifica)
    ("9i", 9, r"\frac{\pi}{2}", sp.pi / 2),
    ("-2", 2, r"\pi", sp.pi),
    ("-8", 8, r"\pi", sp.pi),
    ("-7", 7, r"\pi", sp.pi),
    ("-9", 9, r"\pi", sp.pi),
    ("-5", 5, r"\pi", sp.pi),
    ("-11", 11, r"\pi", sp.pi),
    ("4i", 4, r"\frac{\pi}{2}", sp.pi / 2),
    ("-6i", 6, r"-\frac{\pi}{2}", -sp.pi / 2),
    ("1+i", sp.sqrt(2), r"\frac{\pi}{4}", sp.pi / 4),
    ("-1+i\\sqrt{3}", 2, r"\frac{2\pi}{3}", 2 * sp.pi / 3),
    ("1-i\\sqrt{3}", 2, r"-\frac{\pi}{3}", -sp.pi / 3),
    ("-\\sqrt{3}-i", 2, r"-\frac{5\pi}{6}", -sp.Rational(5, 6) * sp.pi),
    ("-1-i", sp.sqrt(2), r"-\frac{3\pi}{4}", -sp.Rational(3, 4) * sp.pi),
]


def build():
    items, add = make_list()
    for w_desc, r, theta_latex, theta_val in W_LIST:
        for n in (3, 4, 5):
            # verifica: r*(cos theta + i sin theta) == w numericamente coerente col simbolo
            correct = formula(sp.latex(r) if not isinstance(r, int) else str(r), theta_latex, n)
            wrong1 = formula(sp.latex(r) if not isinstance(r, int) else str(r), theta_latex, n, step_num=1)  # dimentica il "2"
            wrong2 = formula(sp.latex(r) if not isinstance(r, int) else str(r), theta_latex, n, angle_wrong_num=True)  # angolo con segno sbagliato
            wrong3 = formula(sp.latex(r) if not isinstance(r, int) else str(r), theta_latex, n, root_wrong=True)  # radice n-esima dimenticata (usa r invece di r^(1/n))

            style = random.choice(["equazione", "radici"])
            if style == "equazione":
                text = r"Risolvere in \(\mathbb{C}\) l'equazione \( z^{%d} = %s \)." % (n, w_desc)
            else:
                ord_name = {3: "cubiche", 4: "quarte", 5: "quinte"}[n]
                text = r"Calcolare le radici %s di \( %s \)." % (ord_name, w_desc)

            add(text, correct, [wrong1, wrong2, wrong3])

    # ---- domande "quale NON e' una radice" con radici in forma polare esplicita ----
    for w_desc, r, theta_latex, theta_val in W_LIST[:8]:
        for n in (4, 5):
            r_latex = sp.latex(r) if not isinstance(r, int) else str(r)
            roots_latex = []
            for kk in range(n):
                ang = sp.Rational(kk) * 2 / n
                ang_latex = f"\\dfrac{{{theta_latex}}}{{{n}}}+\\dfrac{{{2*kk}\\pi}}{{{n}}}" if kk else f"\\dfrac{{{theta_latex}}}{{{n}}}"
                roots_latex.append(rf"\sqrt[{n}]{{{r_latex}}}\left(\cos\left({ang_latex}\right)+i\sin\left({ang_latex}\right)\right)")
            correct_root = roots_latex[0]
            fake_root = (rf"\sqrt[{n}]{{{r_latex}}}\left(\cos\left(\dfrac{{{theta_latex}}}{{{n}}}+\dfrac{{\pi}}{{{n}}}\right)"
                         rf"+i\sin\left(\dfrac{{{theta_latex}}}{{{n}}}+\dfrac{{\pi}}{{{n}}}\right)\right)")
            text = (r"Le radici %s di \( %s \) sono \( z_k=\sqrt[%d]{%s}\left(\cos\frac{%s+2k\pi}{%d}+i\sin\frac{%s+2k\pi}{%d}\right) \), "
                    r"\(k=0,\dots,%d\). Quale delle seguenti NON è una di queste radici?" %
                    ({4: "quarte", 5: "quinte"}[n], w_desc, n, r_latex, theta_latex, n, theta_latex, n, n - 1))
            options_correct_set = roots_latex  # tutte vere radici (k=0..n-1)
            wrong_answer = fake_root
            true_but_shown_as_correct_option = options_correct_set[1] if len(options_correct_set) > 1 else options_correct_set[0]
            # per l'MCQ: 3 opzioni sono vere radici (prese da roots_latex), 1 è "fake_root" (la risposta corretta da scegliere è fake_root)
            distractor_roots = roots_latex[1:4] if len(roots_latex) >= 4 else roots_latex[1:]
            if len(distractor_roots) < 3:
                continue
            add(text, wrong_answer, distractor_roots[:3])

    return items


if __name__ == "__main__":
    random.seed(99)
    items = build()
    print("Totale domande radici complesse stile esame:", len(items))
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
