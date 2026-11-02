import { useState } from 'react';

function App() {
  // 1. Estados do React
  const [n, setN] = useState(1000);           // Número de lançamentos
  const [seed, setSeed] = useState(42);       // Semente
  const [imagem, setImagem] = useState(null); // String Base64 do gráfico
  const [carregando, setCarregando] = useState(false); // Status do botão

  // 2. Função que faz a chamada para o Backend
  const handleSimular = async () => {
    setCarregando(true);
    setImagem(null); // Limpa a imagem anterior, se houver

    try {
      // Fazemos um POST para o FastAPI
      const response = await fetch('http://localhost:8000/simular', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        // Convertemos n e seed para inteiros, pois os inputs do HTML retornam strings
        body: JSON.stringify({ n: parseInt(n), seed: parseInt(seed) }),
      });

      if (!response.ok) {
        throw new Error('Falha na simulação');
      }

      const data = await response.json();
      
      // 3. Monta a URL de dados que a tag <img> consegue renderizar
      setImagem(`data:image/png;base64,${data.imagem_base64}`);
      
    } catch (error) {
      console.error(error);
      alert('Erro ao conectar com o backend. O servidor está rodando?');
    } finally {
      setCarregando(false);
    }
  };

  // 4. A Interface Visual (JSX)
  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', padding: '2rem' }}>
      <h1>Simulador de Processos Estocásticos</h1>
      <p>Moeda Justa (Cara = +1, Coroa = -1)</p>

      {/* Painel de Controle */}
      <div style={{ 
        display: 'flex', 
        gap: '1rem', 
        alignItems: 'flex-end', 
        marginBottom: '2rem',
        backgroundColor: '#fff',
        padding: '1.5rem',
        borderRadius: '8px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
      }}>
        <div>
          <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
            Lançamentos (n):
          </label>
          <input 
            type="number" 
            value={n} 
            onChange={(e) => setN(e.target.value)}
            style={{ padding: '0.5rem', width: '120px' }}
          />
        </div>

        <div>
          <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
            Semente (seed):
          </label>
          <input 
            type="number" 
            value={seed} 
            onChange={(e) => setSeed(e.target.value)}
            style={{ padding: '0.5rem', width: '120px' }}
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
            height: '40px'
          }}
        >
          {carregando ? 'Simulando...' : 'Simular'}
        </button>
      </div>

      {/* Área de Exibição do Gráfico */}
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