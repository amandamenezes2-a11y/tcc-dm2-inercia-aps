import streamlit as st
import duckdb
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Predição Clínica",
    layout="wide"
)

st.title("🧠 Predição de Inércia Terapêutica")
st.markdown("---")

# ============================================================
# DUCKDB
# ============================================================

conn = duckdb.connect(
    "data/duckdb/inercia_aps.duckdb",
    read_only=True
)

# ============================================================
# DADOS
# ============================================================

df = conn.execute("""

SELECT *
FROM tb_inercia_dm2

""").fetchdf()

# ============================================================
# FEATURES DINÂMICAS
# ============================================================

features = []

if "idade" in df.columns:
    features.append("idade")

if "hba1c" in df.columns:
    features.append("hba1c")

if "n_classes_pre" in df.columns:
    features.append("n_classes_pre")

target = "inercia_terapeutica"

# ============================================================
# BASE
# ============================================================

base = df[
    features + [target]
].dropna()

X = base[features]

y = base[target]

# ============================================================
# TREINO
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

modelo = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

modelo.fit(
    X_train,
    y_train
)

# ============================================================
# MÉTRICA
# ============================================================

pred = modelo.predict(X_test)

acc = accuracy_score(
    y_test,
    pred
)

st.metric(
    "Acurácia do Modelo",
    f"{acc:.2f}"
)

st.markdown("---")

# ============================================================
# IMPORTÂNCIA
# ============================================================

st.subheader("Importância das Variáveis")

importancia = pd.DataFrame({

    "Variável": features,

    "Importância": modelo.feature_importances_

})

importancia = importancia.sort_values(
    "Importância",
    ascending=False
)

st.dataframe(
    importancia,
    width="stretch"
)

# ============================================================
# SIMULAÇÃO
# ============================================================

st.subheader("Simulação Clínica")

entrada = {}

# ============================================================
# IDADE
# ============================================================

if "idade" in features:

    idade = st.slider(
        "Idade",
        18,
        100,
        60
    )

    entrada["idade"] = idade

# ============================================================
# HBA1C
# ============================================================

if "hba1c" in features:

    hba1c = st.slider(
        "HbA1c",
        5.0,
        15.0,
        9.0
    )

    entrada["hba1c"] = hba1c

# ============================================================
# CLASSES
# ============================================================

if "n_classes_pre" in features:

    classes = st.slider(
        "Número de Classes Terapêuticas",
        1,
        5,
        2
    )

    entrada["n_classes_pre"] = classes

# ============================================================
# DATAFRAME
# ============================================================

entrada_df = pd.DataFrame(
    [entrada]
)

# ============================================================
# PROBABILIDADE
# ============================================================

prob = modelo.predict_proba(
    entrada_df
)[0][1]

# ============================================================
# RESULTADO
# ============================================================

st.markdown("---")

if prob >= 0.7:

    st.error(
        f"🔴 Alto risco de inércia terapêutica ({prob:.1%})"
    )

elif prob >= 0.4:

    st.warning(
        f"🟠 Risco moderado ({prob:.1%})"
    )

else:

    st.success(
        f"🟢 Baixo risco ({prob:.1%})"
    )

# ============================================================
# FINAL
# ============================================================

st.success(
    "Modelo preditivo carregado com sucesso!"
)