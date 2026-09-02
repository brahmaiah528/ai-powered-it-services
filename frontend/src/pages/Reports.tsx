import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import {
  BarChart3,
  Download,
  Calendar,
  CheckCircle2,
  Clock,
  AlertTriangle,
  TrendingUp,
  FileSpreadsheet
} from 'lucide-react';
import { Badge } from '../components/common/Badge';

export const Reports: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = async () => {
    setLoading(true);
    try {
      const res = await api.getDashboardKPIs();
      setData(res);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleExportCSV = () => {
    window.open(api.exportCSVUrl, '_blank');
  };

  if (loading || !data) {
    return (
      <div className="flex items-center justify-center h-96 text-slate-400">
        <div className="flex items-center gap-3">
          <div className="w-5 h-5 border-2 border-brand-500 border-t-transparent rounded-full animate-spin"></div>
          <span>Generating Operational Reports...</span>
        </div>
      </div>
    );
  }

  const { kpis, charts } = data;

  return (
    <div className="space-y-6 pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-brand-400" />
            <span>Operational SLA & Incident Intelligence Reports</span>
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Audit compliance, SLA adherence rates, Mean Time To Resolution (MTTR), and department breakdowns.
          </p>
        </div>

        <button
          onClick={handleExportCSV}
          className="bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold px-4 py-2 rounded-lg flex items-center gap-2 shadow-md shadow-emerald-600/20 transition"
        >
          <Download className="w-4 h-4" />
          <span>Export Full CSV Report</span>
        </button>
      </div>

      {/* KPI Overview */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
          <span className="text-xs text-slate-400 block mb-1">SLA Compliance Rate</span>
          <div className="text-2xl font-bold font-mono text-emerald-400">{kpis.sla_compliance_rate}%</div>
          <span className="text-[10px] text-slate-400 mt-1">Enterprise Target: &gt;95.0%</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
          <span className="text-xs text-slate-400 block mb-1">Average Resolution MTTR</span>
          <div className="text-2xl font-bold font-mono text-indigo-400">{kpis.avg_resolution_time_min}m</div>
          <span className="text-[10px] text-slate-400 mt-1">Mean Time To Resolution</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
          <span className="text-xs text-slate-400 block mb-1">Resolved Tickets</span>
          <div className="text-2xl font-bold font-mono text-white">{kpis.resolved_today}</div>
          <span className="text-[10px] text-slate-400 mt-1">Successfully closed</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
          <span className="text-xs text-slate-400 block mb-1">SLA Breaches</span>
          <div className="text-2xl font-bold font-mono text-amber-400">{kpis.sla_breaches}</div>
          <span className="text-[10px] text-slate-400 mt-1">Requires supervisor review</span>
        </div>
      </div>

      {/* Breakdown Charts Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Category Volume Breakdown */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
          <h3 className="text-sm font-bold text-slate-100">Incident Volume by Category</h3>
          <div className="space-y-2.5">
            {charts.category_breakdown.map((cat: any) => (
              <div key={cat.category} className="text-xs">
                <div className="flex justify-between mb-1 text-slate-300">
                  <span className="font-medium">{cat.category}</span>
                  <span className="font-mono font-bold text-slate-200">{cat.count} tickets</span>
                </div>
                <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden border border-slate-800">
                  <div
                    className="bg-brand-500 h-full rounded-full"
                    style={{ width: `${Math.min(100, (cat.count / kpis.total_incidents) * 100 * 3)}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Department Volume Breakdown */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
          <h3 className="text-sm font-bold text-slate-100">Incident Volume by Department</h3>
          <div className="space-y-2.5">
            {charts.department_breakdown.map((dept: any) => (
              <div key={dept.department} className="text-xs">
                <div className="flex justify-between mb-1 text-slate-300">
                  <span className="font-medium">{dept.fullName}</span>
                  <span className="font-mono font-bold text-slate-200">{dept.count}</span>
                </div>
                <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden border border-slate-800">
                  <div
                    className="bg-indigo-500 h-full rounded-full"
                    style={{ width: `${Math.min(100, (dept.count / kpis.total_incidents) * 100 * 2.5)}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Weekly Resolution Trend */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
        <h3 className="text-sm font-bold text-slate-100">7-Day Incident Volume & SLA Met Trend</h3>
        <div className="grid grid-cols-7 gap-2 text-center text-xs font-mono">
          {charts.volume_trend.map((day: any) => (
            <div key={day.day} className="bg-slate-950 p-3 rounded-lg border border-slate-800 space-y-2">
              <span className="font-bold text-brand-400 block">{day.day}</span>
              <div className="text-[11px] text-slate-300">
                <div>Created: <strong className="text-white">{day.created}</strong></div>
                <div>Resolved: <strong className="text-emerald-400">{day.resolved}</strong></div>
                <div>SLA Met: <strong className="text-indigo-300">{day.sla_met}</strong></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
