from core.database import duck_conn

import pandas as pd
import matplotlib.pyplot as plt

print("=" * 60)
print("INÉRCIA POR ESTRATO HbA1c")
print("=" * 60)

# ============================================================
# CARREGANDO BASE
# ============================================================

df = duck_conn.execute("""

SELECT *
FROM tb_inercia_enriquecida

""").fetchdf()

print("\nBASE:")
print(df.shape)

# ============================================================
# ESTRATOS HbA1c
# ============================================================

df["estrato_hba1c"] = pd.cut(

    df["hba1c"],

    bins=[8, 9, 10, 20],

    labels=[
        "8.0–8.9",
        "9.0–9.9",
        "≥10"
    ],

    include_lowest=True

)

# ============================================================
# PREVALÊNCIA
# ============================================================

prev = df.groupby(
    "estrato_hba1c"
)["inercia_terapeutica"] \
.mean() \
.reset_index()

prev["prevalencia"] = (
    prev["inercia_terapeutica"] * 100
)

print("\nPREVALÊNCIAS:")
print(prev)

# ============================================================
# GRÁFICO
# ============================================================

plt.figure(figsize=(8,5))

bars = plt.bar(
    prev["estrato_hba1c"],
    prev["prevalencia"]
)

# labels
for bar in bars:

    y = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width()/2,
        y + 1,
        f"{y:.1f}%",
        ha="center"
    )

plt.ylabel("Prevalência de inércia (%)")
plt.xlabel("Estratos HbA1c")
plt.title(
    "Prevalência de Inércia Terapêutica segundo HbA1c"
)

plt.ylim(0, 100)

plt.grid(
    axis="y",
    alpha=0.3
)

# ============================================================
# EXPORTAÇÃO
# ============================================================

plt.savefig(
    "docs/figuras/inercia_por_hba1c.png",
    dpi=300,
    bbox_inches="tight"
)

prev.to_csv(
    "data/results/inercia_por_hba1c.csv",
    index=False
)

print("\nARQUIVOS EXPORTADOS:")
print("- inercia_por_hba1c.png")
print("- inercia_por_hba1c.csv")

print("\nPROCESSO FINALIZADO")
print("=" * 60)