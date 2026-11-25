import sys
import os
import io
import base64

# Adiciona a raiz do projeto ao caminho de busca do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.schemas import SimulacaoRequest, SimulacaoResponse
from src.markov_systems.simulation import (
    gerar_lancamentos,
    calcular_media_acumulada,
    calcular_soma_acumulada,
)

app = FastAPI(title="Simulador Markov - IC UFABC")

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def fig_to_base64(fig: plt.Figure) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


@app.get("/")
def read_root():
    return {"status": "Backend online", "projeto": "Processos Estocásticos"}


@app.post("/simular", response_model=SimulacaoResponse)
def simular_e_plotar(params: SimulacaoRequest):
    lancamentos = gerar_lancamentos(n=params.n, seed=params.seed, p_cara=params.p_cara)
    medias = calcular_media_acumulada(lancamentos)
    somas = calcular_soma_acumulada(lancamentos)

    eixo_t = np.arange(1, params.n + 1)
    valor_esperado = (2 * params.p_cara) - 1  # E[X_i] = 2p - 1

    # ------------------------------------------------------------------
    # GRÁFICO 1: Lei Forte dos Grandes Números (Média Acumulada M_t)
    # ------------------------------------------------------------------
    fig_media, ax_media = plt.subplots(figsize=(10, 4.5))
    ax_media.plot(eixo_t, medias, color="navy", lw=1.2, label=r"Média Amostral ($M_t$)")
    ax_media.axhline(
        valor_esperado,
        color="crimson",
        linestyle="--",
        lw=1.3,
        label=rf"Esperança Matemática ($\mathbb{{E}}[X] = {valor_esperado:.2f}$)",
    )
    ax_media.axhline(0, color="gray", linestyle=":", lw=1.0, label="Origem ($0$)")

    ax_media.set_ylim(-1.1, 1.1)
    ax_media.set_xlabel("Número de Lançamentos ($t$)")
    ax_media.set_ylabel(r"Média Acumulada ($M_t$)")
    ax_media.set_title(
        f"Lei Forte dos Grandes Números: Convergência da Média Amostral\n"
        f"(n = {params.n}, seed = {params.seed}, p = {params.p_cara:.2f})"
    )
    ax_media.legend(loc="best")
    ax_media.grid(alpha=0.3)

    grafico_media_b64 = fig_to_base64(fig_media)

    # ------------------------------------------------------------------
    # GRÁFICO 2: Passeio Aleatório Unidimensional (Soma Acumulada S_t)
    # ------------------------------------------------------------------
    fig_passeio, ax_passeio = plt.subplots(figsize=(10, 4.5))

    deriva_esperada = eixo_t * valor_esperado  # E[S_t] = t * (2p - 1)

    ax_passeio.plot(eixo_t, somas, color="darkgreen", lw=1.2, label=r"Trajetória do Passeio ($S_t$)")
    ax_passeio.plot(
        eixo_t,
        deriva_esperada,
        color="crimson",
        linestyle="--",
        lw=1.3,
        label=rf"Deriva Esperada ($\mathbb{{E}}[S_t] = {valor_esperado:.2f}t$)",
    )

    if params.mostrar_desvio_padrao:
        # Var(X_i) = 4 * p * (1 - p)  =>  DP(S_t) = 2 * sqrt(t * p * (1 - p))
        dp_somas = 2.0 * np.sqrt(eixo_t * params.p_cara * (1.0 - params.p_cara))
        ax_passeio.fill_between(
            eixo_t,
            deriva_esperada - dp_somas,
            deriva_esperada + dp_somas,
            color="crimson",
            alpha=0.14,
            label=r"Faixa de $\pm 1$ Desvio Padrão ($\mathbb{E}[S_t] \pm \sigma_{S_t}$)",
        )

    ax_passeio.axhline(0, color="gray", linestyle=":", lw=1.0, label="Origem ($0$)")
    ax_passeio.set_xlabel("Número de Passos / Lançamentos ($t$)")
    ax_passeio.set_ylabel(r"Posição Acumulada ($S_t$)")
    ax_passeio.set_title(
        f"Passeio Aleatório Unidimensional com Deriva (Soma Acumulada)\n"
        f"(n = {params.n}, seed = {params.seed}, p = {params.p_cara:.2f})"
    )
    ax_passeio.legend(loc="best")
    ax_passeio.grid(alpha=0.3)

    grafico_passeio_b64 = fig_to_base64(fig_passeio)

    return SimulacaoResponse(
        grafico_media_base64=grafico_media_b64,
        grafico_passeio_base64=grafico_passeio_b64,
    )