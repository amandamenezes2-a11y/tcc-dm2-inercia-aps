import streamlit as st
import pandas as pd
import numpy as np

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Predição Clínica",
    layout="wide"
)

st.title("🧠 Predição Clínica de Inércia Terapêutica")
st.markdown("---")

# ============================================================
# BASE DEMO
# ============================================================

df = pd.read_csv(
    "data/demo/coorte_demo.csv"
)

# ============================================================
# SCORE SIMPLIFICADO
# ============================================================

st.subheader("Simulação Clínica")

idade = st.slider(
    "Idade",
    18,
    100,
    60
)

hba1c = st.slider(
    "HbA1c",
    5.0,
    15.0,
    9.0
)

classes = st.slider(
    "Número de Classes Terapêuticas",
    1,
    5,
    2
)

# ============================================================
# SCORE CLÍNICO
# ============================================================

score = (
    (hba1c * 0.6)
    +
    (classes * 8)
    +
    (idade * 0.1)
)

# normalização
prob = min(score / 20, 1)

# ============================================================
# RESULTADO
# ============================================================

st.markdown("---")

st.metric(
    "Probabilidade Estimada",
    f"{prob:.1%}"
)

if prob >= 0.7:

    st.error(
        "🔴 Alto risco de inércia terapêutica"
    )

elif prob >= 0.4:

    st.warning(
        "🟠 Risco moderado"
    )

else:

    st.success(
        "🟢 Baixo risco"
    )

# ============================================================
# INTERPRETAÇÃO
# ============================================================

st.markdown("---")

st.subheader("Interpretação Clínica")

st.write("""
O modelo demonstrativo utiliza:
- HbA1c;
- intensidade terapêutica;
- idade;

para estimar risco clínico de inércia terapêutica.
""")

# ============================================================
# FINAL
# ============================================================

st.success(
    "Predição clínica demo carregada."
)