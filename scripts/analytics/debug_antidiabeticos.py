from core.database import pg_conn
import pandas as pd

print("=" * 60)
print("INSPECIONANDO TABELAS DE ANTIDIABÉTICOS")
print("=" * 60)

# ============================================================
# ESTRUTURA DA TABELA
# ============================================================

query = """

SELECT *
FROM base_prescricoes_antidiabeticos
LIMIT 5

"""

df = pd.read_sql(query, pg_conn)

print(df.head())

print("\n")
print("=" * 60)
print("COLUNAS")
print("=" * 60)

print(df.columns)