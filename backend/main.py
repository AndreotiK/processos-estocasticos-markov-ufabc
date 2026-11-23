from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

from src.markov_systems.simulation import gerar_lancamentos, calcular_media_acumulada

app = FastAPI(title="Simulador Markov - IC UFABC")

import sys
import os

# Adiciona a raiz do projeto ao caminho de busca do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

class SimulacaoRequest(BaseModel):
    n: int
    seed: int | None = None
    p_cara: float = 0.5 # NOVO: Probabilidade de cara (default 50%)

@app.get("/")
def read_root():
    return {"status": "Backend online", "projeto": "Processos Estocásticos"}

@app.post("/simular")
def simular_e_plotar(params: SimulacaoRequest):
    # 1. Executa a lógica científica
    # NOTA: Passe o p_cara para a sua função. 
    # (Se a sua função não aceitar esse argumento ainda, veja o Passo 3 abaixo)
    lancamentos = gerar_lancamentos(n=params.n, seed=params.seed, p_cara=params.p_cara)
    medias = calcular_media_acumulada(lancamentos)
    
    # 2. Gera o gráfico
    fig, ax = plt.subplots(figsize=(10, 5))
    eixo_x = np.arange(1, len(medias) + 1)
    
    ax.plot(eixo_x, medias, color="navy", lw=1.2, label="Média Acumulada")
    
    # NOVO: Calcula o Valor Esperado (Esperança) da moeda viciada
    # Se Cara = +1 e Coroa = -1: E(X) = 1*p_cara + (-1)*(1 - p_cara) = 2*p_cara - 1
    valor_esperado = (2 * params.p_cara) - 1
    
    ax.axhline(valor_esperado, color="red", linestyle="--", label=f"Esperança ({valor_esperado:.2f})")
    
    # Mantém a linha do zero apenas como referência visual
    ax.axhline(0, color="gray", linestyle=":", label="Zero")
    
    ax.set_ylim(-1.1, 1.1)
    
    ax.set_xlabel("Número de Lançamentos")
    ax.set_ylabel("Média (Cara=+1, Coroa=-1)")
    ax.set_title(f"Simulação (n={params.n}, seed={params.seed}, P(Cara)={params.p_cara*100:.0f}%)")
    ax.legend()
    ax.grid(alpha=0.3)
    
    # 3. Salva a imagem
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close(fig) 
    
    # 4. Codifica
    imagem_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    
    # 5. Retorna
    return {"imagem_base64": imagem_base64}