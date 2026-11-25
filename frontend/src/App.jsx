import { useState } from 'react';

function App() {
  const [n, setN] = useState(1000);
  const [seed, setSeed] = useState(42);
  const [probabilidade, setProbabilidade] = useState(50);
  const [mostrarDesvioPadrao, setMostrarDesvioPadrao] = useState(true);

  const [graficoMedia, setGraficoMedia] = useState(null);
  const [graficoPasseio, setGraficoPasseio] = useState(null);
  const [carregando, setCarregando] = useState(false);

  const executarSimulacao = async (exibirDp = mostrarDesvioPadrao) => {
    setCarregando(true);

    try {
      const response = await fetch('http://localhost:8000/simular', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          n: parseInt(n, 10),
          seed: seed === '' ? null : parseInt(seed, 10),
          p_cara: probabilidade / 100,
          mostrar_desvio_padrao: exibirDp,
        }),
      });

      if (!response.ok) {
        throw new Error('Falha na simulação');
      }

      const data = await response.json();
      setGraficoMedia(`data:image/png;base64,${data.grafico_media_base64}`);
      setGraficoPasseio(`data:image/png;base64,${data.grafico_passeio_base64}`);
    } catch (error) {
      console.error(error);
      alert('Erro ao conectar com o backend. O servidor está rodando?');
    } finally {
      setCarregando(false);
    }
  };

  const handleToggleDesvioPadrao = (e) => {
    const novoValor = e.target.checked;
    setMostrarDesvioPadrao(novoValor);

    // Atualiza o gráfico automaticamente se já houver uma simulação exibida
    if (graficoPasseio) {
      executarSimulacao(novoValor);
    }
  };

  return (
    <div style={{ maxWidth: '960px', margin: '0 auto', padding: '2rem' }}>
      <h1>Simulador de Processos Estocásticos</h1>
      <p>Ensaios de Bernoulli Simétricos e Assimétricos (Cara = +1, Coroa = -1)</p>

      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '1.25rem',
          marginBottom: '2rem',
          backgroundColor: '#fff',
          padding: '1.5rem',
          borderRadius: '8px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
        }}
      >
        <div
          style={{
            display: 'flex',
            gap: '1rem',
            alignItems: 'flex-end',
            flexWrap: 'wrap',
          }}
        >
          <div>
            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
              Lançamentos (n):
            </label>
            <input
              type="number"
              min="1"
              value={n}
              onChange={(e) => setN(e.target.value)}
              style={{ padding: '0.5rem', width: '110px' }}
            />
          </div>

          <div>
            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
              Semente:
            </label>
            <input
              type="number"
              value={seed}
              onChange={(e) => setSeed(e.target.value)}
              style={{ padding: '0.5rem', width: '110px' }}
            />
          </div>

          <div style={{ flex: 1, minWidth: '250px' }}>
            <label
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                marginBottom: '0.5rem',
                fontWeight: 'bold',
              }}
            >
              <span>Coroa (0%)</span>
              <span style={{ color: '#007bff' }}>Cara: {probabilidade}%</span>
              <span>Cara (100%)</span>
            </label>
            <input
              type="range"
              min="0"
              max="100"
              step="1"
              value={probabilidade}
              onChange={(e) => setProbabilidade(parseInt(e.target.value, 10))}
              style={{ width: '100%', cursor: 'pointer' }}
            />
          </div>

          <button
            onClick={() => executarSimulacao()}
            disabled={carregando}
            style={{
              padding: '0.5rem 1.5rem',
              backgroundColor: carregando ? '#ccc' : '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: carregando ? 'not-allowed' : 'pointer',
              fontWeight: 'bold',
              height: '40px',
              flexShrink: 0,
            }}
          >
            {carregando ? 'Simulando...' : 'Simular'}
          </button>
        </div>

        {/* Toggle para faixa de desvio padrão */}
        <div style={{ borderTop: '1px solid #eee', paddingTop: '0.75rem' }}>
          <label
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.5rem',
              cursor: 'pointer',
              userSelect: 'none',
              fontWeight: '500',
            }}
          >
            <input
              type="checkbox"
              checked={mostrarDesvioPadrao}
              onChange={handleToggleDesvioPadrao}
              style={{ width: '16px', height: '16px', cursor: 'pointer' }}
            />
            Exibir faixa de ±1 desvio padrão no Passeio Aleatório (σ = 2√[t·p·(1-p)])
          </label>
        </div>
      </div>

      {graficoMedia && graficoPasseio && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div
            style={{
              backgroundColor: '#fff',
              padding: '1.5rem',
              borderRadius: '8px',
              boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
              textAlign: 'center',
            }}
          >
            <h2 style={{ marginTop: 0 }}>
              1. Lei Forte dos Grandes Números (Média Amostral)
            </h2>
            <img
              src={graficoMedia}
              alt="Gráfico da Lei Forte dos Grandes Números"
              style={{ maxWidth: '100%', height: 'auto' }}
            />
          </div>

          <div
            style={{
              backgroundColor: '#fff',
              padding: '1.5rem',
              borderRadius: '8px',
              boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
              textAlign: 'center',
            }}
          >
            <h2 style={{ marginTop: 0 }}>
              2. Passeio Aleatório Unidimensional com Deriva (Soma Acumulada)
            </h2>
            <img
              src={graficoPasseio}
              alt="Gráfico do Passeio Aleatório Unidimensional"
              style={{ maxWidth: '100%', height: 'auto' }}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;