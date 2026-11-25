from pydantic import BaseModel, Field


class SimulacaoRequest(BaseModel):
    n: int = Field(..., ge=1, description="Número de lançamentos (n >= 1)")
    seed: int | None = Field(default=None, description="Semente do gerador pseudoaleatório")
    p_cara: float = Field(default=0.5, ge=0.0, le=1.0, description="Probabilidade de cara em [0, 1]")
    mostrar_desvio_padrao: bool = Field(
        default=True,
        description="Exibe a faixa de ±1 desvio padrão no gráfico do passeio aleatório",
    )


class SimulacaoResponse(BaseModel):
    grafico_media_base64: str
    grafico_passeio_base64: str