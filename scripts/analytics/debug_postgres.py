from core.database import pg_conn
import pandas as pd

print("=" * 60)
print("TABELAS DO POSTGRES e-SUS")
print("=" * 60)

query = """

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name

"""

df = pd.read_sql(query, pg_conn)

print(df)