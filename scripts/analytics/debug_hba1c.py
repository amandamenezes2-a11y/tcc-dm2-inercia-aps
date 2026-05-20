from core.database import pg_conn
import pandas as pd

print("=" * 60)
print("PROCURANDO HbA1c")
print("=" * 60)

query = """

SELECT table_name
FROM information_schema.columns
WHERE
    column_name ILIKE '%hba%'
    OR column_name ILIKE '%glica%'
    OR column_name ILIKE '%resultado%'
    OR column_name ILIKE '%hemoglobina%'

ORDER BY table_name

"""

df = pd.read_sql(query, pg_conn)

print(df)