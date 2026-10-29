# Processos Estocásticos, Cadeias de Markov e Sistemas de Interação

Projeto de Iniciação Científica — UFABC, período 2026-2027.

Estudo teórico e simulação computacional de processos estocásticos, com ênfase
em cadeias de Markov discretas e modelos de interação, utilizando Python.

## Status atual

Em desenvolvimento. Implementação inicial concluída:

- Simulação de uma moeda justa (lançamentos ±1).
- Cálculo da média acumulada dos lançamentos.

## Estrutura do repositório

    src/markov_systems/   Código-fonte do projeto (pacote Python)
    scripts/              Scripts executáveis
    tests/                Testes unitários (a implementar)
    results/figures/      Figuras geradas pelas simulações
    data/raw/             Dados brutos (não versionados)

## Requisitos

- Python 3.10+
- NumPy

Instalação das dependências:

    pip install numpy

## Como executar

Da raiz do repositório, execute o módulo de simulação com suas verificações
internas:

    python src/markov_systems/simulation.py

## Autor

- Gustavo Ferreira Andreoti Lima — Bacharelando em Matemática (UFABC)
- Ioannis Papageorgiou — orientador

## Licença

A definir.