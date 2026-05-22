import streamlit as st
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
# BASE DEMO
# ============================================================

df = pd.read_csv(
    "data/demo/coorte_demo.csv"
)

# ============================================================
# FEATURES
# ============================================================

features = [
    "idade",
    "hba1c",
    "n_classes_pre"
]

target = "inercia_terapeutica"

# ============================================================
# BASE MODELO
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
# ACURÁCIA
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

st.dataframe(
    importancia.sort_values(
        "Importância",
        ascending=False
    ),
    use_container_width=True
)

# ============================================================
# SIMULAÇÃO
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

entrada = pd.DataFrame({

    "idade": [idade],

    "hba1c": [hba1c],

    "n_classes_pre": [classes]

})

prob = modelo.predict_proba(
    entrada
)[0][1]

# ============================================================
# RESULTADO
# ============================================================

if prob >= 0.7:

    st.error(
        f"🔴 Alto risco ({prob:.1%})"
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
    "Modelo preditivo demo carregado."
)