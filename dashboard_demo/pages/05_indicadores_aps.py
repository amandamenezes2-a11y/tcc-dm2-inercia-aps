import streamlit as st
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
# BASE DEMO
# ============================================================

df = pd.read_csv(
    "data/demo/coorte_demo.csv"
)

# ============================================================
# INDICADORES
# ============================================================

prevalencia = (
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
    f"{prevalencia:.1f}%"
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

fig, ax = plt.subplots(figsize=(8,5))

ax.bar(
    ["Inércia", "Criticidade"],
    [prevalencia, taxa_criticos]
)

ax.set_ylabel("%")

st.pyplot(fig)

# ============================================================
# INTERPRETAÇÃO
# ============================================================

st.subheader("Interpretação Clínica")

if prevalencia >= 50:

    st.error("""
Alta prevalência de inércia terapêutica.
Necessidade de intervenção prioritária.
""")

else:

    st.success("""
Indicadores dentro de parâmetros aceitáveis.
""")

# ============================================================
# FINAL
# ============================================================

st.success(
    "Indicadores APS demo carregados."
)