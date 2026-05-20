# Vigilância Clínica DM2 - APS

Pipeline analítico para avaliação de inércia terapêutica em pacientes com Diabetes Mellitus tipo 2 utilizando dados do e-SUS APS.

---

# Objetivo

Avaliar a prevalência de inércia terapêutica em pacientes com DM2 e HbA1c alterada na Atenção Primária à Saúde.

---

# Definição Operacional

Foi considerada inércia terapêutica:

> ausência de intensificação farmacológica em até 180 dias após HbA1c ≥8%.

Intensificação foi definida como:
- introdução de nova classe farmacológica antidiabética;
- aumento do número de classes terapêuticas.

---

# Fonte de Dados

- e-SUS APS
- PostgreSQL
- tabelas clínicas e laboratoriais

---

# Estrutura do Projeto

```text
TCC_DM2_INERCIA/

│
├── core/
│   └── database.py
│
├── scripts/
│
│   ├── analytics/
│   │
│   │   ├── 03_coorte_longitudinal.py
│   │   ├── 04_motor_inercia.py
│   │   ├── 05_enriquecimento_coorte.py
│
│   └── analysis/
│       │
│       ├── 20_regressao_logistica.py
│       ├── 21_forest_plot_publicacao.py
│       ├── 31_tabela1.py
│       ├── 32_inercia_por_hba1c.py
│       └── 33_fluxograma_coorte.py
│
├── dashboard/
│   ├── app.py
│   └── pages/
│
├── data/
│   ├── duckdb/
│   └── results/
│
├── docs/
│   └── figuras/
│
└── README.md
```

---

# Pipeline Analítico

## 1. Construção longitudinal

```bash
python -m scripts.analytics.03_coorte_longitudinal
```

## 2. Motor de inércia terapêutica

```bash
python -m scripts.analytics.04_motor_inercia
```

## 3. Enriquecimento demográfico

```bash
python -m scripts.analytics.05_enriquecimento_coorte
```

## 4. Regressão logística

```bash
python -m scripts.analysis.20_regressao_logistica
```

## 5. Tabela descritiva

```bash
python -m scripts.analysis.31_tabela1
```

## 6. Prevalência por HbA1c

```bash
python -m scripts.analysis.32_inercia_por_hba1c
```

## 7. Fluxograma da coorte

```bash
python -m scripts.analysis.33_fluxograma_coorte
```

---

# Dashboard

Executar:

```bash
streamlit run dashboard/app.py
```

---

# Principais Resultados

- Coorte final: 3500 eventos
- HbA1c média: 9,9%
- Inércia terapêutica: 66,4%
- HbA1c ≥10%: 41,4%

Regressão logística:
- HbA1c mais elevado associou-se à menor chance de inércia terapêutica.

---

# Tecnologias Utilizadas

- Python
- Pandas
- DuckDB
- PostgreSQL
- Statsmodels
- Streamlit
- Matplotlib

---

# Autora

Amanda Menezes dos Santos  
Graduação em Farmácia – UFBA

---

# Orientação

Prof. Sóstenes Mistro