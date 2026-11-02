from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Importações para plotagem e manipulação de dados
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

from src.markov_systems.simulation import gerar_lancamentos, calcular_media_acumulada

app = FastAPI(title="Simulador Markov - IC UFABC")

# Configuração essencial de CORS
origins = [
    "http://localhost:3000",  # Porta padrão do React (Create React App)
    "http://localhost:5173",  # Porta padrão do Vite
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

@app.get("/")
def read_root():
    return {"status": "Backend online", "projeto": "Processos Estocásticos"}

@app.post("/simular")
def simular_e_plotar(params: SimulacaoRequest):
    # 1. Executa a lógica científica
    lancamentos = gerar_lancamentos(n=params.n, seed=params.seed)
    medias = calcular_media_acumulada(lancamentos)
    
    # 2. Gera o gráfico
    fig, ax = plt.subplots(figsize=(10, 5))
    eixo_x = np.arange(1, len(medias) + 1)
    
    ax.plot(eixo_x, medias, color="navy", lw=1.2, label="Média Acumulada")
    ax.axhline(0, color="red", linestyle="--", label="Equilíbrio (0)")
    
    # Fixando o eixo Y para visualizar o funil
    ax.set_ylim(-1.1, 1.1)
    
    ax.set_xlabel("Número de Lançamentos")
    ax.set_ylabel("Média (Cara=+1, Coroa=-1)")
    ax.set_title(f"Simulação da Moeda (n={params.n}, seed={params.seed})")
    ax.legend()
    ax.grid(alpha=0.3)
    
    # 3. Salva a imagem em memória e fecha a figura
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close(fig) # Essencial: libera a memória RAM do servidor
    
    # 4. Codifica em Base64
    imagem_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    
    # 5. Retorna o JSON para o frontend
    return {"imagem_base64": imagem_base64}