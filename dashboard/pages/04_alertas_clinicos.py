import streamlit as st
import duckdb
import pandas as pd

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Alertas Clínicos",
    layout="wide"
)

st.title("🚨 Alertas Clínicos")
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
# CRITÉRIOS DE ALERTA
# ============================================================

alertas = df[
    (
        df["hba1c"] >= 10
    )
    &
    (
        df["inercia_terapeutica"] == True
    )
]

# ============================================================
# CLASSIFICAÇÃO
# ============================================================

def classificar_alerta(hba1c):

    if hba1c >= 12:
        return "🔴 Crítico"

    elif hba1c >= 10:
        return "🟠 Alto"

    else:
        return "🟡 Moderado"

alertas["nivel_alerta"] = (
    alertas["hba1c"]
    .apply(classificar_alerta)
)

# ============================================================
# KPIs
# ============================================================

col1, col2, col3 = st.columns(3)

col1.metric(
    "Pacientes em Alerta",
    len(alertas)
)

col2.metric(
    "HbA1c Média",
    round(alertas["hba1c"].mean(), 2)
)

col3.metric(
    "Maior HbA1c",
    round(alertas["hba1c"].max(), 2)
)

st.markdown("---")

# ============================================================
# ALERTAS
# ============================================================

st.subheader("Pacientes Prioritários para Intervenção")

st.dataframe(
    alertas.sort_values(
        "hba1c",
        ascending=False
    ),
    use_container_width=True
)

# ============================================================
# DOWNLOAD
# ============================================================

csv = alertas.to_csv(index=False)

st.download_button(
    "📥 Download CSV",
    csv,
    "alertas_clinicos.csv",
    "text/csv"
)

# ============================================================
# FINAL
# ============================================================

st.success(
    "Sistema de alertas carregado."
)