import { useState } from 'react';

function App() {
  const [n, setN] = useState(1000);
  const [seed, setSeed] = useState(42);
  // NOVO ESTADO: Probabilidade de Cara (0 a 100)
  const [probabilidade, setProbabilidade] = useState(50); 
  const [imagem, setImagem] = useState(null);
  const [carregando, setCarregando] = useState(false);

  const handleSimular = async () => {
    setCarregando(true);
    setImagem(null);

    try {
      const response = await fetch('http://localhost:8000/simular', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          n: parseInt(n), 
          seed: parseInt(seed),
          // NOVO: Envia a probabilidade dividida por 100 (ex: 50% -> 0.5)
          p_cara: probabilidade / 100 
        }),
      });

      if (!response.ok) {
        throw new Error('Falha na simulação');
      }

      const data = await response.json();
      setImagem(`data:image/png;base64,${data.imagem_base64}`);
      
    } catch (error) {
      console.error(error);
      alert('Erro ao conectar com o backend. O servidor está rodando?');
    } finally {
      setCarregando(false);
    }
  };

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', padding: '2rem' }}>
      <h1>Simulador de Processos Estocásticos</h1>
      <p>Moeda (Cara = +1, Coroa = -1)</p>

      <div style={{ 
        display: 'flex', 
        gap: '1rem', 
        alignItems: 'flex-end', 
        marginBottom: '2rem',
        backgroundColor: '#fff',
        padding: '1.5rem',
        borderRadius: '8px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
        flexWrap: 'wrap' // Permite quebrar linha em telas menores
      }}>
        <div>
          <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
            Lançamentos (n):
          </label>
          <input 
            type="number" 
            value={n} 
            onChange={(e) => setN(e.target.value)}
            style={{ padding: '0.5rem', width: '100px' }}
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
            style={{ padding: '0.5rem', width: '100px' }}
          />
        </div>

        {/* NOVO: Slider de Probabilidade */}
        <div style={{ flex: 1, minWidth: '250px' }}>
          <label style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem', fontWeight: 'bold' }}>
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
            onChange={(e) => setProbabilidade(parseInt(e.target.value))}
            style={{ width: '100%', cursor: 'pointer' }}
          />
        </div>

        <button 
          onClick={handleSimular} 
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
            flexShrink: 0
          }}
        >
          {carregando ? 'Simulando...' : 'Simular'}
        </button>
      </div>

      {imagem && (
        <div style={{ 
          backgroundColor: '#fff', 
          padding: '1rem', 
          borderRadius: '8px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          textAlign: 'center'
        }}>
          <h2>Resultado</h2>
          <img 
            src={imagem} 
            alt="Gráfico da simulação" 
            style={{ maxWidth: '100%', height: 'auto' }} 
          />
        </div>
      )}
    </div>
  );
}

export default App;