from core.database import pg_conn
import pandas as pd

print("=" * 60)
print("TIPOS DE EXAMES")
print("=" * 60)

query = """

SELECT *
FROM tl_tipo_exame
LIMIT 20

"""

df = pd.read_sql(query, pg_conn)

print(df)

print("\n")
print("=" * 60)
print("COLUNAS")
print("=" * 60)

print(df.columns)