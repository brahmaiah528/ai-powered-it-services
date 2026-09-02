import React, { useState } from 'react';
import { Sparkles, Bot, AlertTriangle, CheckCircle2, BookOpen, Clock, ArrowRight, ShieldAlert } from 'lucide-react';
import { api } from '../../services/api';
import { AIAnalysisResult } from '../../types';
import { Badge } from '../common/Badge';

interface AiDiagnosticDrawerProps {
  initialTitle?: string;
  initialDescription?: string;
  onApplyDiagnosis?: (result: AIAnalysisResult) => void;
}

export const AiDiagnosticDrawer: React.FC<AiDiagnosticDrawerProps> = ({
  initialTitle = '',
  initialDescription = '',
  onApplyDiagnosis,
}) => {
  const [title, setTitle] = useState(initialTitle);
  const [description, setDescription] = useState(initialDescription);
  const [impact, setImpact] = useState('High');
  const [urgency, setUrgency] = useState('High');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<AIAnalysisResult | null>(null);

  const handleAnalyze = async () => {
    if (!title && !description) return;
    setIsLoading(true);
    try {
      const data = await api.analyzeIncidentAI({
        title,
        description,
        impact,
        urgency,
      });
      setResult(data);
      if (onApplyDiagnosis) onApplyDiagnosis(data);
    } catch (e) {
      console.error('AI diagnosis error:', e);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-indigo-500 to-purple-500 flex items-center justify-center text-white shadow-md shadow-indigo-500/20">
            <Sparkles className="w-4 h-4" />
          </div>
          <div>
            <h4 className="text-sm font-bold text-slate-100 flex items-center gap-1.5">
              AI Incident Resolution Assistant
              <span className="text-[10px] font-mono bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 px-1.5 py-0.5 rounded">v2.4 Engine</span>
            </h4>
            <p className="text-[11px] text-slate-400">Classify, diagnose, calculate priority, and generate resolution runbooks</p>
          </div>
        </div>
      </div>

      {/* Input controls */}
      <div className="space-y-3">
        <div>
          <label className="text-[11px] font-medium text-slate-300 block mb-1">Incident Title / Summary</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="e.g. Employees cannot access corporate email"
            className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-brand-500"
          />
        </div>

        <div>
          <label className="text-[11px] font-medium text-slate-300 block mb-1">Incident Description & Error Logs</label>
          <textarea
            rows={3}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="e.g. Users receiving HTTP 401 error during Exchange hybrid token authentication. MX records indicate rate limiting."
            className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-brand-500"
          />
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="text-[11px] font-medium text-slate-300 block mb-1">Impact Level</label>
            <select
              value={impact}
              onChange={(e) => setImpact(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-brand-500"
            >
              <option value="High">High (Organization Wide)</option>
              <option value="Medium">Medium (Department)</option>
              <option value="Low">Low (Individual User)</option>
            </select>
          </div>
          <div>
            <label className="text-[11px] font-medium text-slate-300 block mb-1">Urgency Level</label>
            <select
              value={urgency}
              onChange={(e) => setUrgency(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-brand-500"
            >
              <option value="High">High (Immediate Critical)</option>
              <option value="Medium">Medium (Workaround Available)</option>
              <option value="Low">Low (Minor Non-Blocking)</option>
            </select>
          </div>
        </div>

        <button
          onClick={handleAnalyze}
          disabled={isLoading || (!title && !description)}
          className="w-full bg-gradient-to-r from-brand-600 to-indigo-600 hover:from-brand-500 hover:to-indigo-500 disabled:bg-slate-800 disabled:text-slate-500 text-white text-xs font-semibold py-2 rounded-lg flex items-center justify-center gap-2 shadow-lg shadow-brand-600/20 transition"
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span>{isLoading ? 'Running AI Diagnostic Engine...' : 'Run AI Diagnostic Analysis'}</span>
        </button>
      </div>

      {/* AI Diagnostic Output */}
      {result && (
        <div className="mt-4 p-4 rounded-xl bg-slate-950 border border-indigo-500/30 space-y-3 animate-fadeIn">
          <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800/80 pb-2.5">
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-400">Classified Category:</span>
              <Badge variant="info">{result.suggested_category}</Badge>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-400">Calculated Priority:</span>
              <Badge variant={result.calculated_priority.toLowerCase() as any}>
                {result.calculated_priority} ({result.calculated_priority === 'P1' ? 'Critical' : result.calculated_priority === 'P2' ? 'High' : result.calculated_priority === 'P3' ? 'Medium' : 'Low'})
              </Badge>
            </div>
            <div className="flex items-center gap-1.5 text-xs font-mono text-emerald-400">
              <span>Confidence:</span>
              <span className="font-bold">{result.confidence_score}%</span>
            </div>
          </div>

          <div>
            <span className="text-[11px] font-bold text-slate-300 uppercase tracking-wider block mb-1">Probable Cause:</span>
            <p className="text-xs text-slate-200 bg-slate-900 p-2.5 rounded-lg border border-slate-800 font-medium">
              {result.probable_cause}
            </p>
          </div>

          <div>
            <span className="text-[11px] font-bold text-slate-300 uppercase tracking-wider block mb-1">Recommended Actions:</span>
            <div className="space-y-1.5">
              {result.recommended_actions.map((act, i) => (
                <div key={i} className="flex items-start gap-2 text-xs text-slate-300 bg-slate-900/60 p-2 rounded border border-slate-800/50">
                  <span className="w-4 h-4 rounded-full bg-brand-500/20 text-brand-400 font-mono text-[10px] font-bold flex items-center justify-center shrink-0 mt-0.5">
                    {i + 1}
                  </span>
                  <span>{act}</span>
                </div>
              ))}
            </div>
          </div>

          {result.relevant_kb_articles.length > 0 && (
            <div>
              <span className="text-[11px] font-bold text-slate-300 uppercase tracking-wider block mb-1">Relevant Knowledge Articles:</span>
              <div className="grid grid-cols-1 gap-1.5">
                {result.relevant_kb_articles.map((kb) => (
                  <div key={kb.article_number} className="text-xs bg-slate-900 p-2 rounded border border-slate-800 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <BookOpen className="w-3.5 h-3.5 text-indigo-400" />
                      <span className="font-mono text-indigo-300">{kb.article_number}:</span>
                      <span className="text-slate-200 truncate max-w-[280px]">{kb.title}</span>
                    </div>
                    <span className="text-[10px] text-slate-400">{kb.category}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="pt-2 border-t border-slate-800/60 text-[10px] text-slate-500 italic">
            {result.disclaimer}
          </div>
        </div>
      )}
    </div>
  );
};
