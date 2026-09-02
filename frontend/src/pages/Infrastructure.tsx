import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { InfrastructureNode, Alert } from '../types';
import { Activity, Zap, RefreshCw, CheckCircle, AlertTriangle, ShieldAlert, Play, Cpu, HardDrive } from 'lucide-react';
import { Badge } from '../components/common/Badge';

export const Infrastructure: React.FC = () => {
  const [nodes, setNodes] = useState<InfrastructureNode[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);
  const [isSpiking, setIsSpiking] = useState(false);

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 5000); // 5s live polling
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      const [nData, aData] = await Promise.all([
        api.getInfrastructure(),
        api.getAlerts(),
      ]);
      setNodes(nData);
      setAlerts(aData);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleSimulateSpike = async (hostname: string) => {
    setIsSpiking(true);
    try {
      await api.simulateMetricSpike({
        hostname,
        metric: 'CPU',
        value: 94.5,
      });
      loadData();
    } catch (e) {
      console.error(e);
    } finally {
      setIsSpiking(false);
    }
  };

  const handleNormalize = async (hostname: string) => {
    try {
      await api.normalizeNode(hostname);
      loadData();
    } catch (e) {
      console.error(e);
    }
  };

  const handleAcknowledgeAlert = async (id: number) => {
    try {
      await api.acknowledgeAlert(id);
      loadData();
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <Activity className="w-5 h-5 text-brand-400" />
            <span>Infrastructure Health & Real-time Telemetry</span>
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Monitor host nodes, database clusters, CPU/memory thresholds, and trigger automated alert simulations.
          </p>
        </div>

        <button
          onClick={loadData}
          className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
          title="Refresh"
        >
          <RefreshCw className="w-4 h-4" />
        </button>
      </div>

      {/* Trigger Simulation Card */}
      <div className="bg-gradient-to-r from-red-950/40 via-slate-900 to-amber-950/30 border border-red-500/20 rounded-xl p-4 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <Zap className="w-4 h-4 text-amber-400" />
            <span className="text-xs font-bold text-slate-100 uppercase tracking-wider">Automated Alert Testing Tool</span>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            Inject a 94.5% CPU spike on <strong className="text-slate-200">Database-01</strong> to test automated Alert &rarr; P1 Incident &rarr; AI Diagnostics creation.
          </p>
        </div>

        <div className="flex items-center gap-2 shrink-0">
          <button
            onClick={() => handleSimulateSpike('Database-01')}
            disabled={isSpiking}
            className="bg-red-600 hover:bg-red-500 disabled:bg-slate-800 text-white text-xs font-semibold px-4 py-2 rounded-lg flex items-center gap-1.5 shadow-lg shadow-red-600/30 transition"
          >
            <Play className="w-3.5 h-3.5 fill-white" />
            <span>{isSpiking ? 'Spiking...' : 'Simulate CPU Spike (94%)'}</span>
          </button>
          <button
            onClick={() => handleNormalize('Database-01')}
            className="bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs px-3 py-2 rounded-lg border border-slate-700 transition"
          >
            Normalize Node
          </button>
        </div>
      </div>

      {/* Nodes Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {nodes.map((node) => {
          const isCritical = node.status === 'Critical' || node.cpu_usage >= 90;
          const isWarning = node.status === 'Warning' || (node.cpu_usage >= 75 && node.cpu_usage < 90);
          return (
            <div
              key={node.id}
              className={`rounded-xl p-5 border transition ${
                isCritical
                  ? 'bg-red-950/20 border-red-500/40 glow-red'
                  : isWarning
                  ? 'bg-amber-950/15 border-amber-500/30'
                  : 'bg-slate-900 border-slate-800 hover:border-slate-700'
              }`}
            >
              <div className="flex items-center justify-between mb-3">
                <div>
                  <div className="flex items-center gap-2">
                    <span
                      className={`w-2.5 h-2.5 rounded-full ${
                        isCritical
                          ? 'bg-red-500 animate-ping'
                          : isWarning
                          ? 'bg-amber-400'
                          : 'bg-emerald-400'
                      }`}
                    />
                    <h3 className="text-sm font-bold text-slate-100 truncate">{node.hostname}</h3>
                  </div>
                  <span className="text-[10px] text-slate-500 font-mono">{node.ip_address} • {node.node_type}</span>
                </div>
                <Badge variant={isCritical ? 'p1' : isWarning ? 'p2' : 'success'}>
                  {node.status}
                </Badge>
              </div>

              {/* Progress Bars */}
              <div className="space-y-2.5 text-xs font-mono">
                <div>
                  <div className="flex justify-between text-[11px] mb-1">
                    <span className="text-slate-400">CPU LOAD</span>
                    <span className={`font-bold ${node.cpu_usage >= 90 ? 'text-red-400' : 'text-slate-200'}`}>
                      {node.cpu_usage.toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden border border-slate-800">
                    <div
                      className={`h-full rounded-full transition-all duration-500 ${
                        node.cpu_usage >= 90
                          ? 'bg-red-500'
                          : node.cpu_usage >= 75
                          ? 'bg-amber-400'
                          : 'bg-emerald-500'
                      }`}
                      style={{ width: `${Math.min(100, node.cpu_usage)}%` }}
                    />
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-[11px] mb-1">
                    <span className="text-slate-400">MEMORY UTIL</span>
                    <span className="text-slate-200 font-bold">{node.memory_usage.toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden border border-slate-800">
                    <div
                      className="bg-indigo-500 h-full rounded-full transition-all duration-500"
                      style={{ width: `${Math.min(100, node.memory_usage)}%` }}
                    />
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2 mt-4 pt-3 border-t border-slate-800/80 text-[11px] font-mono text-slate-400">
                <div>Latency: <span className="text-slate-200 font-bold">{node.response_time_ms.toFixed(1)}ms</span></div>
                <div>Uptime: <span className="text-emerald-400 font-bold">{node.uptime_percentage}%</span></div>
              </div>

              {isCritical && (
                <div className="mt-3 pt-2 border-t border-red-500/30 flex items-center justify-between">
                  <span className="text-[10px] text-red-400 font-bold animate-pulse">THRESHOLD EXCEEDED (&gt;90%)</span>
                  <button
                    onClick={() => handleNormalize(node.hostname)}
                    className="text-[10px] bg-slate-800 hover:bg-slate-700 text-slate-200 px-2 py-1 rounded"
                  >
                    Reset Metric
                  </button>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Active Alerts Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
        <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
          <ShieldAlert className="w-4 h-4 text-amber-400" />
          <span>Automated Infrastructure Alerts Stream</span>
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 font-semibold uppercase text-[10px]">
                <th className="pb-2">Alert ID</th>
                <th className="pb-2">Target Node</th>
                <th className="pb-2">Metric Breach</th>
                <th className="pb-2">Severity</th>
                <th className="pb-2">Linked Incident</th>
                <th className="pb-2">Message</th>
                <th className="pb-2 text-right">Acknowledge</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {alerts.length === 0 ? (
                <tr>
                  <td colSpan={7} className="text-center py-6 text-slate-500 italic">No active alerts.</td>
                </tr>
              ) : (
                alerts.map((a) => (
                  <tr key={a.id} className="hover:bg-slate-800/40">
                    <td className="py-2.5 font-mono font-bold text-brand-400">{a.alert_code}</td>
                    <td className="py-2.5 font-semibold text-slate-200">{a.resource_name}</td>
                    <td className="py-2.5 font-mono text-red-400 font-bold">
                      {a.metric_name} ({a.metric_value.toFixed(1)}% &gt; {a.threshold_value}%)
                    </td>
                    <td className="py-2.5">
                      <Badge variant={a.severity === 'Critical' ? 'p1' : 'p2'}>{a.severity}</Badge>
                    </td>
                    <td className="py-2.5 font-mono text-indigo-300">{a.incident_number || 'Auto Logged'}</td>
                    <td className="py-2.5 text-slate-400 text-[11px] max-w-[200px] truncate">{a.message}</td>
                    <td className="py-2.5 text-right">
                      {a.is_acknowledged ? (
                        <span className="text-slate-500 text-[11px]">Acked</span>
                      ) : (
                        <button
                          onClick={() => handleAcknowledgeAlert(a.id)}
                          className="text-[11px] bg-slate-800 hover:bg-slate-700 text-slate-200 px-2.5 py-1 rounded"
                        >
                          Ack
                        </button>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
