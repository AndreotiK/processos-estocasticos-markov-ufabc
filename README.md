# Processos Estocásticos, Cadeias de Markov e Sistemas de Interação

Projeto de Iniciação Científica — UFABC, período 2026-2027.

Estudo teórico e simulação computacional de processos estocásticos, com ênfase
em cadeias de Markov discretas e modelos de interação, utilizando Python.

## Status atual

Em desenvolvimento. Implementações concluídas:

- Simulação de uma moeda justa (lançamentos ±1).
- Cálculo da média acumulada dos lançamentos.
- API backend (FastAPI) que recebe parâmetros e devolve um gráfico em Base64.

## Estrutura do repositório

    src/markov_systems/   Código-fonte do projeto (pacote Python)
    backend/              API FastAPI (servidor web)
    scripts/              Scripts executáveis
    tests/                Testes unitários (a implementar)
    results/figures/      Figuras geradas pelas simulações
    data/raw/             Dados brutos (não versionados)

## Requisitos

- Python 3.10+
- NumPy
- Matplotlib
- FastAPI
- Uvicorn

Instalação das dependências:

    pip install numpy matplotlib fastapi uvicorn

## Como executar

### 1. Módulo de simulação (terminal)
Da raiz do repositório, execute as verificações internas do pacote:

    python src/markov_systems/simulation.py

### 2. API Backend (servidor)
Da raiz do repositório, inicie o servidor FastAPI:

    uvicorn backend.main:app --reload

O servidor estará disponível em `http://localhost:8000`.
A documentação interativa da API pode ser acessada em `http://localhost:8000/docs`.

## Autor

- Gustavo Ferreira Andreoti Lima — Bacharelando em Matemática (UFABC)
- Ioannis Papageorgiou — orientador

## Licença

A definir.