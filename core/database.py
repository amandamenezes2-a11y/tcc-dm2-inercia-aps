import duckdb
import psycopg2

# ============================================================
# CONEXÃO DUCKDB
# ============================================================

duck_conn = duckdb.connect(
    database="data/duckdb/inercia_aps.duckdb",
    read_only=False
)



# ============================================================
# EXTENSÃO POSTGRES DUCKDB
# ============================================================

duck_conn.execute("INSTALL postgres")
duck_conn.execute("LOAD postgres")
duck_conn.execute("PRAGMA threads=4")

# ============================================================
# CONEXÃO POSTGRES E-SUS
# ============================================================

PG_HOST = "localhost"
PG_PORT = "5432"
PG_DB = "esus_completa"
PG_USER = "postgres"
PG_PASSWORD = "esusapsufba"

pg_conn = psycopg2.connect(
    host=PG_HOST,
    port=PG_PORT,
    database=PG_DB,
    user=PG_USER,
    password=PG_PASSWORD
)

print("=" * 60)
print("CONEXÕES ATIVAS")
print("=" * 60)