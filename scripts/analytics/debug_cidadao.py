from core.database import pg_conn
import pandas as pd

print("=" * 60)
print("DEBUG TABELA CIDADÃO")
print("=" * 60)

query = """

SELECT *
FROM tb_cidadao
LIMIT 5

"""

df = pd.read_sql(query, pg_conn)

print(df.head())

print("\nCOLUNAS:")
print(df.columns)