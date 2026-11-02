# Processos Estocásticos, Cadeias de Markov e Sistemas de Interação

Projeto de Iniciação Científica — UFABC, período 2026-2027.

Estudo teórico e simulação computacional de processos estocásticos, com ênfase
em cadeias de Markov discretas e modelos de interação, utilizando Python.

## 🎥 Demonstração do Protótipo

Assista à apresentação do primeiro protótipo funcional do projeto, que integra a simulação matemática em Python a uma interface web interativa:

[![Apresentação do Protótipo](https://img.youtube.com/vi/rHRq8N19W5s/0.jpg)](https://www.youtube.com/watch?v=rHRq8N19W5s&list=PLbfcrKHH15Nk)

## Status atual

Em desenvolvimento. Etapas concluídas:

- Simulação de uma moeda justa (lançamentos ±1) e cálculo da média acumulada.
- API backend (FastAPI) que recebe parâmetros (n e seed) e devolve o gráfico em Base64.
- Frontend interativo (React) para entrada de dados e exibição do gráfico em tempo real.
- Apresentação do primeiro protótipo ao orientador.

## Estrutura do repositório

    src/markov_systems/   Código-fonte do projeto (pacote Python)
    backend/              API FastAPI (servidor web)
    frontend/             Interface de usuário (React + Vite)
    scripts/              Scripts executáveis
    tests/                Testes unitários (a implementar)
    results/figures/      Figuras geradas pelas simulações
    data/raw/             Dados brutos (não versionados)

## Requisitos

**Backend e Simulação:**
- Python 3.10+
- NumPy
- Matplotlib
- FastAPI
- Uvicorn

**Frontend:**
- Node.js (versão LTS recomendada)
- npm (geralmente instalado junto com o Node.js)

Instalação das dependências do Python (na raiz do repositório, com o ambiente virtual ativado):

    pip install numpy matplotlib fastapi uvicorn

## Como executar

Para rodar a aplicação completa (backend + frontend), você precisará de **dois terminais**.

### 1. Módulo de simulação (opcional, via terminal)
Para rodar apenas as verificações internas da lógica matemática:

    python src/markov_systems/simulation.py

### 2. Iniciar a API Backend (Terminal 1)
Na raiz do repositório, inicie o servidor FastAPI:

    uvicorn backend.main:app --reload

O servidor estará disponível em `http://localhost:8000`.
A documentação interativa da API pode ser acessada em `http://localhost:8000/docs`.

### 3. Iniciar a Interface Frontend (Terminal 2)
Em um segundo terminal, navegue até a pasta do frontend, instale as dependências (apenas na primeira vez) e inicie o servidor:

    cd frontend
    npm install
    npm run dev

A interface estará disponível no endereço indicado no terminal (geralmente `http://localhost:5173`).

## Autor

- Gustavo Ferreira Andreoti Lima — Bacharelando em Matemática (UFABC)
- Ioannis Papageorgiou — orientador

## Licença

A definir.