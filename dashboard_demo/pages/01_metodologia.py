import streamlit as st

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Metodologia",
    page_icon="📚",
    layout="wide"
)

# ============================================================
# TÍTULO
# ============================================================

st.title("📚 Metodologia")

st.markdown("""
Esta página apresenta os fundamentos metodológicos utilizados para
identificação da inércia terapêutica em pacientes com Diabetes Mellitus tipo 2
(DM2) acompanhados na Atenção Primária à Saúde (APS).
""")

st.markdown("---")

# ============================================================
# OBJETIVO
# ============================================================

st.header("🎯 Objetivo")

st.markdown("""
Avaliar a ocorrência de inércia terapêutica no manejo do Diabetes Mellitus tipo 2
em pacientes acompanhados na Atenção Primária à Saúde por meio da construção
de uma coorte longitudinal baseada em dados do e-SUS APS e do desenvolvimento
de uma plataforma interativa de vigilância clínica.
""")

# ============================================================
# DEFINIÇÃO DE INÉRCIA TERAPÊUTICA
# ============================================================

st.header("📌 Definição Operacional de Inércia Terapêutica")

st.info("""
Foi considerada inércia terapêutica a ausência de intensificação
farmacoterapêutica em até 180 dias após registro de HbA1c ≥ 8%.
""")

# ============================================================
# DESENHO DO ESTUDO
# ============================================================

st.header("🧪 Desenho do Estudo")

st.markdown("""
- Estudo observacional analítico
- Coorte longitudinal retrospectiva
- Dados secundários provenientes do e-SUS APS
- Município de Vitória da Conquista – BA
- Período analisado: 2020–2025
""")

# ============================================================
# VARIÁVEIS UTILIZADAS
# ============================================================

st.header("📊 Variáveis Utilizadas")

st.table(
    {
        "Variável": [
            "Sexo",
            "Idade",
            "Faixa etária",
            "HbA1c",
            "Estratificação HbA1c",
            "Classificação terapêutica",
            "Intensificação terapêutica",
            "Inércia terapêutica"
        ],
        "Descrição": [
            "Sexo biológico",
            "Idade em anos",
            "Estratos etários",
            "Hemoglobina glicada",
            "Classificação dos níveis glicêmicos",
            "Complexidade farmacoterapêutica",
            "Mudança para esquema mais complexo",
            "Desfecho principal do estudo"
        ]
    }
)

# ============================================================
# FLUXO DE VIGILÂNCIA CLÍNICA
# ============================================================

st.header("🔄 Fluxo de Vigilância Clínica")

st.markdown("""
```text
Extração de dados do e-SUS APS
            ↓
Limpeza e padronização
            ↓
Construção da coorte longitudinal
            ↓
Identificação de HbA1c ≥ 8%
            ↓
Avaliação da farmacoterapia
            ↓
Identificação da intensificação terapêutica
            ↓
Classificação de inércia terapêutica
            ↓
Estratificação de risco clínico
            ↓
Monitoramento em dashboard
""")

# ============================================================
# PIPELINE ANALÍTICA
# ============================================================

st.header("⚙️ Pipeline Analítica")

st.markdown("""
A plataforma foi construída utilizando:

PostgreSQL
DuckDB
Python
Pandas
NumPy
SciPy
Statsmodels
Streamlit

A integração PostgreSQL → DuckDB → Dashboard permite
processamento reproduzível e monitoramento clínico longitudinal.
""")

# ============================================================
# CLASSIFICAÇÃO TERAPÊUTICA
# ============================================================

st.header("💊 Classificação Terapêutica")

st.markdown("""
Os esquemas farmacoterapêuticos foram classificados em:

Monoterapia
Dupla terapia
Terapia intensiva (≥ 3 medicamentos)
Insulinoterapia

Trocas entre medicamentos da mesma complexidade terapêutica
não foram consideradas intensificação.
""")

# ============================================================
# LIMITAÇÕES
# ============================================================

st.header("⚠️ Limitações do Modelo")

st.warning("""
• Utilização de dados secundários.

• Dependência da qualidade dos registros clínicos.

• Possibilidade de subnotificação.

• Ausência de informações sobre adesão terapêutica.

• Ausência de informações sobre motivos clínicos para não intensificação.

• Possível heterogeneidade entre equipes de saúde.

• A ferramenta não substitui julgamento clínico profissional.
""")

# ============================================================
# APLICAÇÃO PRÁTICA
# ============================================================

st.header("🏥 Aplicação Prática")

st.success("""
A plataforma foi desenvolvida para apoiar a vigilância clínica,
priorização de pacientes e tomada de decisão baseada em dados
na Atenção Primária à Saúde.
""")

# ============================================================
# RODAPÉ
# ============================================================

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.caption("🎓 Universidade Federal da Bahia")

with col2:
    st.caption("💊 Curso de Farmácia")

with col3:
    st.caption("📊 Versão 1.0")

st.caption("""
Sistema de Vigilância Clínica da Inércia Terapêutica em Diabetes Mellitus Tipo 2.

Amanda Menezes dos Santos

Orientação: Prof. Dr. Sóstenes Mistro.
""")