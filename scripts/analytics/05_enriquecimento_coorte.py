from core.database import duck_conn, pg_conn

import pandas as pd

print("=" * 60)
print("ENRIQUECIMENTO DA COORTE")
print("=" * 60)

# ============================================================
# CARREGANDO COORTE
# ============================================================

coorte = duck_conn.execute("""

SELECT *
FROM tb_inercia_dm2

""").fetchdf()

print("\nCOORTE:")
print(coorte.shape)

# ============================================================
# DADOS DEMOGRÁFICOS
# ============================================================

print("\nEXTRAINDO DADOS DEMOGRÁFICOS...")

query = """

SELECT

    p.co_seq_prontuario,
    c.co_seq_cidadao,
    c.no_sexo,
    c.dt_nascimento

FROM tb_prontuario p

LEFT JOIN tb_cidadao c
    ON p.co_cidadao = c.co_seq_cidadao

"""

df_demo = pd.read_sql(query, pg_conn)

print(df_demo.head())

print("\nDIMENSÃO DEMOGRÁFICA:")
print(df_demo.shape)

# ============================================================
# JOIN
# ============================================================

print("\nREALIZANDO JOIN...")

coorte = coorte.merge(
    df_demo,
    left_on="co_prontuario",
    right_on="co_seq_prontuario",
    how="left"
)

# ============================================================
# DATAS
# ============================================================

print("\nCALCULANDO IDADE...")

coorte["dt_nascimento"] = pd.to_datetime(
    coorte["dt_nascimento"],
    errors="coerce"
)

coorte["idade"] = (
    pd.to_datetime("today") - coorte["dt_nascimento"]
).dt.days / 365.25

# ============================================================
# MANTER APENAS ADULTOS
# ============================================================

coorte = coorte[
    coorte["idade"] >= 18
]

# ============================================================
# SEXO
# ============================================================

coorte["sexo"] = coorte["no_sexo"].replace({
    "MASCULINO": "Masculino",
    "FEMININO": "Feminino"
})

# ============================================================
# COLUNAS
# ============================================================

print("\nCOLUNAS:")
print(coorte.columns)

# ============================================================
# RESULTADOS
# ============================================================

print("\nDIMENSÃO FINAL:")
print(coorte.shape)

print("\nSEXO:")
print(
    coorte["sexo"].value_counts()
)

print("\nIDADE:")
print(
    coorte["idade"].describe()
)

# ============================================================
# SALVANDO
# ============================================================

print("\nSALVANDO TABELA...")

duck_conn.execute("""
DROP TABLE IF EXISTS tb_inercia_enriquecida
""")

duck_conn.register(
    "coorte_temp",
    coorte
)

duck_conn.execute("""

CREATE TABLE tb_inercia_enriquecida AS
SELECT *
FROM coorte_temp

""")

print("\nTABELA SALVA!")

print("\nPROCESSO FINALIZADO")
print("=" * 60)