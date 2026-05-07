import { useState } from 'react';

export default function App() {
  const [mes, setMes] = useState([]);
  const [val, setVal] = useState('');

  const sendMessage = async () => {
    if (!val.trim()) return;

    const userMessage = { text: val, sender: 'user' };
    setMes(prev => [...prev, userMessage]);
    setVal('');

    try {
      const response = await fetch(`http://localhost:8000/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: val }),
      });

      if (!response.ok) throw new Error('Backend error');
      const data = await response.json();

      setMes(prev => [...prev, { text: data.response, sender: 'ai' }]);
    } catch (e) {
      console.error(e);
      alert('Could not connect to the backend server.');
    }
  };

  return (
    <div className="bg-black flex flex-col justify-center items-center min-h-screen p-4">
      <div className="bg-slate-900 w-full max-w-lg rounded-3xl border border-slate-800 flex flex-col h-[70vh] shadow-2xl overflow-hidden">
        
        <div className="bg-slate-800/50 w-full flex items-center p-6 gap-4 border-b border-slate-800">
          <div className="w-3 h-3 rounded-full bg-green-400 animate-pulse"></div>
          <h1 className="text-white font-bold text-2xl">AI Chatbot</h1>
        </div>
        <div className="flex-1 p-4 space-y-4">
          {mes.length === 0 ? (
            <div className="h-full flex items-center justify-center text-slate-500 italic text-sm">
              Type a message to start chatting...
            </div>
          ) : (
            mes.map((m, i) => (
              <div className={`flex ${m.sender === 'user' ? 'justify-end' : ''}`} key={i}>
                <div className={`px-4 py-2 rounded-2xl max-w-[80%] text-white text-sm ${m.sender === 'user' ? 'bg-emerald-600 rounded-br-none' : 'bg-slate-800 rounded-bl-none'}`}>
                  <p>{m.text}</p>
                </div>
              </div>
            ))
          )}
        </div>
        <div className="p-4 bg-slate-900 border-t border-slate-800">
          <div className="flex bg-slate-950 border border-slate-700 rounded-2xl p-1 focus-within:border-emerald-500 transition-all">
            <input 
              type="text" 
              value={val} 
              onChange={(e) => setVal(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Message AI..." 
              className="flex-1 bg-transparent px-4 py-2 outline-none text-white text-sm"
            />
            <button 
              onClick={sendMessage}
              className="bg-emerald-500 hover:bg-emerald-400 text-slate-900 font-bold px-5 py-2 rounded-xl transition-all active:scale-95 text-sm"
            >
              Send
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}
