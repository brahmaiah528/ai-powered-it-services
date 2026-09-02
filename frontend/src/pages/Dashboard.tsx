import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import {
  AlertTriangle,
  CheckCircle,
  Clock,
  Activity,
  Server,
  ShieldAlert,
  ArrowUpRight,
  TrendingUp,
  Sparkles,
  ExternalLink,
  ChevronRight,
  Play
} from 'lucide-react';
import { Badge } from '../components/common/Badge';

interface DashboardProps {
  onNavigateTab: (tab: string) => void;
  onOpenIncidentDetail: (id: number) => void;
  onOpenSimulation: () => void;
}

export const Dashboard: React.FC<DashboardProps> = ({
  onNavigateTab,
  onOpenIncidentDetail,
  onOpenSimulation,
}) => {
  const [data, setData] = useState<any>(null);
  const [recentIncidents, setRecentIncidents] = useState<any[]>([]);
  const [infraNodes, setInfraNodes] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
    const interval = setInterval(loadDashboardData, 8000); // 8s live refresh
    return () => clearInterval(interval);
  }, []);

  const loadDashboardData = async () => {
    try {
      const [kpiRes, incRes, infraRes] = await Promise.all([
        api.getDashboardKPIs(),
        api.getIncidents({}),
        api.getInfrastructure(),
      ]);
      setData(kpiRes);
      setRecentIncidents(incRes.slice(0, 6));
      setInfraNodes(infraRes.slice(0, 6));
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  if (loading || !data) {
    return (
      <div className="flex items-center justify-center h-96 text-slate-400">
        <div className="flex items-center gap-3">
          <div className="w-5 h-5 border-2 border-brand-500 border-t-transparent rounded-full animate-spin"></div>
          <span>Loading IT Operations Telemetry...</span>
        </div>
      </div>
    );
  }

  const { kpis, charts } = data;

  return (
    <div className="space-y-6 pb-12">
      {/* Top Banner & Scenario Launcher */}
      <div className="bg-gradient-to-r from-slate-900 via-brand-950/40 to-slate-900 border border-slate-800 rounded-2xl p-5 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-lg font-bold text-white tracking-tight">Enterprise IT Operations Command Center</h2>
            <Badge variant="info">Live Telemetry</Badge>
          </div>
          <p className="text-xs text-slate-400 mt-1 max-w-2xl">
            Real-time infrastructure health, AI-powered root cause analysis, SLA compliance tracking, and automated DevOps synchronization.
          </p>
        </div>

        <div className="flex items-center gap-3 shrink-0">
          <button
            onClick={onOpenSimulation}
            className="bg-gradient-to-r from-red-600 to-amber-600 hover:from-red-500 hover:to-amber-500 text-white text-xs font-semibold px-4 py-2.5 rounded-xl flex items-center gap-2 shadow-lg shadow-red-600/30 transition transform hover:-translate-y-0.5"
          >
            <Play className="w-4 h-4 text-white fill-white animate-pulse" />
            <span>Demonstrate Critical DB Scenario</span>
          </button>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3.5">
        <div className="glass-panel p-4 rounded-xl border border-slate-800 flex flex-col justify-between">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-medium">Total Incidents</span>
            <AlertTriangle className="w-4 h-4 text-slate-400" />
          </div>
          <div className="text-2xl font-extrabold text-white font-mono">{kpis.total_incidents}</div>
          <span className="text-[10px] text-slate-400 mt-1">30 active in catalog</span>
        </div>

        <div className="glass-panel p-4 rounded-xl border border-slate-800 flex flex-col justify-between">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-medium">Open Tickets</span>
            <Clock className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-extrabold text-amber-400 font-mono">{kpis.open_incidents}</div>
          <span className="text-[10px] text-slate-400 mt-1">In triage & progress</span>
        </div>

        <div className="glass-panel p-4 rounded-xl border border-red-500/20 bg-red-950/10 flex flex-col justify-between">
          <div className="flex items-center justify-between text-red-400 mb-2">
            <span className="text-xs font-medium">Critical (P1)</span>
            <ShieldAlert className="w-4 h-4 text-red-400 animate-pulse" />
          </div>
          <div className="text-2xl font-extrabold text-red-400 font-mono">{kpis.critical_incidents}</div>
          <span className="text-[10px] text-red-400/80 mt-1">Requires immediate action</span>
        </div>

        <div className="glass-panel p-4 rounded-xl border border-slate-800 flex flex-col justify-between">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-medium">SLA Compliance</span>
            <CheckCircle className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-extrabold text-emerald-400 font-mono">{kpis.sla_compliance_rate}%</div>
          <span className="text-[10px] text-slate-400 mt-1">{kpis.sla_breaches} breaches recorded</span>
        </div>

        <div className="glass-panel p-4 rounded-xl border border-slate-800 flex flex-col justify-between">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-medium">Avg MTTR</span>
            <Activity className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-2xl font-extrabold text-indigo-400 font-mono">{kpis.avg_resolution_time_min}m</div>
          <span className="text-[10px] text-slate-400 mt-1">Mean Time To Resolution</span>
        </div>

        <div className="glass-panel p-4 rounded-xl border border-slate-800 flex flex-col justify-between">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-medium">System Uptime</span>
            <Server className="w-4 h-4 text-blue-400" />
          </div>
          <div className="text-2xl font-extrabold text-blue-400 font-mono">{kpis.system_availability_percent}%</div>
          <span className="text-[10px] text-slate-400 mt-1">10 nodes monitored</span>
        </div>
      </div>

      {/* Main Grid: Priority / Category breakdown & Infrastructure Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Recent Incidents & Priority Breakdown */}
        <div className="lg:col-span-2 space-y-6">
          {/* Priority Matrix Distribution */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-sm font-bold text-slate-100">Incident Distribution by Priority</h3>
                <p className="text-xs text-slate-400">Calculated dynamically: Impact × Urgency</p>
              </div>
              <button
                onClick={() => onNavigateTab('incidents')}
                className="text-xs text-brand-400 hover:text-brand-300 flex items-center gap-1 font-medium"
              >
                View all incidents <ChevronRight className="w-3.5 h-3.5" />
              </button>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {charts.priority_breakdown.map((p: any) => (
                <div key={p.name} className="bg-slate-950 p-3.5 rounded-xl border border-slate-800/80">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs font-semibold text-slate-300">{p.name}</span>
                    <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: p.color }} />
                  </div>
                  <div className="text-xl font-bold font-mono text-slate-100">{p.value}</div>
                  <div className="w-full bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
                    <div
                      className="h-full rounded-full"
                      style={{
                        width: `${Math.max(10, (p.value / kpis.total_incidents) * 100)}%`,
                        backgroundColor: p.color,
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Active Incidents Table */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-sm font-bold text-slate-100">Recent Incident Stream & AI Classification</h3>
                <p className="text-xs text-slate-400">Live ITIL Incident records</p>
              </div>
              <button
                onClick={() => onNavigateTab('incidents')}
                className="text-xs text-brand-400 hover:text-brand-300 font-medium"
              >
                Full Incident Queue
              </button>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400 font-semibold uppercase text-[10px]">
                    <th className="pb-2">Incident ID</th>
                    <th className="pb-2">Summary</th>
                    <th className="pb-2">Category</th>
                    <th className="pb-2">Priority</th>
                    <th className="pb-2">Status</th>
                    <th className="pb-2">Jira Key</th>
                    <th className="pb-2 text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {recentIncidents.map((inc) => (
                    <tr key={inc.id} className="hover:bg-slate-800/40 transition">
                      <td className="py-2.5 font-mono font-bold text-brand-400">{inc.incident_number}</td>
                      <td className="py-2.5 text-slate-200 font-medium max-w-[220px] truncate">{inc.title}</td>
                      <td className="py-2.5 text-slate-400">{inc.category}</td>
                      <td className="py-2.5">
                        <Badge variant={inc.priority.toLowerCase() as any}>{inc.priority}</Badge>
                      </td>
                      <td className="py-2.5">
                        <Badge variant={inc.status === 'Resolved' ? 'success' : inc.status === 'New' ? 'warning' : 'neutral'}>
                          {inc.status}
                        </Badge>
                      </td>
                      <td className="py-2.5 font-mono text-[11px] text-indigo-300">
                        {inc.jira_issue_key || '—'}
                      </td>
                      <td className="py-2.5 text-right">
                        <button
                          onClick={() => onOpenIncidentDetail(inc.id)}
                          className="text-brand-400 hover:text-brand-300 font-medium text-[11px] hover:underline"
                        >
                          Details
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Right 1 Col: Infrastructure Telemetry Health & AI Insights */}
        <div className="space-y-6">
          {/* Infrastructure Health Status */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-sm font-bold text-slate-100 flex items-center gap-1.5">
                  <Activity className="w-4 h-4 text-emerald-400" />
                  <span>Infrastructure Telemetry</span>
                </h3>
                <p className="text-xs text-slate-400">Server & DB cluster status</p>
              </div>
              <button
                onClick={() => onNavigateTab('infrastructure')}
                className="text-xs text-brand-400 hover:text-brand-300 font-medium"
              >
                All Nodes
              </button>
            </div>

            <div className="space-y-2.5">
              {infraNodes.map((node) => (
                <div
                  key={node.id}
                  className="bg-slate-950 p-2.5 rounded-lg border border-slate-800/80 flex items-center justify-between text-xs"
                >
                  <div className="flex items-center gap-2.5">
                    <span
                      className={`w-2.5 h-2.5 rounded-full shrink-0 ${
                        node.status === 'Healthy'
                          ? 'bg-emerald-400'
                          : node.status === 'Warning'
                          ? 'bg-amber-400 animate-pulse'
                          : 'bg-red-500 animate-pulse'
                      }`}
                    />
                    <div>
                      <span className="font-semibold text-slate-200 block truncate max-w-[140px]">{node.hostname}</span>
                      <span className="text-[10px] text-slate-500 font-mono">{node.ip_address}</span>
                    </div>
                  </div>

                  <div className="text-right font-mono text-[11px]">
                    <div className="text-slate-300">CPU: <span className="font-bold">{node.cpu_usage.toFixed(1)}%</span></div>
                    <div className="text-slate-400 text-[10px]">Mem: {node.memory_usage.toFixed(1)}%</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* AI Diagnostic Highlights */}
          <div className="bg-gradient-to-b from-indigo-950/40 to-slate-900 border border-indigo-500/20 rounded-xl p-5 space-y-3">
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-indigo-400" />
              <h3 className="text-sm font-bold text-slate-100">AI Diagnostic Intelligence</h3>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              Auto-diagnosed <span className="text-indigo-300 font-bold">231 incidents</span> with 93.4% average recommendation confidence score.
            </p>
            <div className="bg-slate-950/60 p-3 rounded-lg border border-indigo-500/20 text-xs">
              <span className="font-semibold text-amber-300 block mb-1">Potential Recurring Problem:</span>
              <p className="text-slate-400 text-[11px]">
                Database-01 connection lock contention during bulk nightly reconciliation jobs (Linked: INC-1001, INC-1007, INC-1025).
              </p>
            </div>
            <button
              onClick={() => onNavigateTab('ai-assistant')}
              className="w-full bg-brand-600/20 hover:bg-brand-600/30 text-brand-300 border border-brand-500/30 text-xs font-semibold py-2 rounded-lg transition text-center"
            >
              Open AI Operations Hub
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
