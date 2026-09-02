import React, { useState, useEffect } from 'react';
import { Modal } from '../common/Modal';
import { api } from '../../services/api';
import {
  Play,
  RotateCcw,
  CheckCircle2,
  AlertOctagon,
  Sparkles,
  GitBranch,
  Terminal,
  Activity,
  Layers,
  ArrowRight,
  ChevronRight,
  ShieldAlert
} from 'lucide-react';
import { Badge } from '../common/Badge';

interface ScenarioSimulationModalProps {
  isOpen: boolean;
  onClose: () => void;
  onScenarioCompleted?: () => void;
}

export const ScenarioSimulationModal: React.FC<ScenarioSimulationModalProps> = ({
  isOpen,
  onClose,
  onScenarioCompleted,
}) => {
  const [steps, setSteps] = useState<any[]>([]);
  const [currentStepIndex, setCurrentStepIndex] = useState<number>(0);
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [logs, setLogs] = useState<string[]>([]);
  const [activeTab, setActiveTab] = useState<'timeline' | 'architecture' | 'logs'>('timeline');

  useEffect(() => {
    if (isOpen) {
      loadSteps();
    }
  }, [isOpen]);

  const loadSteps = async () => {
    try {
      const data = await api.getScenarioSteps();
      setSteps(data.steps || []);
    } catch (e) {
      console.error(e);
    }
  };

  const handleStepExecute = async (index: number) => {
    if (index >= steps.length) return;
    const step = steps[index];
    try {
      const res = await api.executeScenarioStep(step.step);
      const timestamp = new Date().toLocaleTimeString();
      setLogs((prev) => [
        `[${timestamp}] Step ${step.step} (${step.phase}): ${res.message || step.title}`,
        ...prev,
      ]);
      setCurrentStepIndex(index + 1);
    } catch (e) {
      console.error(e);
    }
  };

  const handleAutoRun = async () => {
    setIsRunning(true);
    let idx = currentStepIndex;
    while (idx < steps.length) {
      await handleStepExecute(idx);
      idx++;
      await new Promise((r) => setTimeout(r, 700)); // Smooth step animation
    }
    setIsRunning(false);
    if (onScenarioCompleted) onScenarioCompleted();
  };

  const handleReset = async () => {
    try {
      await api.resetScenario();
      setCurrentStepIndex(0);
      setLogs([`[${new Date().toLocaleTimeString()}] Scenario reset to initial state.`]);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Critical Database Failure & DevOps Resolution (INC-1025)"
      maxWidth="4xl"
    >
      <div className="space-y-4">
        {/* Scenario Header Info */}
        <div className="bg-gradient-to-r from-red-950/40 via-slate-900 to-indigo-950/40 border border-red-500/20 rounded-xl p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <Badge variant="p1" className="animate-pulse">CRITICAL END-TO-END SCENARIO</Badge>
              <span className="text-xs font-mono text-slate-400">INC-1025 • Database-01</span>
            </div>
            <h4 className="text-sm font-bold text-slate-100 mt-1">
              Infrastructure Spike → AI Diagnostics → Jira Sync → CI/CD Deployment → Zero-Downtime Recovery
            </h4>
            <p className="text-xs text-slate-400 mt-0.5">
              Demonstrating the full 23-step workflow combining ITSM, AI RCA, Jira, GitHub, Jenkins & Docker.
            </p>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            <button
              onClick={handleAutoRun}
              disabled={isRunning || currentStepIndex >= steps.length}
              className="bg-red-600 hover:bg-red-500 disabled:bg-slate-800 disabled:text-slate-500 text-white text-xs font-semibold px-4 py-2 rounded-lg flex items-center gap-2 shadow-lg shadow-red-600/30 transition"
            >
              <Play className="w-3.5 h-3.5" />
              <span>{isRunning ? 'Executing...' : 'Auto-Run Scenario'}</span>
            </button>
            <button
              onClick={handleReset}
              disabled={isRunning}
              className="bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs px-3 py-2 rounded-lg flex items-center gap-1.5 border border-slate-700 transition"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Reset</span>
            </button>
          </div>
        </div>

        {/* Progress Bar */}
        <div>
          <div className="flex justify-between text-xs text-slate-400 mb-1 font-mono">
            <span>Progress: Step {currentStepIndex} of {steps.length}</span>
            <span>{Math.round((currentStepIndex / (steps.length || 1)) * 100)}% Completed</span>
          </div>
          <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
            <div
              className="bg-gradient-to-r from-red-500 via-amber-500 to-emerald-500 h-full transition-all duration-300"
              style={{ width: `${(currentStepIndex / (steps.length || 1)) * 100}%` }}
            />
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex border-b border-slate-800 text-xs font-medium">
          <button
            onClick={() => setActiveTab('timeline')}
            className={`px-4 py-2 border-b-2 transition ${
              activeTab === 'timeline'
                ? 'border-brand-500 text-brand-400 font-semibold'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            23-Step Interactive Timeline
          </button>
          <button
            onClick={() => setActiveTab('architecture')}
            className={`px-4 py-2 border-b-2 transition ${
              activeTab === 'architecture'
                ? 'border-brand-500 text-brand-400 font-semibold'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            DevOps & ITSM Ecosystem Architecture
          </button>
          <button
            onClick={() => setActiveTab('logs')}
            className={`px-4 py-2 border-b-2 transition ${
              activeTab === 'logs'
                ? 'border-brand-500 text-brand-400 font-semibold'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            Execution Logs ({logs.length})
          </button>
        </div>

        {/* Timeline View */}
        {activeTab === 'timeline' && (
          <div className="max-h-96 overflow-y-auto pr-2 space-y-2">
            {steps.map((s, idx) => {
              const isPast = idx < currentStepIndex;
              const isCurrent = idx === currentStepIndex;
              return (
                <div
                  key={s.step}
                  className={`p-3 rounded-xl border text-xs transition flex items-start gap-3 ${
                    isPast
                      ? 'bg-emerald-950/20 border-emerald-500/30 text-slate-300'
                      : isCurrent
                      ? 'bg-brand-950/40 border-brand-500 text-white shadow-md shadow-brand-500/10 scale-[1.01]'
                      : 'bg-slate-900/50 border-slate-800 text-slate-500'
                  }`}
                >
                  <div className="mt-0.5 shrink-0">
                    {isPast ? (
                      <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    ) : isCurrent ? (
                      <div className="w-4 h-4 rounded-full border-2 border-brand-400 flex items-center justify-center animate-spin">
                        <div className="w-1.5 h-1.5 bg-brand-400 rounded-full" />
                      </div>
                    ) : (
                      <div className="w-4 h-4 rounded-full border border-slate-700 flex items-center justify-center text-[9px] font-mono">
                        {s.step}
                      </div>
                    )}
                  </div>

                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-[10px] uppercase font-bold text-slate-400">{s.phase}</span>
                      <span className="font-semibold text-slate-200">{s.title}</span>
                    </div>
                    <p className="text-[11px] text-slate-400 mt-0.5">{s.detail}</p>
                  </div>

                  {isCurrent && (
                    <button
                      onClick={() => handleStepExecute(idx)}
                      className="shrink-0 bg-brand-600 hover:bg-brand-500 text-white text-[11px] font-semibold px-2.5 py-1 rounded shadow"
                    >
                      Execute Step
                    </button>
                  )}
                </div>
              );
            })}
          </div>
        )}

        {/* Architecture Diagram View */}
        {activeTab === 'architecture' && (
          <div className="bg-slate-950 rounded-xl p-4 border border-slate-800 text-xs font-mono space-y-3">
            <div className="text-brand-400 font-bold">INTEGRATED INCIDENT RESOLUTION LIFECYCLE</div>
            <div className="grid grid-cols-1 sm:grid-cols-4 gap-2 text-center">
              <div className="p-2.5 rounded bg-slate-900 border border-red-500/30">
                <div className="text-red-400 font-bold mb-1">1. MONITOR</div>
                <p className="text-[10px] text-slate-400">Database-01 CPU &gt; 90%</p>
                <p className="text-[10px] text-slate-400">ALT-94201 Critical</p>
              </div>
              <div className="p-2.5 rounded bg-slate-900 border border-purple-500/30">
                <div className="text-purple-400 font-bold mb-1">2. AI ANALYZE</div>
                <p className="text-[10px] text-slate-400">INC-1025 (P1)</p>
                <p className="text-[10px] text-slate-400">96.5% Confidence RCA</p>
              </div>
              <div className="p-2.5 rounded bg-slate-900 border border-blue-500/30">
                <div className="text-blue-400 font-bold mb-1">3. JIRA & DEVOPS</div>
                <p className="text-[10px] text-slate-400">Jira ITSM-245</p>
                <p className="text-[10px] text-slate-400">GitHub Commit e9a1b42</p>
              </div>
              <div className="p-2.5 rounded bg-slate-900 border border-emerald-500/30">
                <div className="text-emerald-400 font-bold mb-1">4. DEPLOY & RESOLVE</div>
                <p className="text-[10px] text-slate-400">Jenkins Build #129</p>
                <p className="text-[10px] text-slate-400">CPU 28.4% (Recovered)</p>
              </div>
            </div>
            <div className="p-3 bg-slate-900/60 rounded border border-slate-800 text-slate-300 text-[11px] leading-relaxed">
              <p><span className="text-indigo-400 font-semibold">Value Proposition:</span> Transforms disconnected IT alerts into an automated, AI-assisted resolution pipeline with full enterprise traceability from infrastructure telemetry to production container deployment.</p>
            </div>
          </div>
        )}

        {/* Execution Logs */}
        {activeTab === 'logs' && (
          <div className="bg-slate-950 rounded-xl p-3 border border-slate-800 font-mono text-[11px] text-emerald-400 max-h-80 overflow-y-auto space-y-1">
            {logs.length === 0 ? (
              <p className="text-slate-500">No execution logs yet. Click "Auto-Run Scenario" or "Execute Step".</p>
            ) : (
              logs.map((log, i) => (
                <div key={i} className="leading-relaxed">
                  {log}
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </Modal>
  );
};
