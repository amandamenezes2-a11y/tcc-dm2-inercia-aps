from core.database import duck_conn

import pandas as pd
import statsmodels.api as sm
import numpy as np

print("=" * 60)
print("REGRESSÃO LOGÍSTICA MULTIVARIADA")
print("=" * 60)

# ============================================================
# CARREGANDO BASE
# ============================================================

df = duck_conn.execute("""

SELECT *
FROM tb_inercia_enriquecida

""").fetchdf()

print("\nBASE:")
print(df.shape)

print("\nCOLUNAS:")
print(df.columns)

# ============================================================
# TRATAMENTO
# ============================================================

df = df.copy()

# Variável dependente
df["desfecho"] = df["inercia_terapeutica"].astype(int)

# Sexo binário
df["sexo_masc"] = np.where(
    df["sexo"] == "Masculino",
    1,
    0
)


# ============================================================
# VARIÁVEIS DO MODELO
# ============================================================

variaveis = [
    "idade",
    "sexo_masc",
    "hba1c",
    ]

# Removendo missings
base_modelo = df[["desfecho"] + variaveis].dropna()

print("\nBASE MODELO:")
print(base_modelo.shape)

# ============================================================
# X E Y
# ============================================================

X = base_modelo[variaveis]
X = sm.add_constant(X)

y = base_modelo["desfecho"]

# ============================================================
# MODELO
# ============================================================

print("\nTREINANDO MODELO...")

modelo = sm.Logit(y, X).fit()

print(modelo.summary())

# ============================================================
# OR AJUSTADO
# ============================================================

params = modelo.params
conf = modelo.conf_int()

or_df = pd.DataFrame({
    "Variavel": params.index,
    "OR": np.exp(params.values),
    "IC95_inf": np.exp(conf[0]),
    "IC95_sup": np.exp(conf[1]),
    "p_valor": modelo.pvalues.values
})

print("\nOR AJUSTADOS")
print(or_df)

# ============================================================
# EXPORTANDO
# ============================================================

or_df.to_csv(
    "data/results/regressao_logistica.csv",
    index=False
)

print("\nARQUIVO EXPORTADO:")
print("data/results/regressao_logistica.csv")

print("\n" + "=" * 60)
print("ANÁLISE FINALIZADA")
print("=" * 60)