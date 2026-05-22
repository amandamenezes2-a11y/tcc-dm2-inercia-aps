import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Série Temporal",
    layout="wide"
)

st.title("📈 Monitoramento Longitudinal")
st.markdown("---")

# ============================================================
# BASE DEMO
# ============================================================

df = pd.read_csv(
    "data/demo/coorte_demo.csv"
)

# ============================================================
# DATA DEMO
# ============================================================

df["data_evento"] = pd.date_range(
    start="2024-01-01",
    periods=len(df),
    freq="D"
)

# ============================================================
# CONVERSÃO
# ============================================================

df["data_evento"] = pd.to_datetime(
    df["data_evento"]
)

# ============================================================
# AGREGAÇÃO
# ============================================================

serie = (
    df
    .groupby(
        pd.Grouper(
            key="data_evento",
            freq="ME"
        )
    )["inercia_terapeutica"]
    .mean()
    .reset_index()
)

serie["inercia_terapeutica"] = (
    serie["inercia_terapeutica"] * 100
)

# ============================================================
# KPIs
# ============================================================

col1, col2 = st.columns(2)

col1.metric(
    "Prevalência Média",
    f"{serie['inercia_terapeutica'].mean():.1f}%"
)

col2.metric(
    "Meses Monitorados",
    len(serie)
)

st.markdown("---")

# ============================================================
# GRÁFICO
# ============================================================

fig, ax = plt.subplots(figsize=(12,5))

ax.plot(
    serie["data_evento"],
    serie["inercia_terapeutica"],
    linewidth=3
)

ax.set_ylabel("Prevalência (%)")
ax.set_xlabel("Tempo")

ax.grid(True)

st.pyplot(fig)

# ============================================================
# TABELA
# ============================================================

st.dataframe(
    serie,
    use_container_width=True
)

# ============================================================
# FINAL
# ============================================================

st.success(
    "Série temporal demo carregada."
)