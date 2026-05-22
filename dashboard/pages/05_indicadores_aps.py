import streamlit as st
import duckdb
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Indicadores APS",
    layout="wide"
)

st.title("🏥 Indicadores Estratégicos APS")
st.markdown("---")

# ============================================================
# DUCKDB
# ============================================================

conn = duckdb.connect(
    "data/duckdb/inercia_aps.duckdb",
    read_only=True
)

# ============================================================
# DADOS
# ============================================================

df = conn.execute("""

SELECT *
FROM tb_inercia_dm2

""").fetchdf()

# ============================================================
# INDICADORES
# ============================================================

prevalencia_inercia = (
    df["inercia_terapeutica"]
    .mean()
    * 100
)

media_hba1c = (
    df["hba1c"]
    .mean()
)

criticos = len(
    df[df["hba1c"] >= 10]
)

total = len(df)

taxa_criticos = (
    criticos / total
) * 100

# ============================================================
# KPIs
# ============================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Prevalência de Inércia",
    f"{prevalencia_inercia:.1f}%"
)

col2.metric(
    "HbA1c Média",
    f"{media_hba1c:.2f}"
)

col3.metric(
    "Pacientes Críticos",
    criticos
)

col4.metric(
    "Taxa de Criticidade",
    f"{taxa_criticos:.1f}%"
)

st.markdown("---")

# ============================================================
# GRÁFICO
# ============================================================

st.subheader("Indicadores Estratégicos")

indicadores = pd.DataFrame({
    "Indicador": [
        "Inércia",
        "Criticidade"
    ],
    "Valor": [
        prevalencia_inercia,
        taxa_criticos
    ]
})

fig, ax = plt.subplots(figsize=(8,5))

ax.bar(
    indicadores["Indicador"],
    indicadores["Valor"]
)

ax.set_ylabel("%")

st.pyplot(fig)

# ============================================================
# INTERPRETAÇÃO
# ============================================================

st.subheader("Interpretação Clínica")

if prevalencia_inercia >= 50:

    st.error("""
Alta prevalência de inércia terapêutica.
Necessidade de intervenção prioritária.
""")

else:

    st.success("""
Indicadores dentro de parâmetros aceitáveis.
""")

# ============================================================
# TABELA
# ============================================================

st.subheader("Base Analítica")

st.dataframe(
    df.head(100),
    use_container_width=True
)

# ============================================================
# DOWNLOAD
# ============================================================

csv = df.to_csv(index=False)

st.download_button(
    "📥 Download Base",
    csv,
    "base_analitica.csv",
    "text/csv"
)

# ============================================================
# FINAL
# ============================================================

st.success(
    "Indicadores APS carregados."
)