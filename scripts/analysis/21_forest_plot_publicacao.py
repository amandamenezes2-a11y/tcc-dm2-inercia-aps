import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# DADOS
# ============================================================

df = pd.DataFrame({
    "Variavel": [
        "Idade",
        "Sexo masculino",
        "HbA1c contínua",
        "HbA1c ≥10%"
    ],
    "OR": [
        0.997,
        1.03,
        1.016,
        0.61
    ],
    "IC_inf": [
        0.992,
        0.89,
        1.00,
        0.53
    ],
    "IC_sup": [
        1.002,
        1.20,
        1.03,
        0.71
    ]
})

# ============================================================
# FIGURA
# ============================================================

fig, ax = plt.subplots(figsize=(8, 4))

ax.errorbar(
    df["OR"],
    df["Variavel"],
    xerr=[
        df["OR"] - df["IC_inf"],
        df["IC_sup"] - df["OR"]
    ],
    fmt='o'
)

ax.axvline(
    1,
    linestyle='--'
)

ax.set_xlabel("Odds Ratio (IC95%)")
ax.set_title("Fatores associados à inércia terapêutica")

plt.tight_layout()

# ============================================================
# EXPORTAÇÃO
# ============================================================

plt.savefig(
    "docs/figuras/forest_plot_publicacao.png",
    dpi=300,
    bbox_inches="tight"
)

print("\nFIGURA EXPORTADA:")
print("docs/figuras/forest_plot_publicacao.png")