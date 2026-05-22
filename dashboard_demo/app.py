import streamlit as st
import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Vigilância DM2 APS",
    layout="wide"
)

st.title("📊 Vigilância Clínica DM2 - APS")
st.markdown("---")

# ============================================================
# MODO DEMO
# ============================================================

MODO_DEMO = True

# ============================================================
# CARREGAMENTO DOS DADOS
# ============================================================

if MODO_DEMO:

    df = pd.read_csv(
        "data/demo/coorte_demo.csv"
    )

    # cria coluna fake para manter dashboard
    df["co_prontuario"] = range(1, len(df) + 1)

else:

    conn = duckdb.connect(
        "data/duckdb/inercia_aps.duckdb"
    )

    df = conn.execute("""

    SELECT *
    FROM tb_inercia_dm2

    """).fetchdf()

# ============================================================
# INDICADORES PRINCIPAIS
# ============================================================

prevalencia = (
    df["inercia_terapeutica"]
    .mean()
    * 100
)

hba1c_media = df["hba1c"].mean()

total_pacientes = df["co_prontuario"].nunique()

total_eventos = len(df)

# ============================================================
# MÉTRICAS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Prevalência de Inércia",
    f"{prevalencia:.2f}%"
)

col2.metric(
    "HbA1c Média",
    f"{hba1c_media:.2f}"
)

col3.metric(
    "Pacientes",
    total_pacientes
)

col4.metric(
    "Eventos",
    total_eventos
)

st.markdown("---")

# ============================================================
# DISTRIBUIÇÃO HbA1c
# ============================================================

st.subheader("Distribuição HbA1c")

fig, ax = plt.subplots(figsize=(10, 5))

# remove valores absurdos
df_plot = df[
    (df["hba1c"] >= 4) &
    (df["hba1c"] <= 20)
]

sns.histplot(
    data=df_plot,
    x="hba1c",
    bins=20,
    kde=True,
    ax=ax
)

# linha meta terapêutica
ax.axvline(
    7,
    color="green",
    linestyle="--",
    linewidth=2,
    label="Meta terapêutica"
)

# linha alto risco
ax.axvline(
    9,
    color="red",
    linestyle="--",
    linewidth=2,
    label="Alto risco"
)

ax.set_xlabel("HbA1c (%)")
ax.set_ylabel("Frequência")
ax.set_title("Distribuição de HbA1c")
ax.legend()

st.pyplot(fig)

# ============================================================
# INÉRCIA TERAPÊUTICA
# ============================================================

st.subheader("Inércia Terapêutica")

contagem = (
    df["inercia_terapeutica"]
    .value_counts()
)

fig2, ax2 = plt.subplots()

ax2.pie(
    contagem,
    labels=["Sem Inércia", "Inércia"],
    autopct="%1.1f%%"
)

st.pyplot(fig2)

# ============================================================
# PACIENTES PRIORITÁRIOS
# ============================================================

st.subheader("Pacientes Prioritários")

criticos = df[
    (df["hba1c"] >= 10)
    &
    (df["inercia_terapeutica"] == 1)
]

st.dataframe(
    criticos.head(50)
)

# ============================================================
# TABELA ANALÍTICA
# ============================================================

st.subheader("Tabela Analítica")

st.dataframe(
    df.head(100)
)

# ============================================================
# FINAL
# ============================================================

st.success("Dashboard carregado com sucesso!")