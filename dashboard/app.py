import streamlit as st
import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Vigilância Clínica DM2",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("📌 Vigilância Clínica APS")

st.sidebar.markdown("""
Sistema de monitoramento longitudinal
de inércia terapêutica em Diabetes Mellitus tipo 2.
""")

st.sidebar.markdown("---")

# ============================================================
# CONEXÃO DUCKDB
# ============================================================

conn = duckdb.connect(
    "data/duckdb/inercia_aps.duckdb",
    read_only=True
)

# ============================================================
# CARREGAMENTO DOS DADOS
# ============================================================

df = conn.execute("""

SELECT *
FROM tb_inercia_dm2

""").fetchdf()

# ============================================================
# FILTRO SEXO (SE EXISTIR)
# ============================================================

if "sexo" in df.columns:

    sexo_filtro = st.sidebar.multiselect(
        "Sexo",
        df["sexo"].dropna().unique(),
        default=df["sexo"].dropna().unique()
    )

    df = df[
        df["sexo"].isin(sexo_filtro)
    ]

# ============================================================
# FILTRO HBA1C
# ============================================================

hba1c_min = st.sidebar.slider(
    "HbA1c mínima",
    4.0,
    20.0,
    7.0
)

df = df[
    df["hba1c"] >= hba1c_min
]

# ============================================================
# CLASSIFICAÇÃO DE RISCO
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
# TÍTULO
# ============================================================

st.title("📊 Vigilância Clínica DM2 - APS")

st.markdown("""
Dashboard operacional para monitoramento longitudinal
de indivíduos com Diabetes Mellitus tipo 2.
""")

st.markdown("---")

# ============================================================
# KPIs
# ============================================================

prevalencia = (
    df["inercia_terapeutica"]
    .mean()
    * 100
)

hba1c_media = df["hba1c"].mean()

if "co_prontuario" in df.columns:
    pacientes = df["co_prontuario"].nunique()
else:
    pacientes = len(df)

eventos = len(df)

criticos = len(
    df[df["risco_clinico"] == "Crítico"]
)

# ============================================================
# CARDS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Prevalência",
    f"{prevalencia:.1f}%"
)

col2.metric(
    "HbA1c Média",
    f"{hba1c_media:.2f}"
)

col3.metric(
    "Pacientes",
    pacientes
)

col4.metric(
    "Eventos",
    eventos
)

col5.metric(
    "Risco Crítico",
    criticos
)

st.markdown("---")

# ============================================================
# GRÁFICOS
# ============================================================

col_graf1, col_graf2 = st.columns(2)

# ============================================================
# HISTOGRAMA HBA1C
# ============================================================

with col_graf1:

    st.subheader("Distribuição HbA1c")

    fig, ax = plt.subplots(figsize=(8,5))

    sns.histplot(
        data=df,
        x="hba1c",
        bins=20,
        kde=True,
        ax=ax
    )

    ax.axvline(
        7,
        color="green",
        linestyle="--",
        linewidth=2,
        label="Meta terapêutica"
    )

    ax.axvline(
        9,
        color="red",
        linestyle="--",
        linewidth=2,
        label="Alto risco"
    )

    ax.set_xlabel("HbA1c (%)")
    ax.set_ylabel("Frequência")

    ax.legend()

    st.pyplot(fig)

# ============================================================
# GRÁFICO DE RISCO
# ============================================================

with col_graf2:

    st.subheader("Estratificação de Risco")

    risco = (
        df["risco_clinico"]
        .value_counts()
    )

    fig2, ax2 = plt.subplots(figsize=(6,6))

    ax2.pie(
        risco,
        labels=risco.index,
        autopct="%1.1f%%"
    )

    st.pyplot(fig2)

st.markdown("---")

# ============================================================
# PACIENTES PRIORITÁRIOS
# ============================================================

st.subheader("🚨 Pacientes Prioritários")

prioritarios = df[
    (df["hba1c"] >= 10)
    &
    (df["inercia_terapeutica"] == True)
]

st.dataframe(
    prioritarios,
    use_container_width=True
)

# ============================================================
# DOWNLOAD
# ============================================================

csv = prioritarios.to_csv(index=False)

st.download_button(
    "📥 Download CSV",
    csv,
    "pacientes_prioritarios.csv",
    "text/csv"
)

# ============================================================
# FINAL
# ============================================================

st.markdown("---")

st.success("Sistema operacional carregado com sucesso!")