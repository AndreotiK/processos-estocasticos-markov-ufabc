"""
Módulo de simulação de lançamentos de moeda justa.

Convenção adotada neste módulo
------------------------------
    cara  = +1
    coroa = -1

Cada lançamento é modelado como X_i = 2 * B_i - 1, onde B_i ~ Bernoulli(1/2)
com B_i ∈ {0, 1}. Assim:
    B_i = 0  ->  X_i = -1  (coroa)
    B_i = 1  ->  X_i = +1  (cara)

A média acumulada M_t = (X_1 + ... + X_t) / t é a variável usada
posteriormente para visualizar a convergência (Lei dos Grandes Números).
"""

import numpy as np


def gerar_lancamentos(n: int, seed: int | None = None) -> np.ndarray:
    """
    Gera uma sequência de n lançamentos de uma moeda justa.

    Parameters
    ----------
    n : int
        Número de lançamentos. Deve ser >= 1.
    seed : int ou None, opcional
        Semente do gerador. Se None, cada chamada produz uma sequência
        diferente. Se fornecida, o resultado é reprodutível.

    Returns
    -------
    np.ndarray
        Array 1D de comprimento n, com valores em {-1, +1}.

    Raises
    ------
    ValueError
        Se n não for inteiro ou for menor que 1.
    """
    if not isinstance(n, (int, np.integer)) or n < 1:
        raise ValueError(f"n deve ser inteiro >= 1; recebido: {n!r}")

    rng = np.random.default_rng(seed)
    bits = rng.integers(low=0, high=2, size=n)   # high é exclusivo
    return 2 * bits - 1                          # 0 -> -1 ; 1 -> +1


def calcular_media_acumulada(lancamentos: np.ndarray) -> np.ndarray:
    """
    Calcula a média acumulada M_t = (X_1 + ... + X_t) / t para t = 1..n.

    Parameters
    ----------
    lancamentos : np.ndarray
        Array 1D de comprimento n >= 1, com valores em {-1, +1}.

    Returns
    -------
    np.ndarray
        Array 1D de mesmo comprimento, onde a posição t-1 contém M_t.

    Raises
    ------
    ValueError
        Se o array não for 1D ou estiver vazio.
    """
    lancamentos = np.asarray(lancamentos)
    if lancamentos.ndim != 1 or lancamentos.size == 0:
        raise ValueError(
            f"esperado array 1D não vazio; recebido shape={lancamentos.shape}"
        )

    n = lancamentos.size
    soma_acumulada = np.cumsum(lancamentos)        # S_t = X_1 + ... + X_t
    indices = np.arange(1, n + 1)                  # t = 1, 2, ..., n
    return soma_acumulada / indices


# ----------------------------------------------------------------------
# Auto-teste: executar `python src/markov_systems/simulation.py` da raiz
# ----------------------------------------------------------------------
if __name__ == "__main__":
    SEED = 10
    N = 10

    print("=" * 60)
    print("Auto-teste de simulation.py")
    print("=" * 60)

    # (1) Geração com seed fixa
    x = gerar_lancamentos(N, seed=SEED)
    print(f"\nlançamentos (n={N}, seed={SEED}):")
    print(x)

    # (2) Comprimento
    assert len(x) == N, f"comprimento {len(x)} != {N}"

    # (3) Domínio
    assert set(x).issubset({-1, 1}), f"valores fora de {{-1,+1}}: {set(x)}"

    # (4) Reprodutibilidade
    x2 = gerar_lancamentos(N, seed=SEED)
    assert np.array_equal(x, x2), "mesma seed produziu sequências diferentes"

    # (5) Sensibilidade à seed
    x3 = gerar_lancamentos(N, seed=SEED + 1)
    assert not np.array_equal(x, x3), "seeds diferentes produziram mesma sequência"

    # (6) Média acumulada — conferência manual em sequência curta
    print("\nmédia acumulada para sequência curta de teste:")
    curta = np.array([+1, +1, -1, +1])              # M = [1, 1, 1/3, 1/2]
    m_curta = calcular_media_acumulada(curta)
    esperado = np.array([1.0, 1.0, 1/3, 0.5])
    print(f"  lançamentos : {curta}")
    print(f"  M calculada : {m_curta}")
    print(f"  M esperada  : {esperado}")
    assert np.allclose(m_curta, esperado), "média acumulada divergiu do esperado"

    # (7) Média acumulada da sequência principal
    m = calcular_media_acumulada(x)
    print(f"\nmédia acumulada (n={N}):")
    print(m)
    print(f"M_final = {m[-1]:.6f}")
    assert abs(m[-1]) <= 1.0, "|M_n| > 1 é impossível para X_i ∈ {-1,+1}"

    print("\n" + "=" * 60)
    print("Todas as verificações passaram.")
    print("=" * 60)