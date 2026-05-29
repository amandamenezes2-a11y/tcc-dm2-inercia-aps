import streamlit as st

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Sobre o Projeto",
    page_icon="📖",
    layout="wide"
)

# ============================================================
# TÍTULO
# ============================================================

st.title("📖 Sobre o Projeto")

st.markdown("""
# Vigilância Clínica da Inércia Terapêutica em Diabetes Mellitus Tipo 2 na Atenção Primária à Saúde
""")

st.markdown("""
Projeto desenvolvido como Trabalho de Conclusão de Curso (TCC) do Curso de Farmácia
da Universidade Federal da Bahia (UFBA).
""")

st.markdown("---")

# ============================================================
# CONTEXTO
# ============================================================

st.header("🌎 Contexto")

st.markdown("""
O Diabetes Mellitus tipo 2 (DM2) representa um importante problema de saúde pública,
associado a elevadas taxas de morbimortalidade e ao desenvolvimento de complicações
microvasculares e macrovasculares.

Apesar da disponibilidade de diferentes opções terapêuticas, muitos indivíduos
permanecem fora das metas glicêmicas recomendadas.

Entre os principais obstáculos para o controle adequado da doença destaca-se a
**inércia terapêutica**, caracterizada pela ausência de início ou intensificação
oportuna do tratamento diante de metas terapêuticas não atingidas.
""")

# ============================================================
# OBJETIVO
# ============================================================

st.header("🎯 Objetivo")

st.markdown("""
Desenvolver uma plataforma interativa de vigilância clínica capaz de identificar
possíveis situações de inércia terapêutica em indivíduos com Diabetes Mellitus tipo 2
acompanhados na Atenção Primária à Saúde, utilizando dados provenientes do e-SUS APS.
""")

# ============================================================
# PRINCIPAIS RESULTADOS
# ============================================================

st.header("📊 Recursos Demonstrados")

col1, col2 = st.columns(2)

with col1:
    st.success("Identificação de pacientes prioritários")

    st.success("Estratificação de risco clínico")

with col2:
    st.success("Monitoramento longitudinal")

    st.success("Exportação CSV e Excel")

st.info(
    """
    Esta versão utiliza dados demonstrativos para apresentação
    das funcionalidades da plataforma.
    """
)

# ============================================================
# TECNOLOGIAS
# ============================================================

st.header("⚙️ Tecnologias Utilizadas")

st.markdown("""
- Python
- Streamlit
- PostgreSQL
- DuckDB
- Pandas
- NumPy
- Statsmodels
- Matplotlib
- OpenPyXL
""")

# ============================================================
# FUNCIONALIDADES
# ============================================================

st.header("🖥️ Funcionalidades da Plataforma")

st.markdown("""
✅ Identificação de pacientes prioritários

✅ Monitoramento clínico longitudinal

✅ Visualização de indicadores epidemiológicos

✅ Identificação de possíveis casos de inércia terapêutica

✅ Estratificação de risco clínico

✅ Exportação de dados em CSV e Excel

✅ Dashboard interativo para apoio à tomada de decisão
""")

# ============================================================
# IMPACTO
# ============================================================

st.header("🏥 Aplicação Prática")

st.success("""
A plataforma foi desenvolvida para apoiar profissionais de saúde,
gestores e equipes da Atenção Primária na identificação de pacientes
prioritários e no monitoramento de indicadores clínicos relacionados
ao Diabetes Mellitus tipo 2.
""")

# ============================================================
# AUTORIA
# ============================================================

st.header("👩‍🎓 Autoria")

st.markdown("""
**Amanda Menezes dos Santos**

Graduanda em Farmácia — Universidade Federal da Bahia (UFBA)

**Orientador:** Prof. Dr. Sóstenes Mistro
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

Desenvolvido para fins acadêmicos e de pesquisa.
""")