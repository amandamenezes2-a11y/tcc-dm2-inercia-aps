from core.database import duck_conn

import pandas as pd

print("=" * 60)
print("TABELA 1 - CARACTERÍSTICAS DA COORTE")
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
# INDICADORES
# ============================================================

n = len(df)

idade_media = round(
    df["idade"].mean(),
    1
)

idade_dp = round(
    df["idade"].std(),
    1
)

hba1c_media = round(
    df["hba1c"].mean(),
    1
)

hba1c_dp = round(
    df["hba1c"].std(),
    1
)

# ============================================================
# SEXO
# ============================================================

feminino = len(
    df[df["sexo"] == "Feminino"]
)

masculino = len(
    df[df["sexo"] == "Masculino"]
)

feminino_pct = round(
    feminino / n * 100,
    1
)

masculino_pct = round(
    masculino / n * 100,
    1
)

# ============================================================
# INÉRCIA
# ============================================================

inercia_pct = round(
    df["inercia_terapeutica"].mean() * 100,
    1
)

intensificacao_pct = round(
    df["intensificou"].mean() * 100,
    1
)

# ============================================================
# HbA1c ≥10
# ============================================================

hba1c_10 = len(
    df[df["hba1c"] >= 10]
)

hba1c_10_pct = round(
    hba1c_10 / n * 100,
    1
)

# ============================================================
# TABELA
# ============================================================

tabela1 = pd.DataFrame({

    "Variavel": [

        "Número de pacientes",
        "Idade média (DP)",
        "Sexo feminino",
        "Sexo masculino",
        "HbA1c média (DP)",
        "HbA1c ≥10%",
        "Prevalência de inércia",
        "Intensificação terapêutica"

    ],

    "Resultado": [

        f"{n}",

        f"{idade_media} ({idade_dp})",

        f"{feminino} ({feminino_pct}%)",

        f"{masculino} ({masculino_pct}%)",

        f"{hba1c_media} ({hba1c_dp})",

        f"{hba1c_10} ({hba1c_10_pct}%)",

        f"{inercia_pct}%",

        f"{intensificacao_pct}%"

    ]

})

# ============================================================
# RESULTADO
# ============================================================

print("\nTABELA 1:")
print(tabela1)

# ============================================================
# EXPORTAÇÃO
# ============================================================

tabela1.to_csv(
    "data/results/tabela1_coorte.csv",
    index=False
)

tabela1.to_excel(
    "data/results/tabela1_coorte.xlsx",
    index=False
)

print("\nARQUIVOS EXPORTADOS:")
print("- tabela1_coorte.csv")
print("- tabela1_coorte.xlsx")

print("\nPROCESSO FINALIZADO")
print("=" * 60)