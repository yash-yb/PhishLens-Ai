import React, { useState } from 'react';
import { Upload, Shield, AlertTriangle, CheckCircle, Info, RefreshCw, Eye } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';

const API_BASE = 'http://localhost:5000/api';

function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
      setResult(null);
      setError(null);
    }
  };

  const handleScan = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('image', file);

    try {
      const response = await axios.post(`${API_BASE}/scan`, formData);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Analysis failed. Make sure services are running.');
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (level) => {
    if (level === 'Safe') return 'text-emerald-400';
    if (level === 'Suspicious') return 'text-amber-400';
    return 'text-rose-500';
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
      {/* Header */}
      <header className="text-center mb-16 animate-fade-in">
        <div className="inline-flex items-center justify-center p-3 glass-card mb-6 mb-4">
          <Shield className="w-8 h-8 text-indigo-400" />
        </div>
        <h1 className="text-5xl font-extrabold tracking-tight mb-4 bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-rose-400">
          PhishLens AI
        </h1>
        <p className="text-slate-400 text-lg max-w-2xl mx-auto">
          Deep semantic analysis for WhatsApp images. Detect phishing, scams, and social engineering in seconds.
        </p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">
        {/* Upload Section */}
        <section className="glass-card p-8 animate-fade-in" style={{ animationDelay: '0.1s' }}>
          <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
            <Upload className="w-5 h-5 text-indigo-400" />
            Upload Target Image
          </h2>
          
          <div 
            className={`border-2 border-dashed rounded-xl p-12 text-center transition-all cursor-pointer ${
              preview ? 'border-indigo-500/50 bg-indigo-500/5' : 'border-slate-700 hover:border-slate-500'
            }`}
            onClick={() => document.getElementById('fileInput').click()}
          >
            <input 
              type="file" 
              id="fileInput" 
              hidden 
              onChange={handleFileChange} 
              accept="image/*"
            />
            {preview ? (
              <img src={preview} alt="Preview" className="max-w-full max-h-64 mx-auto rounded-lg shadow-xl" />
            ) : (
              <div className="py-8">
                <Upload className="w-12 h-12 text-slate-600 mx-auto mb-4" />
                <p className="text-slate-400">Drop an image here or click to browse</p>
                <p className="text-slate-600 text-sm mt-2">Supports JPG, PNG (Max 5MB)</p>
              </div>
            )}
          </div>

          <button 
            disabled={!file || loading}
            onClick={handleScan}
            className={`w-full mt-6 btn-primary disabled:opacity-50 disabled:scale-100 flex items-center justify-center gap-2 py-3`}
          >
            {loading ? (
              <>
                <RefreshCw className="w-5 h-5 animate-spin" />
                Analyzing with AI...
              </>
            ) : (
              <>
                <Eye className="w-5 h-5" />
                Scan for Threats
              </>
            )}
          </button>
          
          {error && (
            <div className="mt-4 p-4 bg-rose-500/10 border border-rose-500/20 rounded-lg flex items-center gap-3 text-rose-400 animate-fade-in">
              <AlertTriangle className="w-5 h-5" />
              <p className="text-sm">{error}</p>
            </div>
          )}
        </section>

        {/* Results Section */}
        <AnimatePresence mode="wait">
          {result ? (
            <motion.section 
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="glass-card p-8 min-h-[500px]"
            >
              <div className="flex justify-between items-start mb-8">
                <div>
                  <h2 className="text-xl font-bold mb-1 flex items-center gap-2 text-slate-100">
                    Scan Result
                  </h2>
                  <p className="text-slate-400 text-sm">Detection complete</p>
                </div>
                <div className={`text-3xl font-black ${getRiskColor(result.risk_level)}`}>
                  {result.risk_score}%
                </div>
              </div>

              <div className={`p-6 rounded-xl mb-8 flex items-center gap-4 ${
                result.risk_level === 'Safe' ? 'bg-emerald-500/10 border border-emerald-500/20' : 
                'bg-rose-500/10 border border-rose-500/20'
              }`}>
                {result.risk_level === 'Safe' ? (
                  <CheckCircle className="w-8 h-8 text-emerald-400" />
                ) : (
                  <AlertTriangle className="w-8 h-8 text-rose-500" />
                )}
                <div>
                  <p className="font-bold text-lg">{result.risk_level}</p>
                  <p className="text-slate-400 text-sm">
                    {result.risk_level === 'Safe' ? 'No significant threats detected.' : 'This image contains suspicious patterns.'}
                  </p>
                </div>
              </div>

              <div className="space-y-6">
                <div>
                  <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-500 mb-4 flex items-center gap-2">
                    <CheckCircle className="w-4 h-4" /> Detected Cues (Explainability)
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {result.detected_cues?.length > 0 ? result.detected_cues.map((cue, i) => (
                      <span key={i} className="px-3 py-1 bg-white/5 border border-white/10 rounded-full text-xs text-indigo-300">
                        {cue.type}: {cue.cue}
                      </span>
                    )) : (
                      <p className="text-slate-500 text-sm italic">No suspicious cues identified.</p>
                    )}
                  </div>
                </div>

                <div>
                  <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-500 mb-2 flex items-center gap-2">
                    <Info className="w-4 h-4" /> Extracted Text
                  </h3>
                  <div className="p-4 bg-black/30 rounded-lg border border-white/5 text-sm text-slate-400 max-h-40 overflow-y-auto">
                    {result.full_text}
                  </div>
                </div>
              </div>
            </motion.section>
          ) : (
            <motion.section 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="glass-card p-8 flex flex-col items-center justify-center text-center opacity-50 min-h-[500px]"
            >
              <Shield className="w-16 h-16 text-slate-700 mb-6" />
              <p className="text-slate-500">Awaiting image for analysis...</p>
            </motion.section>
          )}
        </AnimatePresence>
      </div>

      {/* Benefits / Info */}
      <footer className="mt-24 grid grid-cols-1 md:grid-cols-3 gap-8 animate-fade-in" style={{ animationDelay: '0.3s' }}>
        <div className="p-6 glass-card">
          <Shield className="w-6 h-6 text-emerald-400 mb-4" />
          <h4 className="font-bold mb-2">Explainable AI</h4>
          <p className="text-sm text-slate-500">We explain *why* an image is risky by highlighting the triggers.</p>
        </div>
        <div className="p-6 glass-card">
          <Eye className="w-6 h-6 text-indigo-400 mb-4" />
          <h4 className="font-bold mb-2">OCR Powered</h4>
          <p className="text-sm text-slate-500">Uses advanced EasyOCR to read text even from blurry screenshots.</p>
        </div>
        <div className="p-6 glass-card">
          <CheckCircle className="w-6 h-6 text-rose-400 mb-4" />
          <h4 className="font-bold mb-2">Instant Alerts</h4>
          <p className="text-sm text-slate-500">Real-time risk scoring for immediate decision making.</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
