from core.database import duck_conn
import pandas as pd

print("=" * 60)
print("MOTOR DE INÉRCIA TERAPÊUTICA")
print("=" * 60)

# ============================================================
# CARREGANDO DADOS
# ============================================================

print("\nCARREGANDO TABELAS...")

df_hba1c = duck_conn.execute("""

SELECT *
FROM exames_hba1c
WHERE vl_hemoglobina_glicada >= 8

""").fetchdf()

print(df_hba1c.columns)

# ============================================================
# PADRONIZANDO NOME DA COLUNA
# ============================================================

df_hba1c = df_hba1c.rename(
    columns={
        "vl_hemoglobina_glicada": "hba1c"
    }
)

print(df_hba1c.columns)

df_med = duck_conn.execute("""

SELECT *
FROM prescricoes_dm2

""").fetchdf()

print(f"HbA1c alteradas: {len(df_hba1c)}")
print(f"Prescrições: {len(df_med)}")

# ============================================================
# TRATANDO DATAS
# ============================================================

print("\nTRATANDO DATAS...")

df_hba1c["dt_resultado"] = pd.to_datetime(
    df_hba1c["dt_resultado"],
    errors="coerce"
)

df_med["dt_prescricao_atendimento"] = pd.to_datetime(
    df_med["dt_prescricao_atendimento"],
    errors="coerce"
)
# ============================================================
# LIMPEZA HbA1c
# ============================================================

df_hba1c = df_hba1c[
    (df_hba1c["hba1c"] >= 4)
    &
    (df_hba1c["hba1c"] <= 20)
]

# foco clínico DM descontrolado
df_hba1c = df_hba1c[
    df_hba1c["hba1c"] >= 8
]

print("\nHbA1c após limpeza:")
print(df_hba1c["hba1c"].describe())

# ============================================================
# REMOVENDO DATAS NULAS
# ============================================================

df_hba1c = df_hba1c.dropna(subset=["dt_resultado"])

print(f"\nExames válidos: {len(df_hba1c)}")

# ============================================================
# MOTOR DE INÉRCIA
# ============================================================

print("\nPROCESSANDO INÉRCIA...")

resultados = []

for _, exame in df_hba1c.iterrows():

    prontuario = exame["co_prontuario"]
    data_exame = exame["dt_resultado"]
    hba1c = exame["hba1c"]

    meds_pre = df_med[
        (df_med["co_seq_prontuario"] == prontuario)
        &
        (df_med["dt_prescricao_atendimento"] < data_exame)
    ]

    meds_pos = df_med[
        (df_med["co_seq_prontuario"] == prontuario)
        &
        (df_med["dt_prescricao_atendimento"] >= data_exame)
        &
        (
            df_med["dt_prescricao_atendimento"]
            <= data_exame + pd.Timedelta(days=180)
        )
    ]

    classes_pre = set(meds_pre["no_principio_ativo"].dropna())
    classes_pos = set(meds_pos["no_principio_ativo"].dropna())

    novas_classes = classes_pos - classes_pre

    intensificou = len(novas_classes) > 0

    resultados.append({
        "co_prontuario": prontuario,
        "data_exame": data_exame,
        "hba1c": hba1c,
        "n_classes_pre": len(classes_pre),
        "n_classes_pos": len(classes_pos),
        "n_novas_classes": len(novas_classes),
        "intensificou": intensificou,
        "inercia_terapeutica": not intensificou
    })

# ============================================================
# DATAFRAME FINAL
# ============================================================

df_final = pd.DataFrame(resultados)

print("\nDIMENSÃO FINAL:")
print(df_final.shape)

# ============================================================
# PREVALÊNCIA
# ============================================================

prev = (
    df_final["inercia_terapeutica"]
    .mean()
    * 100
)

print(f"\nPREVALÊNCIA DE INÉRCIA: {prev:.2f}%")

# ============================================================
# SALVANDO NO DUCKDB
# ============================================================

print("\nSALVANDO RESULTADOS...")

duck_conn.register("df_final", df_final)

duck_conn.execute("""

CREATE OR REPLACE TABLE tb_inercia_dm2 AS
SELECT * FROM df_final

""")

print("\nTABELA SALVA!")

print("\nPROCESSO FINALIZADO")
print("=" * 60)