from core.database import duck_conn, pg_conn
import pandas as pd

print("=" * 60)
print("COORTE LONGITUDINAL DM2")
print("=" * 60)

# ============================================================
# EXTRAINDO HbA1c + PRONTUÁRIO
# ============================================================

print("\nEXTRAINDO EXAMES...")

query = """

SELECT
    er.co_prontuario,
    er.dt_resultado,
    hg.vl_hemoglobina_glicada

FROM tb_exame_hemoglobina_glicada hg

LEFT JOIN tb_exame_requisitado er
ON hg.co_exame_requisitado = er.co_seq_exame_requisitado

WHERE
    hg.vl_hemoglobina_glicada IS NOT NULL
    AND er.co_prontuario IS NOT NULL

"""

df_hba1c = pd.read_sql(query, pg_conn)

print(df_hba1c.head())

print("\nDIMENSÃO EXAMES:")
print(df_hba1c.shape)

# ============================================================
# EXTRAINDO PRESCRIÇÕES
# ============================================================

print("\nEXTRAINDO PRESCRIÇÕES...")

query_med = """

SELECT
    co_seq_prontuario,
    dt_prescricao_atendimento,
    no_principio_ativo

FROM base_prescricoes_antidiabeticos

WHERE
    dt_prescricao_atendimento IS NOT NULL

"""

df_med = pd.read_sql(query_med, pg_conn)

print(df_med.head())

print("\nDIMENSÃO PRESCRIÇÕES:")
print(df_med.shape)

# ============================================================
# SALVANDO NO DUCKDB
# ============================================================

print("\nSALVANDO TABELAS ANALÍTICAS...")

duck_conn.register("df_hba1c", df_hba1c)
duck_conn.register("df_med", df_med)

duck_conn.execute("""

CREATE OR REPLACE TABLE exames_hba1c AS
SELECT * FROM df_hba1c

""")

duck_conn.execute("""

CREATE OR REPLACE TABLE prescricoes_dm2 AS
SELECT * FROM df_med

""")

print("\nTABELAS SALVAS!")

# ============================================================
# VALIDAÇÃO
# ============================================================

total_hba1c = duck_conn.execute("""

SELECT COUNT(*)
FROM exames_hba1c

""").fetchone()[0]

total_med = duck_conn.execute("""

SELECT COUNT(*)
FROM prescricoes_dm2

""").fetchone()[0]

print(f"\nTOTAL HbA1c: {total_hba1c}")
print(f"TOTAL PRESCRIÇÕES: {total_med}")

print("\nPROCESSO FINALIZADO")
print("=" * 60)