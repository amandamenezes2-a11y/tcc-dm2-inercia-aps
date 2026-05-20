from core.database import pg_conn
import pandas as pd

print("=" * 60)
print("DEBUG PRONTUÁRIO")
print("=" * 60)

query = """

SELECT *
FROM tb_prontuario
LIMIT 5

"""

df = pd.read_sql(query, pg_conn)

print(df.head())

print("\nCOLUNAS:")
print(df.columns)