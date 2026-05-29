import streamlit as st
import pandas as pd
from io import BytesIO

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
# BASE DEMO
# ============================================================

df = pd.read_csv(
    "data/demo/coorte_demo.csv"
)

# ============================================================
# ALERTAS
# ============================================================

alertas = df[
    (
        df["hba1c"] >= 10
    )
    &
    (
        df["inercia_terapeutica"] == 1
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
# TABELA
# ============================================================

st.dataframe(
    alertas.sort_values(
        "hba1c",
        ascending=False
    ),
    width="stretch"
)

# ============================================================
# FINAL
# ============================================================

st.success(
    "Alertas demo carregados."
)