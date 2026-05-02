import { useState } from 'react';
import './App.css';

function App() {
  const [userInput, setUserInput] = useState('');
  const [systemState, setSystemState] = useState({
    response: 'Awaiting input...',
    providerUsed: null,
    latency: null,
    loading: false,
    error: null
  });
  const [selectedProvider, setSelectedProvider] = useState('gemini');

  const handleSend = async () => {
    if (!userInput.trim()) return;
    
    setSystemState({ response: 'Processing request...', providerUsed: null, latency: null, loading: true, error: null });

    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: userInput, provider: selectedProvider }),
      });

      if (!res.ok) throw new Error('Backend services unavailable');

      const data = await res.json();
      setSystemState({
        response: data.response,
        providerUsed: data.provider_used,
        latency: data.latency_ms,
        loading: false,
        error: null
      });
    } catch (error) {
      setSystemState({ response: '', providerUsed: null, latency: null, loading: false, error: error.message });
    }
  };

  return (
    <div className="gateway-container">
      <header className="gateway-header">
        <h1>Nexus LLM Gateway</h1>
        <div className="status-badge">
          <span className="dot pulse"></span> Live Async Router
        </div>
      </header>
      
      <main className="gateway-main">
        <div className="control-panel">
          <div className="input-group">
            <label>Primary Engine Route</label>
            <select 
              value={selectedProvider} 
              onChange={(e) => setSelectedProvider(e.target.value)}
              className="provider-select"
            >
              <option value="gemini">Gemini 2.5 Flash</option>
              <option value="openai">GPT-4o Mini</option>
              <option value="claude">Claude 3.5 Sonnet</option>
            </select>
          </div>
        </div>

        <div className="chat-interface">
          <textarea 
            value={userInput} 
            onChange={(e) => setUserInput(e.target.value)}
            placeholder="Initialize query sequence..."
            className="prompt-input"
          />
          <button onClick={handleSend} disabled={systemState.loading} className="send-btn">
            {systemState.loading ? "Routing..." : "Execute Request"}
          </button>
        </div>

        <div className="response-panel">
          <div className="response-header">
            <h3>System Output</h3>
            {systemState.latency && (
              <div className="metrics">
                <span className="metric-tag provider-tag">{systemState.providerUsed.toUpperCase()}</span>
                <span className="metric-tag latency-tag">{systemState.latency}ms</span>
              </div>
            )}
          </div>
          
          <div className={`response-content ${systemState.error ? 'error-text' : ''}`}>
            {systemState.error ? `System Error: ${systemState.error}` : systemState.response}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;