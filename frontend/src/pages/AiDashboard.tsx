import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import {
  Sparkles,
  Bot,
  Brain,
  AlertOctagon,
  CheckCircle2,
  TrendingUp,
  Activity,
  Layers,
  Search,
  ExternalLink,
  ArrowRight
} from 'lucide-react';
import { Badge } from '../components/common/Badge';
import { AiDiagnosticDrawer } from '../components/ai/AiDiagnosticDrawer';

export const AiDashboard: React.FC = () => {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAiStats();
  }, []);

  const loadAiStats = async () => {
    try {
      const data = await api.getAIDashboardStats();
      setStats(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  if (loading || !stats) {
    return (
      <div className="flex items-center justify-center h-96 text-slate-400">
        <div className="flex items-center gap-3">
          <div className="w-5 h-5 border-2 border-brand-500 border-t-transparent rounded-full animate-spin"></div>
          <span>Loading AI Operations Telemetry...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 pb-12">
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-950/60 via-purple-950/40 to-slate-900 border border-indigo-500/30 rounded-2xl p-6 shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
              <Brain className="w-6 h-6 text-indigo-400" />
              <span>AI Operations & Predictive Resolution Hub</span>
            </h2>
            <Badge variant="p4">v2.4 Cognitive Engine</Badge>
          </div>
          <p className="text-xs text-slate-400 mt-1 max-w-2xl">
            Machine intelligence telemetry parsing, automatic category classification, probability matrix root cause analysis, and proactive anomaly detection.
          </p>
        </div>
      </div>

      {/* AI Metric Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3.5">
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
          <span className="text-xs font-medium text-slate-400 block mb-1">Incidents Analyzed</span>
          <div className="text-2xl font-bold font-mono text-white">{stats.incidents_analyzed}</div>
          <span className="text-[10px] text-emerald-400 mt-1 flex items-center gap-1">
            <TrendingUp className="w-3 h-3" /> 100% ingest rate
          </span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
          <span className="text-xs font-medium text-slate-400 block mb-1">Auto-Classified</span>
          <div className="text-2xl font-bold font-mono text-indigo-400">{stats.auto_classified}</div>
          <span className="text-[10px] text-slate-400 mt-1">10 domain categories</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
          <span className="text-xs font-medium text-slate-400 block mb-1">Recommendations</span>
          <div className="text-2xl font-bold font-mono text-purple-400">{stats.resolution_recommendations}</div>
          <span className="text-[10px] text-slate-400 mt-1">Action checklists generated</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
          <span className="text-xs font-medium text-slate-400 block mb-1">High Confidence (&gt;90%)</span>
          <div className="text-2xl font-bold font-mono text-emerald-400">{stats.high_confidence_recommendations}</div>
          <span className="text-[10px] text-slate-400 mt-1">Avg Score: {stats.average_confidence}%</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
          <span className="text-xs font-medium text-slate-400 block mb-1">Recurring Problem Candidates</span>
          <div className="text-2xl font-bold font-mono text-amber-400">{stats.potential_recurring_problems}</div>
          <span className="text-[10px] text-amber-400 mt-1">Pattern clustering active</span>
        </div>
      </div>

      {/* Main Grid: Interactive AI Diagnostic Drawer + AI Pattern Insights */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left 7 cols: Interactive Assistant */}
        <div className="lg:col-span-7 space-y-6">
          <AiDiagnosticDrawer />
        </div>

        {/* Right 5 cols: Pattern Insights & Category Breakdown */}
        <div className="lg:col-span-5 space-y-6">
          {/* AI Pattern Insights */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
            <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-indigo-400" />
              <span>Proactive Telemetry Anomaly Insights</span>
            </h3>

            <div className="space-y-3">
              {stats.recent_ai_insights.map((item: any) => (
                <div key={item.id} className="bg-slate-950 p-3.5 rounded-xl border border-slate-800/80 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-slate-200">{item.title}</span>
                    <Badge variant="warning">{item.confidence}% Match</Badge>
                  </div>
                  <p className="text-[11px] text-slate-400 leading-relaxed font-mono bg-slate-900/80 p-2 rounded border border-slate-800/50">
                    {item.pattern}
                  </p>
                  <div className="text-[11px] text-indigo-300 bg-indigo-950/30 p-2 rounded border border-indigo-500/20">
                    <span className="font-semibold text-indigo-200">Recommended RCA: </span>
                    {item.recommendation}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Category Classification Breakdown */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <h3 className="text-sm font-bold text-slate-100 mb-3">AI Category Classification Matrix</h3>
            <div className="grid grid-cols-2 gap-2 text-xs">
              {Object.entries(stats.category_distribution).map(([cat, count]: [string, any]) => (
                <div key={cat} className="bg-slate-950 p-2.5 rounded-lg border border-slate-800 flex items-center justify-between">
                  <span className="text-slate-300">{cat}</span>
                  <span className="font-mono font-bold text-brand-400">{count}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
