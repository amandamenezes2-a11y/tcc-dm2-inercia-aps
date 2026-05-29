import streamlit as st
import pandas as pd
from io import BytesIO

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Pacientes Prioritários",
    layout="wide"
)

st.title("🚨 Pacientes Prioritários")
st.markdown("---")

# ============================================================
# BASE DEMO
# ============================================================

df = pd.read_csv(
    "data/demo/coorte_demo.csv"
)

# id fake
df["co_prontuario"] = range(1, len(df) + 1)

# ============================================================
# FILTRO CLÍNICO
# ============================================================

criticos = df[
    (df["hba1c"] >= 10)
    &
    (df["inercia_terapeutica"] == 1)
]

# ============================================================
# MÉTRICAS
# ============================================================

col1, col2, col3 = st.columns(3)

col1.metric(
    "Pacientes Prioritários",
    len(criticos)
)

col2.metric(
    "HbA1c Média",
    round(
        criticos["hba1c"].mean(),
        2
    )
)

col3.metric(
    "Prevalência",
    f"{(len(criticos)/len(df))*100:.1f}%"
)

st.markdown("---")

# ============================================================
# TABELA
# ============================================================

st.subheader("Pacientes com HbA1c ≥ 10% e inércia terapêutica")

st.dataframe(
    criticos,
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

excel = gerar_excel(criticos)

csv = criticos.to_csv(index=False)

st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name="pacientes_prioritarios_demo.csv",
    mime="text/csv"
)

st.download_button(
    label="📊 Download Excel",
    data=excel,
    file_name="pacientes_prioritarios_demo.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# ============================================================
# FINAL
# ============================================================

st.success("Dashboard demo carregada com sucesso!")