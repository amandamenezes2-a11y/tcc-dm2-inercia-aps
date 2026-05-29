import streamlit as st
import duckdb
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Série Temporal",
    layout="wide"
)

st.title("📈 Monitoramento Longitudinal")
st.markdown("---")

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
# CRIA DATA FAKE (SE NÃO EXISTIR)
# ============================================================

if "data_evento" not in df.columns:

    df["data_evento"] = pd.date_range(
        start="2024-01-01",
        periods=len(df),
        freq="D"
    )

# ============================================================
# CONVERSÃO DE DATA
# ============================================================

df["data_evento"] = pd.to_datetime(
    df["data_evento"]
)

# ============================================================
# SÉRIE TEMPORAL MENSAL
# ============================================================

serie = (
    df
    .groupby(
        pd.Grouper(
            key="data_evento",
            freq="ME"
        )
    )["inercia_terapeutica"]
    .mean()
    .reset_index()
)

serie["inercia_terapeutica"] = (
    serie["inercia_terapeutica"] * 100
)

# ============================================================
# KPIs
# ============================================================

col1, col2 = st.columns(2)

col1.metric(
    "Prevalência Média",
    f"{serie['inercia_terapeutica'].mean():.1f}%"
)

col2.metric(
    "Meses Monitorados",
    len(serie)
)

st.markdown("---")

# ============================================================
# GRÁFICO
# ============================================================

st.subheader(
    "Prevalência de Inércia Terapêutica ao Longo do Tempo"
)

fig, ax = plt.subplots(figsize=(12,5))

ax.plot(
    serie["data_evento"],
    serie["inercia_terapeutica"],
    linewidth=3
)

ax.set_ylabel("Prevalência (%)")
ax.set_xlabel("Tempo")

ax.grid(True)

st.pyplot(fig)

# ============================================================
# TABELA
# ============================================================

st.subheader("Tabela Temporal")

st.dataframe(
    serie,
    width="stretch"
)

# ============================================================
# FUNÇÃO EXCEL
# ============================================================

from io import BytesIO

def gerar_excel(df):

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="SerieTemporal"
        )

    return output.getvalue()

# ============================================================
# DOWNLOAD
# ============================================================

excel = gerar_excel(serie)

csv = serie.to_csv(index=False)

st.download_button(
    "📥 Download CSV",
    csv,
    "serie_temporal.csv",
    "text/csv"
)

st.download_button(
    "📊 Download Excel",
    excel,
    "serie_temporal.xlsx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# ============================================================
# FINAL
# ============================================================

st.success("Monitoramento longitudinal carregado com sucesso!")