import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# CONFIGURAÇÕES
# ============================================================

np.random.seed(42)

N = 250

# ============================================================
# GERANDO DADOS DEMO
# ============================================================

df = pd.DataFrame({
    "idade": np.random.randint(18, 90, N),

    "sexo": np.random.choice(
        ["Feminino", "Masculino"],
        N,
        p=[0.67, 0.33]
    ),

    "hba1c": np.round(
        np.random.normal(9.9, 1.6, N),
        1
    ),

    "n_classes_pre": np.random.choice(
        [1, 2, 3],
        N,
        p=[0.4, 0.45, 0.15]
    ),

    "n_classes_pos": np.random.choice(
        [1, 2, 3, 4],
        N,
        p=[0.25, 0.40, 0.25, 0.10]
    ),

    "inercia_terapeutica": np.random.choice(
        [0, 1],
        N,
        p=[0.34, 0.66]
    )
})

# ============================================================
# AJUSTES
# ============================================================

df["hba1c"] = df["hba1c"].clip(6.5, 18)

df["intensificou"] = np.where(
    df["inercia_terapeutica"] == 1,
    0,
    1
)

# ============================================================
# SALVANDO
# ============================================================

Path("data/demo").mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    "data/demo/coorte_demo.csv",
    index=False
)

print("=" * 60)
print("BASE DEMO GERADA")
print("=" * 60)

print(df.head())

print("\nDIMENSÃO:")
print(df.shape)

print("\nARQUIVO:")
print("data/demo/coorte_demo.csv")