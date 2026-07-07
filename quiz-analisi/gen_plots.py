import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os

OUT = os.path.join(os.path.dirname(__file__), "public", "images")
os.makedirs(OUT, exist_ok=True)

def style(ax):
    ax.axhline(0, color="black", linewidth=1)
    ax.axvline(0, color="black", linewidth=1)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

# 1. Piecewise function with jump discontinuity at x=1
fig, ax = plt.subplots(figsize=(5,4))
x1 = np.linspace(-2, 1, 200)
y1 = x1**2
x2 = np.linspace(1, 3, 200)
y2 = x2 + 1.5
ax.plot(x1, y1, color="#2563eb", linewidth=2.5)
ax.plot(x2, y2, color="#2563eb", linewidth=2.5)
ax.plot(1, 1, 'o', color="#2563eb", markerfacecolor='white', markersize=8, markeredgewidth=2)
ax.plot(1, 2.5, 'o', color="#2563eb", markersize=8)
style(ax)
ax.set_xlim(-2.5, 3.5)
ax.set_ylim(-1, 6)
ax.set_title("Grafico di f(x)")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "img1_piecewise.png"), dpi=130)
plt.close()

# 2. Cubic-like function for monotonicity
fig, ax = plt.subplots(figsize=(5,4))
x = np.linspace(-2.5, 2.5, 400)
y = x**3 - 3*x
ax.plot(x, y, color="#16a34a", linewidth=2.5)
style(ax)
ax.set_xlim(-3, 3)
ax.set_ylim(-4, 4)
ax.set_title("Grafico di g(x)")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "img2_monotonia.png"), dpi=130)
plt.close()

# 3. Derivative graph: parabola crossing x-axis at -1 and 2 (f'(x))
fig, ax = plt.subplots(figsize=(5,4))
x = np.linspace(-3, 4, 400)
y = (x+1)*(x-2)
ax.plot(x, y, color="#dc2626", linewidth=2.5)
ax.axhline(0, color="black", linewidth=1)
style(ax)
ax.set_xlim(-3, 4)
ax.set_ylim(-3, 6)
ax.set_title("Grafico di f '(x), derivata di f(x)")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "img3_derivata.png"), dpi=130)
plt.close()

# 4. Area under curve for integral (f(x) = -x^2+4 from -1 to 2, shaded)
fig, ax = plt.subplots(figsize=(5,4))
x = np.linspace(-2.3, 2.3, 400)
y = -x**2 + 4
ax.plot(x, y, color="#7c3aed", linewidth=2.5)
xf = np.linspace(-1, 2, 200)
yf = -xf**2 + 4
ax.fill_between(xf, 0, yf, color="#7c3aed", alpha=0.25)
style(ax)
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-1, 5)
ax.set_title("Area sottesa al grafico di h(x) tra x=-1 e x=2")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "img4_area.png"), dpi=130)
plt.close()

# 5. Function with horizontal and vertical asymptote: f(x) = (2x+1)/(x-1)
fig, ax = plt.subplots(figsize=(5,4))
x_left = np.linspace(-4, 0.85, 300)
x_right = np.linspace(1.15, 6, 300)
def f(x): return (2*x+1)/(x-1)
ax.plot(x_left, f(x_left), color="#0891b2", linewidth=2.5)
ax.plot(x_right, f(x_right), color="#0891b2", linewidth=2.5)
ax.axvline(1, color="gray", linestyle=":", linewidth=1.5)
ax.axhline(2, color="gray", linestyle=":", linewidth=1.5)
style(ax)
ax.set_xlim(-4, 6)
ax.set_ylim(-6, 10)
ax.set_title("Grafico di p(x)")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "img5_asintoti.png"), dpi=130)
plt.close()

# 6. Inflection point graph: f(x) = x^3
fig, ax = plt.subplots(figsize=(5,4))
x = np.linspace(-2, 2, 400)
y = x**3
ax.plot(x, y, color="#ea580c", linewidth=2.5)
ax.plot(0, 0, 'o', color="black", markersize=6)
style(ax)
ax.set_xlim(-2.2, 2.2)
ax.set_ylim(-8, 8)
ax.set_title("Grafico di q(x)")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "img6_concavita.png"), dpi=130)
plt.close()

print("done")
