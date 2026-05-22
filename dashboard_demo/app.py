import streamlit as st
import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================================================
# CONFIGURAÇÃO
# =========================================================

st.set_page_config(
    page_title="Vigilância DM2 APS",
    layout="wide"
)

st.title("📊 Vigilância Clínica DM2 - APS")

st.markdown(
    """
    Dashboard demonstrativa para vigilância clínica de inércia terapêutica
    em Diabetes Mellitus tipo 2 na Atenção Primária à Saúde.
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

    # coluna fake para manter compatibilidade
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
# AJUSTES DE COLUNAS
# =========================================================

df.columns = [c.lower() for c in df.columns]

# cria sexo se não existir
if "sexo" not in df.columns:

    import numpy as np

    np.random.seed(42)

    df["sexo"] = np.random.choice(
        ["Masculino", "Feminino"],
        size=len(df)
    )

# cria coluna de inércia se não existir
if "inercia_terapeutica" not in df.columns:

    if "hba1c" in df.columns:
        df["inercia_terapeutica"] = (
            df["hba1c"] >= 8.0
        ).astype(int)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("## 📌 Vigilância DM2 APS")

st.sidebar.markdown(
    """
    Dashboard demonstrativa para vigilância clínica de inércia terapêutica
    em Diabetes Mellitus tipo 2 na Atenção Primária à Saúde.
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

st.sidebar.info("Base demonstrativa anonimizada.")

# =========================================================
# MÉTRICAS
# =========================================================

prevalencia = (
    df["inercia_terapeutica"].mean() * 100
)

hba1c_media = df["hba1c"].mean()

pacientes = len(df)

eventos = len(df)

# =========================================================
# KPIs
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Prevalência de Inércia",
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

# =========================================================
# GRÁFICOS
# =========================================================

col1, col2 = st.columns(2)

# ---------------------------------------------------------
# HISTOGRAMA
# ---------------------------------------------------------

with col1:

    st.subheader("Distribuição HbA1c")

    fig, ax = plt.subplots(figsize=(8, 5))

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

# ---------------------------------------------------------
# GRÁFICO PIZZA
# ---------------------------------------------------------

with col2:

    fig2, ax2 = plt.subplots(figsize=(7, 7))

    labels = ["Inércia", "Sem Inércia"]

    sizes = [
        df["inercia_terapeutica"].sum(),
        len(df) - df["inercia_terapeutica"].sum()
    ]

    colors = ["#1f77b4", "#ff7f0e"]

    ax2.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
        wedgeprops={
            "edgecolor": "white",
            "linewidth": 2
        },
        textprops={
            "fontsize": 12
        }
    )

    ax2.axis("equal")

    ax2.set_title(
        "Inércia Terapêutica",
        fontsize=18,
        fontweight="bold"
    )

    st.pyplot(fig2)