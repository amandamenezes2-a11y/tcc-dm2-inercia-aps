import streamlit as st
import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# =========================================================
# CONFIGURAÇÃO
# =========================================================

st.set_page_config(
    page_title="Vigilância DM2 APS",
    layout="wide"
)

# =========================================================
# TÍTULO
# =========================================================

st.title("📊 Vigilância Clínica DM2")

st.markdown(
    """
    Dashboard operacional para monitoramento longitudinal
    de indivíduos com Diabetes Mellitus tipo 2.
    """
)

# =========================================================
# MODO DEMO
# =========================================================

MODO_DEMO = True

# =========================================================
# CARREGAMENTO DOS DADOS
# =========================================================

if MODO_DEMO:

    df = pd.read_csv(
        "data/demo/coorte_demo.csv"
    )

    df["co_prontuario"] = range(1, len(df) + 1)

else:

    conn = duckdb.connect(
        "data/duckdb/inercia_aps.duckdb"
    )

    df = conn.execute("""
        SELECT *
        FROM tb_inercia_dm2
    """).fetchdf()

# =========================================================
# PADRONIZAÇÃO
# =========================================================

df.columns = [c.lower() for c in df.columns]

# cria sexo fake caso não exista
if "sexo" not in df.columns:

    np.random.seed(42)

    df["sexo"] = np.random.choice(
        ["Masculino", "Feminino"],
        size=len(df)
    )

# cria inércia terapêutica
if "inercia_terapeutica" not in df.columns:

    df["inercia_terapeutica"] = (
        df["hba1c"] >= 8
    ).astype(int)

# =========================================================
# CLASSIFICAÇÃO DE RISCO
# =========================================================

def classificar_risco(hba1c):

    if hba1c >= 11:
        return "Crítico"

    elif hba1c >= 9:
        return "Moderado"

    else:
        return "Alto"

df["risco"] = df["hba1c"].apply(
    classificar_risco
)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("## 📌 Vigilância Clínica APS")

st.sidebar.markdown(
    """
    Sistema de monitoramento longitudinal
    de inércia terapêutica
    em Diabetes Mellitus tipo 2.
    """
)

# filtro sexo
sexo = st.sidebar.multiselect(
    "Sexo",
    options=df["sexo"].unique(),
    default=df["sexo"].unique()
)

df = df[df["sexo"].isin(sexo)]

# filtro HbA1c
hba1c_min = st.sidebar.slider(
    "HbA1c mínima",
    min_value=float(df["hba1c"].min()),
    max_value=float(df["hba1c"].max()),
    value=7.0
)

df = df[df["hba1c"] >= hba1c_min]

st.sidebar.info(
    "Base demonstrativa anonimizada."
)

# =========================================================
# MÉTRICAS
# =========================================================

prevalencia = (
    df["inercia_terapeutica"].mean() * 100
)

hba1c_media = df["hba1c"].mean()

pacientes = len(
    df["co_prontuario"].unique()
)

eventos = len(df)

risco_critico = (
    df[df["risco"] == "Crítico"]
    .shape[0]
)

# =========================================================
# KPIs
# =========================================================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:

    st.metric(
        "Prevalência",
        f"{prevalencia:.1f}%"
    )

with col2:

    st.metric(
        "HbA1c Média",
        f"{hba1c_media:.2f}"
    )

with col3:

    st.metric(
        "Pacientes",
        pacientes
    )

with col4:

    st.metric(
        "Eventos",
        eventos
    )

with col5:

    st.metric(
        "Risco Crítico",
        risco_critico
    )

# =========================================================
# GRÁFICOS
# =========================================================

col1, col2 = st.columns(2)

# =========================================================
# HISTOGRAMA
# =========================================================

with col1:

    st.subheader("Distribuição HbA1c")

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    sns.histplot(
        df["hba1c"],
        bins=20,
        kde=True,
        ax=ax
    )

    ax.axvline(
        7,
        color="green",
        linestyle="--",
        label="Meta terapêutica"
    )

    ax.axvline(
        9,
        color="red",
        linestyle="--",
        label="Alto risco"
    )

    ax.set_xlabel("HbA1c (%)")

    ax.set_ylabel("Frequência")

    ax.legend()

    st.pyplot(fig)

# =========================================================
# PIZZA IGUAL À DASHBOARD REAL
# =========================================================

with col2:

    st.subheader("Estratificação de Risco")

    risco_counts = (
        df["risco"]
        .value_counts()
    )

    labels = risco_counts.index

    sizes = risco_counts.values

    colors = [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c"
    ]

    fig2, ax2 = plt.subplots(
        figsize=(8, 8)
    )

    ax2.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        startangle=150,
        colors=colors
    )

    st.pyplot(fig2)