import streamlit as st
import pandas as pd

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
    use_container_width=True
)

# ============================================================
# DOWNLOAD
# ============================================================

csv = criticos.to_csv(index=False)

st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name="pacientes_prioritarios_demo.csv",
    mime="text/csv"
)

# ============================================================
# FINAL
# ============================================================

st.success("Dashboard demo carregada com sucesso!")