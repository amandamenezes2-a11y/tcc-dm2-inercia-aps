import streamlit as st
import duckdb
import pandas as pd

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Monitoramento Clínico",
    layout="wide"
)

st.title("📌 Monitoramento Clínico")
st.markdown("---")

# ============================================================
# DUCKDB
# ============================================================

conn = duckdb.connect(
    "data/duckdb/inercia_aps.duckdb",
    read_only=True
)

df = conn.execute("""

SELECT *
FROM tb_inercia_dm2

""").fetchdf()

# ============================================================
# ESTRATIFICAÇÃO
# ============================================================

def classificar_risco(hba1c):

    if hba1c < 7:
        return "Baixo"

    elif hba1c < 9:
        return "Moderado"

    elif hba1c < 10:
        return "Alto"

    else:
        return "Crítico"

df["risco_clinico"] = (
    df["hba1c"]
    .apply(classificar_risco)
)

# ============================================================
# FILTROS
# ============================================================

st.sidebar.title("Filtros")

risco = st.sidebar.multiselect(
    "Risco Clínico",
    ["Baixo", "Moderado", "Alto", "Crítico"],
    default=["Crítico"]
)

df = df[
    df["risco_clinico"].isin(risco)
]

# ============================================================
# KPIs
# ============================================================

col1, col2, col3 = st.columns(3)

col1.metric(
    "Pacientes",
    len(df)
)

col2.metric(
    "HbA1c Média",
    round(df["hba1c"].mean(), 2)
)

col3.metric(
    "Prevalência Inércia",
    f"{df['inercia_terapeutica'].mean()*100:.1f}%"
)

st.markdown("---")

# ============================================================
# TABELA
# ============================================================

st.subheader("Pacientes Monitorados")

st.dataframe(
    df,
    use_container_width=True
)

# ============================================================
# DOWNLOAD
# ============================================================

csv = df.to_csv(index=False)

st.download_button(
    "📥 Download CSV",
    csv,
    "monitoramento_clinico.csv",
    "text/csv"
)

# ============================================================
# FINAL
# ============================================================

st.success("Monitoramento clínico carregado.")