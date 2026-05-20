from core.database import duck_conn

print("=" * 60)
print("LISTANDO TABELAS")
print("=" * 60)

tabelas = duck_conn.execute("""

SHOW TABLES

""").fetchdf()

print(tabelas)