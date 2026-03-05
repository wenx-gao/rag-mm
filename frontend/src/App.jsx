import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Upload, FileText, Bot, User, Loader2, AlertCircle } from 'lucide-react';

const API_BASE = "http://localhost:8000/api/v1";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  
  const fileInputRef = useRef(null);
  const chatContainerRef = useRef(null);
  const [lastUploadedFile, setLastUploadedFile] = useState("");

  // Auto-scroll to the bottom when new messages arrive
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages, loading]);

  // --- 1. Handle File Upload ---
  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setLastUploadedFile(file.name);
    setUploading(true);
    setError(null);
    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post(`${API_BASE}/upload`, formData);
      alert(`Success: "${file.name}" uploaded. Processing started in background.`);
    } catch (err) {
      console.error("Upload failed", err);
      setError("Failed to upload document. Is the backend running?");
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = "";
    }
  };

  // --- 2. Handle Sending Queries ---
  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    const currentInput = input;
    setInput("");
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(`${API_BASE}/query`, { 
        question: currentInput,
        top_k: 20 // Using the optimized top_k we discussed
      });
      
      const botMessage = { 
        role: 'bot', 
        content: response.data.answer,
        sources: response.data.sources 
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      console.error("Query failed", err);
      setError("AI failed to respond. Check if Ollama and the API are running.");
      setMessages(prev => [...prev, { 
        role: 'bot', 
        content: "Sorry, I encountered an error while processing your request." 
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50 font-sans text-gray-900">
      
      {/* --- HEADER --- */}
      <header className="flex justify-between items-center px-8 py-4 bg-white shadow-sm border-b border-gray-200">
        <div className="flex items-center gap-3">
          <div className="bg-blue-600 p-2 rounded-lg text-white">
            <Bot size={24} />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight">RAG-mm Explorer</h1>
            <p className="text-xs text-gray-500 font-medium uppercase tracking-widest">Local Multimodal AI</p>
          </div>
        </div>
        
        <div className="flex items-center gap-4">
          <input type="file" ref={fileInputRef} onChange={handleUpload} className="hidden" />
          
          {/* Wir packen Button und Name in ein div für ordentliche Ausrichtung */}
          <div className="flex flex-col items-end">
            <button 
              onClick={() => fileInputRef.current.click()}
              disabled={uploading}
              className="flex items-center gap-2 bg-white border border-gray-300 px-4 py-2 rounded-lg hover:bg-gray-50 transition-all font-medium text-sm disabled:opacity-50 shadow-sm"
            >
              {uploading ? <Loader2 className="animate-spin text-blue-600" size={18} /> : <Upload size={18} className="text-gray-600" />}
              {uploading ? "Wird verarbeitet..." : "PDF hochladen"}
            </button>
            
            {/* HIER wird der Name angezeigt, wenn eine Datei vorhanden ist */}
            {lastUploadedFile && (
              <span className="text-[10px] text-blue-600 font-bold mt-1 animate-pulse">
                Aktiv: {lastUploadedFile}
              </span>
            )}
          </div>
        </div>
      </header>

      {/* --- ERROR BAR --- */}
      {error && (
        <div className="bg-red-50 border-b border-red-100 px-8 py-2 flex items-center gap-2 text-red-600 text-sm">
          <AlertCircle size={16} /> {error}
        </div>
      )}

      {/* --- CHAT AREA --- */}
      <main 
        ref={chatContainerRef}
        className="flex-1 overflow-y-auto p-8 space-y-6 max-w-5xl w-full mx-auto"
      >
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center space-y-4">
            <div className="bg-blue-50 p-6 rounded-full text-blue-200">
              <FileText size={64} />
            </div>
            <div className="max-w-xs">
              <h2 className="text-lg font-semibold text-gray-700">No documents indexed yet</h2>
              <p className="text-gray-400 text-sm">Upload a technical PDF or Excel to start chatting with your local AI.</p>
            </div>
          </div>
        )}

        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`flex gap-3 max-w-[85%] ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
              <div className={`flex-shrink-0 h-10 w-10 rounded-full flex items-center justify-center shadow-sm ${msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-white border border-gray-200 text-gray-600'}`}>
                {msg.role === 'user' ? <User size={20} /> : <Bot size={20} />}
              </div>
              
              <div className={`p-4 rounded-2xl shadow-sm border ${msg.role === 'user' ? 'bg-blue-600 text-white border-blue-500' : 'bg-white border-gray-200'}`}>
                <p className="whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                
                {/* --- SOURCES SECTION --- */}
                {msg.sources && msg.sources.length > 0 && (
                  <div className={`mt-4 pt-3 border-t text-xs ${msg.role === 'user' ? 'border-blue-400' : 'border-gray-100'}`}>
                    <span className="font-bold uppercase tracking-wider opacity-60">Verified Sources</span>
                    <div className="mt-2 space-y-1">
                      {msg.sources.map((s, i) => (
                        <div key={i} className="flex items-center gap-2">
                          <FileText size={12} className="opacity-50" />
                          <span className="font-medium">[{s.citation_id}] {s.document}</span>
                          <span className="opacity-50">• p.{s.page || "N/A"} • {s.element_type}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
        
        {loading && (
          <div className="flex justify-start">
            <div className="flex gap-3 items-center text-gray-400 text-sm animate-pulse">
              <Loader2 className="animate-spin" size={16} />
              AI is thinking...
            </div>
          </div>
        )}
      </main>

      {/* --- INPUT AREA --- */}
      <footer className="bg-white border-t border-gray-200 p-6">
        <div className="max-w-5xl mx-auto flex items-end gap-4 bg-gray-50 rounded-2xl border border-gray-300 p-3 focus-within:ring-2 focus-within:ring-blue-100 focus-within:border-blue-400 transition-all">
          <textarea 
            rows="3"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            placeholder="Ask your documents anything..."
            className="flex-1 bg-transparent border-none outline-none resize-none py-2 px-3 text-gray-700 placeholder-gray-400"
          />
          <button 
            onClick={handleSend}
            disabled={loading || !input.trim()}
            className="bg-blue-600 text-white p-4 rounded-xl hover:bg-blue-700 transition-colors shadow-lg shadow-blue-200 disabled:opacity-30 disabled:shadow-none"
          >
            <Send size={24} />
          </button>
        </div>
        <p className="text-center text-[10px] text-gray-400 mt-3 uppercase tracking-widest">
          Powered by Ollama, Docling & Qdrant • Running Locally
        </p>
      </footer>
    </div>
  );
}

export default App;
