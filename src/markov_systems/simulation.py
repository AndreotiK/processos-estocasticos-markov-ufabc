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

A média acumulada M_t = (X_1 + ... + X_t) / t é a variável usada
posteriormente para visualizar a convergência (Lei dos Grandes Números).
"""

import numpy as np


def gerar_lancamentos(n: int, seed: int | None = None, p_cara: float = 0.5) -> np.ndarray:
    """
    Gera uma sequência de n lançamentos de uma moeda, com probabilidade p_cara.

    Parameters
    ----------
    n : int
        Número de lançamentos. Deve ser >= 1.
    seed : int ou None, opcional
        Semente do gerador. Se None, cada chamada produz uma sequência
        diferente. Se fornecida, o resultado é reprodutível.
    p_cara : float, opcional
        Probabilidade de sair cara (valor entre 0.0 e 1.0). Padrão é 0.5 (moeda justa).

    Returns
    -------
    np.ndarray
        Array 1D de comprimento n, com valores em {-1, +1}.

    Raises
    ------
    ValueError
        Se n não for inteiro ou for menor que 1.
        Se p_cara não estiver no intervalo [0, 1].
    """
    if not isinstance(n, (int, np.integer)) or n < 1:
        raise ValueError(f"n deve ser inteiro >= 1; recebido: {n!r}")
        
    if not (0.0 <= p_cara <= 1.0):
        raise ValueError(f"p_cara deve estar entre 0.0 e 1.0; recebido: {p_cara!r}")

    rng = np.random.default_rng(seed)
    
    # Gera números uniformes entre 0 e 1. 
    # Se o número for menor que p_cara, o resultado booleano é True (1), senão False (0).
    bits = (rng.random(size=n) < p_cara).astype(int) 
    
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
    N = 10000

    print("=" * 60)
    print("Auto-teste de simulation.py")
    print("=" * 60)

    # (1) Geração com seed fixa (Moeda Justa)
    x = gerar_lancamentos(N, seed=SEED, p_cara=0.5)
    print(f"\nlançamentos (n={N}, seed={SEED}, p_cara=0.5):")
    print(f"  Média final: {calcular_media_acumulada(x)[-1]:.4f} (esperado ~0.0)")

    # (2) Comprimento e Domínio
    assert len(x) == N, f"comprimento {len(x)} != {N}"
    assert set(x).issubset({-1, 1}), f"valores fora de {{-1,+1}}: {set(x)}"

    # (3) Reprodutibilidade
    x2 = gerar_lancamentos(N, seed=SEED, p_cara=0.5)
    assert np.array_equal(x, x2), "mesma seed produziu sequências diferentes"

    # (4) Teste de Moeda Viciada (80% de chance de Cara)
    x_viciada = gerar_lancamentos(N, seed=SEED, p_cara=0.8)
    media_viciada = calcular_media_acumulada(x_viciada)[-1]
    print(f"\nlançamentos (n={N}, seed={SEED}, p_cara=0.8):")
    print(f"  Média final: {media_viciada:.4f} (esperado ~0.6)")
    
    # A esperança matemática para p_cara=0.8 é (2 * 0.8) - 1 = 0.6
    assert abs(media_viciada - 0.6) < 0.05, "A média não convergiu para o valor esperado (0.6)"

    # (5) Teste de Extremos (100% Cara e 100% Coroa)
    x_extremo_cara = gerar_lancamentos(10, seed=SEED, p_cara=1.0)
    assert np.all(x_extremo_cara == 1), "p_cara=1.0 não gerou todas caras"
    
    x_extremo_coroa = gerar_lancamentos(10, seed=SEED, p_cara=0.0)
    assert np.all(x_extremo_coroa == -1), "p_cara=0.0 não gerou todas coroas"

    # (6) Média acumulada — conferência manual
    print("\nmédia acumulada para sequência curta de teste:")
    curta = np.array([+1, +1, -1, +1])              # M = [1, 1, 1/3, 1/2]
    m_curta = calcular_media_acumulada(curta)
    esperado = np.array([1.0, 1.0, 1/3, 0.5])
    print(f"  lançamentos : {curta}")
    print(f"  M calculada : {m_curta}")
    print(f"  M esperada  : {esperado}")
    assert np.allclose(m_curta, esperado), "média acumulada divergiu do esperado"

    print("\n" + "=" * 60)
    print("Todas as verificações passaram.")
    print("=" * 60)