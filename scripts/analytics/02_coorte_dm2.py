from core.database import duck_conn

print("=" * 60)
print("CONSTRUÇÃO DA COORTE DM2")
print("=" * 60)

# ============================================================
# CRIANDO COORTE ANALÍTICA
# ============================================================

print("\nCRIANDO COORTE...")

duck_conn.execute("""

CREATE OR REPLACE TABLE coorte_dm2 AS

SELECT
    co_seq_cidadao,
    co_prontuario,
    nu_cpf_cidadao,
    no_cidadao,
    dt_nascimento,
    co_dim_sexo,
    nu_altura,
    nu_peso,
    nu_resultado,
    dt_resultado,

    CASE
        WHEN CAST(nu_resultado AS DOUBLE) >= 8
        THEN 1
        ELSE 0
    END AS hba1c_alterada

FROM tb_cidadao_aps

WHERE
    nu_resultado IS NOT NULL

""")

print("COORTE CRIADA!")

# ============================================================
# VALIDANDO
# ============================================================

total = duck_conn.execute("""

SELECT COUNT(*)
FROM coorte_dm2

""").fetchone()[0]

print(f"\nTOTAL DE REGISTROS: {total}")

# ============================================================
# HBA1C >= 8
# ============================================================

alterados = duck_conn.execute("""

SELECT COUNT(*)
FROM coorte_dm2
WHERE hba1c_alterada = 1

""").fetchone()[0]

print(f"HbA1c >= 8%: {alterados}")

print("\nPROCESSO FINALIZADO")
print("=" * 60)