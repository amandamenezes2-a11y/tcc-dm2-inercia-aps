import streamlit as st
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

st.sidebar.title("📌 Vigilância DM2 APS")

st.sidebar.markdown("""
Dashboard demonstrativa para vigilância clínica
de inércia terapêutica em Diabetes Mellitus tipo 2
na Atenção Primária à Saúde.
""")

st.sidebar.markdown("---")

sexo_filtro = st.sidebar.multiselect(
    "Sexo",
    ["Masculino", "Feminino"],
    default=["Masculino", "Feminino"]
)

hba1c_min = st.sidebar.slider(
    "HbA1c mínima",
    4.0,
    15.0,
    7.0
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Base demonstrativa anonimizada."
)

# ============================================================
# TÍTULO
# ============================================================

st.title("📊 Vigilância Clínica DM2 - APS")
st.markdown("---")

# ============================================================
# BASE DEMO
# ============================================================

df = pd.read_csv(
    "data/demo/coorte_demo.csv"
)

df["co_prontuario"] = range(1, len(df) + 1)

# ============================================================
# FILTROS
# ============================================================

df = df[
    (df["sexo"].isin(sexo_filtro))
    &
    (df["hba1c"] >= hba1c_min)
]

# ============================================================
# KPIs
# ============================================================

prevalencia = (
    df["inercia_terapeutica"].mean()
) * 100

hba1c_media = df["hba1c"].mean()

pacientes = df["co_prontuario"].nunique()

eventos = len(df)

# ============================================================
# CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Prevalência de Inércia",
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

st.markdown("---")

# ============================================================
# GRÁFICOS
# ============================================================

col_graf1, col_graf2 = st.columns(2)

# ============================================================
# HISTOGRAMA
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
# PIZZA
# ============================================================

with col_graf2:

    st.subheader("Inércia Terapêutica")

    contagem = (
        df["inercia_terapeutica"]
        .value_counts()
    )

    fig2, ax2 = plt.subplots(figsize=(7,7))

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
    wedgeprops={"edgecolor": "white", "linewidth": 2},
    textprops={"fontsize": 12}
)

ax2.axis("equal")

ax2.set_title(
    "Inércia Terapêutica",
    fontsize=18,
    fontweight="bold"
)

st.pyplot(fig2)

    st.pyplot(fig2)

st.markdown("---")

# ============================================================
# PACIENTES PRIORITÁRIOS
# ============================================================

st.subheader("🚨 Pacientes Prioritários")

criticos = df[
    (df["hba1c"] >= 10)
    &
    (df["inercia_terapeutica"] == 1)
]

st.dataframe(
    criticos,
    use_container_width=True
)

# ============================================================
# DOWNLOAD
# ============================================================

csv = criticos.to_csv(index=False)

st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name="pacientes_prioritarios.csv",
    mime="text/csv"
)

# ============================================================
# RODAPÉ
# ============================================================

st.markdown("---")

st.caption("""
Projeto de vigilância clínica em Diabetes Mellitus tipo 2
na Atenção Primária à Saúde.

Dashboard demonstrativa desenvolvida para fins científicos.
""")