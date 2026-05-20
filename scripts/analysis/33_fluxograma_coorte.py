import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

print("=" * 60)
print("FLUXOGRAMA DA COORTE")
print("=" * 60)

# ============================================================
# NÚMEROS DA COORTE
# ============================================================

n_total = 39267
n_hba1c_alterada = 9348
n_validos = 3514
n_final = 3500

# ============================================================
# FIGURA
# ============================================================

fig, ax = plt.subplots(figsize=(8, 10))

ax.set_xlim(0, 10)
ax.set_ylim(0, 12)

ax.axis("off")

# ============================================================
# FUNÇÃO BOX
# ============================================================

def caixa(x, y, texto):

    box = FancyBboxPatch(

        (x, y),
        6,
        1.2,

        boxstyle="round,pad=0.05",

        linewidth=1.5,
        edgecolor="black",
        facecolor="#E8F0FE"
    )

    ax.add_patch(box)

    ax.text(

        x + 3,
        y + 0.6,

        texto,

        ha="center",
        va="center",
        fontsize=11

    )

# ============================================================
# BOXES
# ============================================================

caixa(
    2,
    10,
    "HbA1c identificados\nn = 39.267"
)

caixa(
    2,
    7,
    "HbA1c ≥8%\nn = 9.348"
)

caixa(
    2,
    4,
    "Exames válidos\nn = 3.514"
)

caixa(
    2,
    1,
    "Coorte final\nn = 3.500"
)

# ============================================================
# SETAS
# ============================================================

ax.annotate(
    "",
    xy=(5, 8.2),
    xytext=(5, 9.9),
    arrowprops=dict(arrowstyle="->", lw=2)
)

ax.annotate(
    "",
    xy=(5, 5.2),
    xytext=(5, 6.9),
    arrowprops=dict(arrowstyle="->", lw=2)
)

ax.annotate(
    "",
    xy=(5, 2.2),
    xytext=(5, 3.9),
    arrowprops=dict(arrowstyle="->", lw=2)
)

# ============================================================
# TEXTO EXCLUSÕES
# ============================================================

ax.text(
    8.3,
    8.8,

    "- HbA1c <8%\n"
    "- sem seguimento",

    fontsize=10
)

ax.text(
    8.3,
    5.8,

    "- dados inconsistentes\n"
    "- idade <18 anos",

    fontsize=10
)

# ============================================================
# TÍTULO
# ============================================================

plt.title(
    "Fluxograma de Seleção da Coorte",
    fontsize=14,
    weight="bold"
)

# ============================================================
# EXPORTAÇÃO
# ============================================================

import os

os.makedirs(
    "docs/figuras",
    exist_ok=True
)

plt.savefig(

    "docs/figuras/fluxograma_coorte.png",

    dpi=300,
    bbox_inches="tight"

)

print("\nARQUIVO EXPORTADO:")
print("docs/figuras/fluxograma_coorte.png")

print("\nPROCESSO FINALIZADO")
print("=" * 60)