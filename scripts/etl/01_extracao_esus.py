from core.database import duck_conn

print("=" * 60)
print("EXTRAÇÃO POSTGRES → DUCKDB")
print("=" * 60)

# ============================================================
# EXTRAÇÃO DIRETA POSTGRES
# ============================================================

query = """
SELECT
    co_seq_fat_cidadao_pec,
    nu_cpf_cidadao,
    no_cidadao,
    dt_nascimento
FROM tb_cidadao
LIMIT 1000
"""

print("\nLENDO POSTGRES...")

df = duck_conn.execute(f"""
SELECT *
FROM postgres_scan(
    'host=localhost port=5432 dbname=esus_completa user=postgres password=esusapsufba',
    'public',
    'tb_cidadao'
)
LIMIT 1000
""").df()

print("\nDIMENSÃO:")
print(df.shape)

# ============================================================
# SALVANDO NO DUCKDB
# ============================================================

print("\nSALVANDO TABELA ANALÍTICA...")

duck_conn.register("df_temp", df)

duck_conn.execute("""
CREATE OR REPLACE TABLE tb_cidadao_aps AS
SELECT *
FROM df_temp
""")

print("\nTABELA SALVA NO DUCKDB!")

# ============================================================
# VALIDAÇÃO
# ============================================================

resultado = duck_conn.execute("""
SELECT COUNT(*)
FROM tb_cidadao_aps
""").fetchone()[0]

print(f"\nREGISTROS NA TABELA: {resultado}")

print("\nPROCESSO FINALIZADO")
print("=" * 60)