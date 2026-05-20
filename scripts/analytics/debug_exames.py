from core.database import pg_conn
import pandas as pd

print("=" * 60)
print("PROCURANDO TABELAS DE EXAMES")
print("=" * 60)

query = """

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
AND (
    table_name ILIKE '%exame%'
    OR table_name ILIKE '%resultado%'
    OR table_name ILIKE '%labor%'
    OR table_name ILIKE '%proced%'
    OR table_name ILIKE '%soap%'
)
ORDER BY table_name

"""

df = pd.read_sql(query, pg_conn)

print(df)