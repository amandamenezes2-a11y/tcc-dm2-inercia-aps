from core.database import duck_conn
import pandas as pd
import matplotlib.pyplot as plt

print("=" * 60)
print("SÉRIE TEMPORAL")
print("=" * 60)

# ============================================================
# CARREGANDO BASE
# ============================================================

df = duck_conn.execute("""

SELECT *
FROM tb_inercia_dm2

""").fetchdf()

print("\nBASE:")
print(df.shape)

# ============================================================
# DATAS
# ============================================================

df["data_exame"] = pd.to_datetime(df["data_exame"])

df["ano"] = df["data_exame"].dt.year

# ============================================================
# AGRUPANDO
# ============================================================

serie = df.groupby("ano")["inercia_terapeutica"] \
    .mean() \
    .reset_index()

serie["prevalencia"] = serie["inercia_terapeutica"] * 100

print("\nSÉRIE TEMPORAL:")
print(serie)

# ============================================================
# GRÁFICO
# ============================================================

plt.figure(figsize=(10,5))

plt.plot(
    serie["ano"],
    serie["prevalencia"],
    marker="o",
    linewidth=3
)

plt.title("Prevalência de Inércia Terapêutica ao Longo do Tempo")
plt.xlabel("Ano")
plt.ylabel("Prevalência (%)")

plt.grid(True)

# ============================================================
# EXPORTAÇÃO
# ============================================================

plt.savefig(
    "docs/figuras/serie_temporal_inercia.png",
    dpi=300,
    bbox_inches="tight"
)

print("\nFIGURA EXPORTADA!")

print("\nPROCESSO FINALIZADO")
print("=" * 60)