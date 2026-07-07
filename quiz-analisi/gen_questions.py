# -*- coding: utf-8 -*-
# Genera data/questions.json: 50 domande stile esame universitario di Ingegneria,
# con formule in LaTeX (rese poi con KaTeX lato client). Tutti i risultati
# numerici sono stati verificati con sympy prima di essere inseriti qui.
import json, random, os

random.seed(7)

Q = []

def add(topic, text, correct, wrong, image=None):
    opts = [correct] + wrong
    order = list(range(len(opts)))
    random.shuffle(order)
    shuffled = [opts[i] for i in order]
    correct_index = shuffled.index(correct)
    q = {
        "id": len(Q) + 1,
        "topic": topic,
        "text": text,
        "options": shuffled,
        "correct": correct_index,
    }
    if image:
        q["image"] = image
    Q.append(q)

# ================= Numeri reali (4) =================
add("Numeri reali",
    r"Sia \( A = \left\{ \dfrac{n}{n+1} : n \in \mathbb{N},\ n \ge 1 \right\} \). Quanto vale \( \sup A \)?",
    r"\(1\)", [r"\(1/2\)", r"\(0\)", r"non esiste"])

add("Numeri reali",
    r"La disuguaglianza di Bernoulli \( (1+x)^n \ge 1+nx \), per \( x > -1 \) e \( n \in \mathbb{N} \):",
    "vale per ogni \\(n \\ge 0\\)", ["vale solo se \\(n\\) è pari", "vale solo se \\(x>0\\)", "non vale in generale"])

add("Numeri reali",
    r"Risolvere in \( \mathbb{R} \) la disequazione \( \left| \dfrac{2x-1}{x+2} \right| \le 1 \):",
    r"\( -\dfrac{1}{3} \le x \le 3 \)", [r"\( -2 < x \le 3 \)", r"\( x \le -\dfrac13 \) oppure \( x \ge 3 \)", r"\( 1 \le x \le 3 \)"])

add("Numeri reali",
    r"Sia \( B = \{ x \in \mathbb{R} : x^2 - 5x + 6 < 0 \} \). Quanto vale \( \inf B \)?",
    r"\(2\)", [r"\(3\)", r"\(0\)", "non esiste"])

# ================= Numeri complessi (4) =================
add("Numeri complessi",
    r"Calcolare \( (1+i)^{8} \).",
    r"\(16\)", [r"\(-16\)", r"\(16i\)", r"\(-16i\)"])

add("Numeri complessi",
    r"Quale dei seguenti numeri NON è una radice cubica di \( -8 \)?",
    r"\(2\)", [r"\(-2\)", r"\(1+i\sqrt3\)", r"\(1-i\sqrt3\)"])

add("Numeri complessi",
    r"Una soluzione dell'equazione \( z^2 = 3-4i \) nel campo complesso è:",
    r"\(2-i\)", [r"\(2+i\)", r"\(-2-i\)", r"\(1-2i\)"])

add("Numeri complessi",
    r"Il luogo dei punti \( z=x+iy \) del piano complesso tali che \( |z-1| = |z+i| \) è:",
    "la retta di equazione \\(y=-x\\)", ["una circonferenza di raggio \\(1\\)", "un'ellisse", "un singolo punto"])

# ================= Funzioni reali (4) =================
add("Funzioni reali",
    r"Determinare il dominio di \( f(x) = \ln\!\left( \dfrac{x-1}{x+3} \right) + \sqrt{4-x^2} \).",
    r"\( (1,2] \)", [r"\( [1,2] \)", r"\( (-3,1) \)", r"\( (-2,2) \)"])

add("Funzioni reali",
    r"Sia \( f(x) = \dfrac{x}{1+|x|} \), \( x \in \mathbb{R} \). Quale affermazione è corretta?",
    r"\(f\) è iniettiva su \( \mathbb{R} \) e la sua immagine è \( (-1,1) \)",
    ["\\(f\\) è suriettiva su \\( \\mathbb{R} \\)", "\\(f\\) non è iniettiva, poiché \\(f(-1)=f(1)\\)", "\\(f\\) è periodica di periodo \\(2\\)"])

add("Funzioni reali",
    r"Determinare la funzione inversa di \( f(x) = 1 + \ln(x-2) \), per \( x>2 \).",
    r"\( f^{-1}(x) = 2 + e^{x-1} \)", [r"\( f^{-1}(x) = e^{x-1} - 2 \)", r"\( f^{-1}(x) = 2 + e^{x+1} \)", r"\( f^{-1}(x) = \ln(x-2) - 1 \)"])

add("Funzioni reali",
    r"Sia \( f(x) = x^5 + x^3 + x \), \( x \in \mathbb{R} \). Cosa si può concludere sull'invertibilità di \(f\)?",
    "\\(f'(x) = 5x^4+3x^2+1 > 0\\) per ogni \\(x\\), quindi \\(f\\) è strettamente crescente e invertibile su \\(\\mathbb{R}\\)",
    ["\\(f\\) non è iniettiva su \\(\\mathbb{R}\\)", "\\(f\\) è invertibile solo per \\(x \\ge 0\\)", "\\(f\\) non è suriettiva su \\(\\mathbb{R}\\)"])

# ================= Limiti (8) =================
add("Limiti",
    r"Calcolare \( \displaystyle\lim_{x\to 0} \dfrac{1-\cos x}{x^2} \).",
    r"\(1/2\)", [r"\(1\)", r"\(0\)", r"\(+\infty\)"])

add("Limiti",
    r"Calcolare \( \displaystyle\lim_{x\to 0^+} x^{x} \).",
    r"\(1\)", [r"\(0\)", r"\(+\infty\)", "non esiste"])

add("Limiti",
    r"Usando gli sviluppi di Taylor, calcolare \( \displaystyle\lim_{x\to 0} \dfrac{e^{x}-1-x}{x^2} \).",
    r"\(1/2\)", [r"\(1\)", r"\(0\)", r"\(+\infty\)"])

add("Limiti",
    r"Calcolare \( \displaystyle\lim_{x\to +\infty} \left( \sqrt{x^2+x} - x \right) \).",
    r"\(1/2\)", [r"\(0\)", r"\(1\)", r"\(+\infty\)"])

add("Limiti",
    r"Osservando il grafico di \(f(x)\), quanto vale \( \displaystyle\lim_{x\to 1^-} f(x) \)?",
    r"\(1\)", [r"\(2{,}5\)", "non esiste", r"\(+\infty\)"], image="img1_piecewise.png")

add("Limiti",
    r"Dal grafico di \(f(x)\), il limite bilatero \( \displaystyle\lim_{x\to 1} f(x) \):",
    "non esiste, perché i limiti destro e sinistro sono diversi (rispettivamente \\(2{,}5\\) e \\(1\\))",
    ["esiste e vale \\(1\\)", "esiste e vale \\(2{,}5\\)", "vale \\(+\\infty\\)"], image="img1_piecewise.png")

add("Limiti",
    r"Osservando il grafico di \(p(x)\), il limite bilatero \( \displaystyle\lim_{x\to 1} p(x) \):",
    "non esiste, perché i limiti laterali sono infiniti di segno opposto",
    [r"vale \(+\infty\)", r"vale \(-\infty\)", r"vale \(2\)"], image="img5_asintoti.png")

add("Limiti",
    r"Osservando il grafico di \(p(x)\), quanto vale \( \displaystyle\lim_{x\to +\infty} p(x) \)?",
    r"\(2\)", [r"\(1\)", r"\(0\)", r"\(+\infty\)"], image="img5_asintoti.png")

# ================= Funzioni continue (4) =================
add("Funzioni continue",
    r"Sia \( f(x) = e^x + x - 3 \) su \( [0,2] \). Cosa si può concludere sull'equazione \(f(x)=0\)?",
    "poiché \\(f\\) è continua, \\(f(0)<0<f(2)\\) e \\(f'(x)=e^x+1>0\\) per ogni \\(x\\), esiste un'unica soluzione in \\((0,2)\\)",
    ["non esiste alcuna soluzione in \\((0,2)\\)", "esistono infinite soluzioni in \\((0,2)\\)", "esistono esattamente due soluzioni in \\((0,2)\\)"])

add("Funzioni continue",
    r"Per quale valore del parametro \(a\) la funzione \( f(x)=\begin{cases} ax+1 & x\le 1 \\ x^2+1 & x>1 \end{cases} \) è continua su \( \mathbb{R} \)?",
    r"\(a=1\)", [r"\(a=2\)", r"\(a=0\)", r"\(a=-1\)"])

add("Funzioni continue",
    r"La funzione \( f(x) = \dfrac1x \), definita su \( (0,1] \), ammette massimo assoluto?",
    "No, perché \\(f\\) è illimitata superiormente vicino a \\(x=0\\) (il dominio non è chiuso)",
    ["Sì, vale \\(1\\) in \\(x=1\\)", "Sì, vale \\(+\\infty\\)", "No, perché \\(f\\) non è continua"])

add("Funzioni continue",
    r"Classificare la discontinuità in \(x=0\) della funzione \( f(x) = \dfrac{|x|}{x} \) (per \(x\neq0\)), estesa con \(f(0)=0\).",
    "discontinuità di prima specie (salto finito di ampiezza \\(2\\), tra \\(-1\\) e \\(1\\))",
    ["discontinuità eliminabile", "discontinuità di seconda specie", "\\(f\\) è continua in \\(0\\)"])

# ================= Calcolo differenziale (17) =================
add("Calcolo differenziale",
    r"Calcolare la derivata di \( f(x) = x^{x} \), \( x>0 \).",
    r"\( f'(x) = x^{x}(\ln x + 1) \)", [r"\( f'(x) = x\cdot x^{x-1} \)", r"\( f'(x) = x^{x}\ln x \)", r"\( f'(x) = x^{x-1} \)"])

add("Calcolo differenziale",
    r"Calcolare la derivata di \( f(x) = \arctan\!\left(\dfrac1x\right) \), \( x\neq0 \).",
    r"\( f'(x) = -\dfrac{1}{1+x^2} \)", [r"\( f'(x) = \dfrac{1}{1+x^2} \)", r"\( f'(x) = -\dfrac{1}{x^2} \)", r"\( f'(x) = \dfrac{-1}{x^2+2} \)"])

add("Calcolo differenziale",
    r"Applicando il Teorema di Lagrange a \( f(x) = \ln x \) su \( [1,e] \), determinare il punto \(c\) la cui esistenza è garantita dal teorema.",
    r"\( c = e-1 \)", [r"\( c = e \)", r"\( c = 1 \)", r"\( c = \dfrac{e+1}{2} \)"])

add("Calcolo differenziale",
    r"Studiare la convessità di \( f(x) = x^4 - 6x^2 \): in quale intervallo \(f\) è concava (rivolge la concavità verso il basso)?",
    r"\( (-1,1) \)", [r"\( (-\infty,-1)\cup(1,+\infty) \)", r"\( (-\infty,+\infty) \)", "in nessun intervallo"])

add("Calcolo differenziale",
    r"Determinare il polinomio di Taylor di ordine \(2\), centrato in \(x_0=0\), di \( f(x) = \cos x \).",
    r"\( 1 - \dfrac{x^2}{2} \)", [r"\( 1 - x^2 \)", r"\( x - \dfrac{x^3}{6} \)", r"\( 1 + \dfrac{x^2}{2} \)"])

add("Calcolo differenziale",
    r"Determinare il valore massimo assoluto di \( f(x) = \dfrac{\ln x}{x} \) su \( (0,+\infty) \).",
    r"\( \dfrac1e \), raggiunto in \(x=e\)", [r"\(e\), raggiunto in \(x=1\)", r"\(1\), raggiunto in \(x=e^2\)", "non esiste, \\(f\\) è illimitata"])

add("Calcolo differenziale",
    r"Nel punto \(x=0\), il grafico di \( f(x) = x^3 - 3x + 1 \) presenta:",
    "un flesso a tangente obliqua (\\(f''(0)=0\\) cambia segno e \\(f'(0)=-3\\neq0\\))",
    ["un flesso a tangente orizzontale", "un massimo relativo", "un minimo relativo"])

add("Calcolo differenziale",
    r"Determinare gli asintoti orizzontali di \( f(x) = \dfrac{x^2-1}{x^2+1} \).",
    r"\( y=1 \), per \( x\to\pm\infty \)", [r"\( y=-1 \)", r"\( y=0 \)", "nessun asintoto orizzontale"])

add("Calcolo differenziale",
    r"Determinare il punto di massimo assoluto di \( f(x) = x\,e^{-x} \) su \( [0,+\infty) \).",
    r"\( x=1 \), con \( f(1) = 1/e \)", [r"\( x=0 \), con \( f(0)=0 \)", r"\( x=e \), con \( f(e)=1 \)", "non esiste massimo assoluto"])

add("Calcolo differenziale",
    r"Sia \( f(x) = x^2 \sin\!\left(\dfrac1x\right) \) per \(x\neq0\), \(f(0)=0\). La funzione è derivabile in \(x=0\)?",
    "Sì, \\(f'(0)=0\\), anche se \\(f'\\) non è continua in \\(0\\)",
    ["No, il limite del rapporto incrementale non esiste", "Sì, ma \\(f'(0)=1\\)", "No, \\(f\\) non è nemmeno continua in \\(0\\)"])

add("Calcolo differenziale",
    r"Osservando il grafico di \(g(x)\), in quale intervallo la funzione risulta decrescente?",
    r"\( (-1,1) \)", [r"\( (-\infty,-1) \)", r"\( (1,+\infty) \)", r"\( (-\infty,+\infty) \)"], image="img2_monotonia.png")

add("Calcolo differenziale",
    r"Osservando il grafico di \(g(x)\), il punto \(x=-1\) rappresenta:",
    "un massimo relativo", ["un minimo relativo", "un flesso", "un punto di non derivabilità"], image="img2_monotonia.png")

add("Calcolo differenziale",
    r"Osservando il grafico di \(g(x)\), il punto \(x=1\) rappresenta:",
    "un minimo relativo", ["un massimo relativo", "un flesso", "nessuno dei precedenti"], image="img2_monotonia.png")

add("Calcolo differenziale",
    r"Il grafico mostrato è quello di \(f'(x)\), derivata di \(f(x)\). In quale intervallo \(f(x)\) risulta crescente?",
    r"\( (-\infty,-1) \) e \( (2,+\infty) \)", [r"\( (-1,2) \)", r"\( (-\infty,+\infty) \)", "in nessun intervallo"], image="img3_derivata.png")

add("Calcolo differenziale",
    r"Dal grafico di \(f'(x)\), il punto \(x=-1\) rappresenta per \(f(x)\):",
    "un massimo relativo", ["un minimo relativo", "un flesso", "un punto angoloso"], image="img3_derivata.png")

add("Calcolo differenziale",
    r"Dal grafico di \(f'(x)\), il punto \(x=2\) rappresenta per \(f(x)\):",
    "un minimo relativo", ["un massimo relativo", "un flesso", "un asintoto"], image="img3_derivata.png")

add("Calcolo differenziale",
    r"Osservando il grafico di \( q(x) = x^3 \), nel punto \(x=0\) la funzione presenta:",
    "un flesso a tangente orizzontale", ["un massimo relativo", "un minimo relativo", "un punto di discontinuità"], image="img6_concavita.png")

# ================= Calcolo integrale (9) =================
add("Calcolo integrale",
    r"Calcolare \( \displaystyle\int x\,e^{x}\,dx \).",
    r"\( (x-1)e^{x} + C \)", [r"\( x\,e^{x} + C \)", r"\( e^{x} + C \)", r"\( (x+1)e^{x} + C \)"])

add("Calcolo integrale",
    r"Calcolare \( \displaystyle\int \ln x \; dx \) (per \(x>0\)).",
    r"\( x\ln x - x + C \)", [r"\( x\ln x + C \)", r"\( \dfrac{\ln x}{x} + C \)", r"\( \dfrac{x}{\ln x} + C \)"])

add("Calcolo integrale",
    r"Calcolare \( \displaystyle\int_0^{\pi} \sin^2 x \; dx \).",
    r"\( \pi/2 \)", [r"\( \pi \)", r"\(0\)", r"\(2\pi\)"])

add("Calcolo integrale",
    r"Calcolare l'area della regione compresa tra le curve \( y=x^2 \) e \( y=x+2 \).",
    r"\( 9/2 \)", [r"\(9\)", r"\(3\)", r"\(4\)"])

add("Calcolo integrale",
    r"L'integrale improprio \( \displaystyle\int_1^{+\infty} \dfrac{dx}{x^p} \) converge se e solo se:",
    r"\( p>1 \)", [r"\( p<1 \)", "per ogni \\(p\\)", "non converge mai"])

add("Calcolo integrale",
    r"Calcolare \( \displaystyle\int_0^{1} \dfrac{2x}{1+x^2}\,dx \).",
    r"\( \ln 2 \)", [r"\(1\)", r"\(2\)", r"\( \ln(1/2) \)"])

add("Calcolo integrale",
    r"Usando il Teorema fondamentale del calcolo integrale, calcolare \( \dfrac{d}{dx} \displaystyle\int_0^{x^2} e^{-t^2}\,dt \).",
    r"\( 2x\,e^{-x^4} \)", [r"\( e^{-x^4} \)", r"\( 2x\,e^{-x^2} \)", r"\( e^{-x^2} \)"])

add("Calcolo integrale",
    r"Osservando il grafico di \(h(x)\), l'area evidenziata tra \(x=-1\) e \(x=2\) rappresenta:",
    r"\( \displaystyle\int_{-1}^{2} h(x)\,dx \)", ["la derivata di \\(h\\) in quel punto", "il limite di \\(h\\) per \\(x\\to2\\)", "il dominio di \\(h\\)"], image="img4_area.png")

add("Calcolo integrale",
    r"Sapendo che \( h(x) = -x^2+4 \), calcolare l'area evidenziata nel grafico (tra \(x=-1\) e \(x=2\)).",
    r"\(9\)", [r"\(6\)", r"\(12\)", r"\(27\)"], image="img4_area.png")

assert len(Q) == 50, f"expected 50, got {len(Q)}"

out_path = os.path.join(os.path.dirname(__file__), "data", "questions.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(Q, f, ensure_ascii=False, indent=2)

print("Written", len(Q), "questions to", out_path)

from collections import Counter
print(Counter(q["topic"] for q in Q))
