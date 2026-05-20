# Sistema de Vigilância de Inércia Terapêutica na APS

Infraestrutura computacional para monitoramento longitudinal da inércia terapêutica em diabetes mellitus tipo 2 baseada em dados reais do e-SUS APS.

## Objetivo

Desenvolver pipeline automatizado para:
- extração de dados do e-SUS APS;
- construção de coorte longitudinal;
- identificação de inércia terapêutica;
- análise epidemiológica automatizada;
- monitoramento clínico em tempo real.

## Arquitetura

PostgreSQL e-SUS APS
→ ETL Python
→ DuckDB
→ Motor longitudinal
→ Regressão logística
→ Dashboard Streamlit

## Tecnologias utilizadas

- Python
- PostgreSQL
- DuckDB
- Pandas
- Statsmodels
- Streamlit
- Matplotlib

## Principais funcionalidades

- Extração automatizada do e-SUS APS
- Identificação de HbA1c alterada
- Detecção de intensificação terapêutica
- Construção de coorte longitudinal
- Regressão logística automatizada
- Dashboard interativo
- Vigilância clínica em tempo real

## Resultados principais

- 39.267 exames HbA1c analisados
- 3.551 eventos longitudinais elegíveis
- Prevalência de inércia terapêutica: 66,6%
- Modelo multivariado ajustado

## Potenciais aplicações

- Vigilância clínica APS
- Apoio matricial
- Gestão em saúde
- Monitoramento farmacoterapêutico
- Qualificação do cuidado em DM2

## Autoria

Amanda Menezes dos Santos
UFBA — Graduação em Farmácia