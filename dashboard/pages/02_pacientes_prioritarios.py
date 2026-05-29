import streamlit as st
import duckdb
import pandas as pd
from io import BytesIO

# ============================================================
# CONEXÃO
# ============================================================

conn = duckdb.connect(
    "data/duckdb/inercia_aps.duckdb",
    read_only=True
)

# ============================================================
# CARREGANDO BASE
# ============================================================

df = conn.execute("""

SELECT *
FROM tb_inercia_dm2

""").fetchdf()

# ============================================================
# CLASSIFICAÇÃO DE RISCO
# ============================================================

def classificar_risco(row):

    if (
        row["hba1c"] >= 10
        and row["inercia_terapeutica"] == 1
    ):
        return "CRÍTICO"

    elif (
        row["hba1c"] >= 9
        and row["inercia_terapeutica"] == 1
    ):
        return "ALTO"

    elif row["hba1c"] >= 8:
        return "MODERADO"

    else:
        return "BAIXO"


df["risco"] = df.apply(classificar_risco, axis=1)

# ============================================================
# FILTRO PRIORITÁRIOS
# ============================================================

df_prioritarios = df[
    (
        (df["hba1c"] >= 9)
        |
        (df["inercia_terapeutica"] == 1)
    )
].copy()

# ============================================================
# ORDENAÇÃO
# ============================================================

df_prioritarios = df_prioritarios.sort_values(
    by="hba1c",
    ascending=False
)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("Filtros")

risco = st.sidebar.multiselect(
    "Risco",
    options=df_prioritarios["risco"].unique(),
    default=df_prioritarios["risco"].unique()
)

df_prioritarios = df_prioritarios[
    df_prioritarios["risco"].isin(risco)
]

# ============================================================
# DASHBOARD
# ============================================================

st.title("🚨 Pacientes Prioritários")
st.caption(
    "Monitoramento clínico de pacientes com provável inércia terapêutica."
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Pacientes críticos",
    len(df_prioritarios[df_prioritarios["risco"] == "CRÍTICO"])
)

col2.metric(
    "Pacientes alto risco",
    len(df_prioritarios[df_prioritarios["risco"] == "ALTO"])
)

col3.metric(
    "HbA1c média",
    round(df_prioritarios["hba1c"].mean(), 1)
)

col4.metric(
    "Sem intensificação",
    len(df_prioritarios[
        df_prioritarios["intensificou"] == 0
    ])
)

# ============================================================
# TABELA
# ============================================================

st.subheader("Lista Prioritária")

# ============================================================
# CORES
# ============================================================

def colorir_risco(val):

    if val == "CRÍTICO":
        return "background-color: #ff4b4b; color: white; font-weight: bold"

    elif val == "ALTO":
        return "background-color: #ffa600; color: black; font-weight: bold"

    elif val == "MODERADO":
        return "background-color: #ffe08a"

    else:
        return ""

# ============================================================
# TABELA
# ============================================================

st.subheader("Lista Prioritária")

tabela = df_prioritarios[
    [
        "co_prontuario",
        "hba1c",
        "n_classes_pre",
        "n_classes_pos",
        "intensificou",
        "inercia_terapeutica",
        "risco"
    ]
]

styled_table = tabela.style.map(
    colorir_risco,
    subset=["risco"]
)

st.dataframe(
    styled_table,
    width="stretch"
)

# ============================================================
# FUNÇÃO EXCEL
# ============================================================

def gerar_excel(df):

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Pacientes"
        )

    return output.getvalue()

# ============================================================
# DOWNLOAD
# ============================================================

excel = gerar_excel(df_prioritarios)

csv = df_prioritarios.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Baixar lista prioritária",
    data=csv,
    file_name="pacientes_prioritarios.csv",
    mime="text/csv"
)

st.download_button(
    label="📊 Baixar Excel",
    data=excel,
    file_name="pacientes_prioritarios.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)