"""
Módulo de simulação de lançamentos de moeda.

Convenção adotada neste módulo
------------------------------
    cara  = +1
    coroa = -1

Cada lançamento é modelado como X_i = 2 * B_i - 1, onde B_i ~ Bernoulli(p_cara)
com B_i ∈ {0, 1}. Assim:
    B_i = 0  ->  X_i = -1  (coroa)
    B_i = 1  ->  X_i = +1  (cara)

- A média acumulada M_t = (X_1 + ... + X_t) / t ilustra a Lei dos Grandes Números.
- A soma acumulada S_t = X_1 + ... + X_t modela um Passeio Aleatório 1D com deriva.
"""

import numpy as np


def gerar_lancamentos(n: int, seed: int | None = None, p_cara: float = 0.5) -> np.ndarray:
    """
    Gera uma sequência de n lançamentos de uma moeda, com probabilidade p_cara.
    """
    if not isinstance(n, (int, np.integer)) or n < 1:
        raise ValueError(f"n deve ser inteiro >= 1; recebido: {n!r}")
        
    if not (0.0 <= p_cara <= 1.0):
        raise ValueError(f"p_cara deve estar entre 0.0 e 1.0; recebido: {p_cara!r}")

    rng = np.random.default_rng(seed)
    bits = (rng.random(size=n) < p_cara).astype(int)
    
    return 2 * bits - 1


def calcular_media_acumulada(lancamentos: np.ndarray) -> np.ndarray:
    """
    Calcula a média acumulada M_t = (X_1 + ... + X_t) / t para t = 1..n.
    """
    lancamentos = np.asarray(lancamentos)
    if lancamentos.ndim != 1 or lancamentos.size == 0:
        raise ValueError(
            f"esperado array 1D não vazio; recebido shape={lancamentos.shape}"
        )

    n = lancamentos.size
    soma_acumulada = np.cumsum(lancamentos)
    indices = np.arange(1, n + 1)
    return soma_acumulada / indices


def calcular_soma_acumulada(lancamentos: np.ndarray) -> np.ndarray:
    """
    Calcula a soma acumulada S_t = X_1 + ... + X_t (Passeio Aleatório 1D) para t = 1..n.
    """
    lancamentos = np.asarray(lancamentos)
    if lancamentos.ndim != 1 or lancamentos.size == 0:
        raise ValueError(
            f"esperado array 1D não vazio; recebido shape={lancamentos.shape}"
        )

    return np.cumsum(lancamentos)


# ----------------------------------------------------------------------
# Auto-teste: executar `python src/markov_systems/simulation.py` da raiz
# ----------------------------------------------------------------------
if __name__ == "__main__":
    SEED = 10
    N = 10000

    print("=" * 60)
    print("Auto-teste de simulation.py")
    print("=" * 60)

    x = gerar_lancamentos(N, seed=SEED, p_cara=0.5)
    print(f"\nlançamentos (n={N}, seed={SEED}, p_cara=0.5):")
    print(f"  Média final: {calcular_media_acumulada(x)[-1]:.4f} (esperado ~0.0)")
    print(f"  Posição final S_n: {calcular_soma_acumulada(x)[-1]}")

    assert len(x) == N, f"comprimento {len(x)} != {N}"
    assert set(x).issubset({-1, 1}), f"valores fora de {{-1,+1}}: {set(x)}"

    x2 = gerar_lancamentos(N, seed=SEED, p_cara=0.5)
    assert np.array_equal(x, x2), "mesma seed produziu sequências diferentes"

    x_viciada = gerar_lancamentos(N, seed=SEED, p_cara=0.8)
    media_viciada = calcular_media_acumulada(x_viciada)[-1]
    soma_viciada = calcular_soma_acumulada(x_viciada)[-1]
    print(f"\nlançamentos (n={N}, seed={SEED}, p_cara=0.8):")
    print(f"  Média final: {media_viciada:.4f} (esperado ~0.6)")
    print(f"  Posição final S_n: {soma_viciada} (esperado ~6000)")
    
    assert abs(media_viciada - 0.6) < 0.05, "A média não convergiu para o valor esperado (0.6)"

    curta = np.array([+1, +1, -1, +1])
    assert np.allclose(calcular_media_acumulada(curta), np.array([1.0, 1.0, 1/3, 0.5]))
    assert np.array_equal(calcular_soma_acumulada(curta), np.array([1, 2, 1, 2]))

    print("\n" + "=" * 60)
    print("Todas as verificações passaram.")
    print("=" * 60)