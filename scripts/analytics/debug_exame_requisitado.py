from core.database import pg_conn
import pandas as pd

print("=" * 60)
print("INSPECIONANDO EXAME REQUISITADO")
print("=" * 60)

query = """

SELECT *
FROM tb_exame_requisitado
LIMIT 10

"""

df = pd.read_sql(query, pg_conn)

print(df)

print("\n")
print("=" * 60)
print("COLUNAS")
print("=" * 60)

print(df.columns)