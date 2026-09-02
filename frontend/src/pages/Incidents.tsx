import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Incident } from '../types';
import {
  AlertTriangle,
  Plus,
  Filter,
  Search,
  Clock,
  Sparkles,
  CheckCircle2,
  ChevronRight,
  ShieldAlert,
  ArrowUpDown,
  RefreshCw
} from 'lucide-react';
import { Badge } from '../components/common/Badge';
import { Modal } from '../components/common/Modal';

interface IncidentsProps {
  searchQuery: string;
  onOpenDetail: (id: number) => void;
  isOpenNewModal: boolean;
  onCloseNewModal: () => void;
}

export const Incidents: React.FC<IncidentsProps> = ({
  searchQuery,
  onOpenDetail,
  isOpenNewModal,
  onCloseNewModal,
}) => {
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [loading, setLoading] = useState(true);
  
  // Filters
  const [priorityFilter, setPriorityFilter] = useState<string>('');
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [categoryFilter, setCategoryFilter] = useState<string>('');

  // Create Form state
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [category, setCategory] = useState('Software');
  const [impact, setImpact] = useState('Medium');
  const [urgency, setUrgency] = useState('Medium');
  const [affectedService, setAffectedService] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    loadIncidents();
  }, [priorityFilter, statusFilter, categoryFilter, searchQuery]);

  const loadIncidents = async () => {
    setLoading(true);
    try {
      const params: Record<string, string> = {};
      if (priorityFilter) params.priority = priorityFilter;
      if (statusFilter) params.status = statusFilter;
      if (categoryFilter) params.category = categoryFilter;
      if (searchQuery) params.search = searchQuery;

      const data = await api.getIncidents(params);
      setIncidents(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateIncident = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title || !description) return;
    setIsSubmitting(true);
    try {
      const newInc = await api.createIncident({
        title,
        description,
        category,
        impact,
        urgency,
        affected_service: affectedService || undefined,
      });
      setTitle('');
      setDescription('');
      setAffectedService('');
      onCloseNewModal();
      loadIncidents();
      onOpenDetail(newInc.id);
    } catch (err) {
      console.error(err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-brand-400" />
            <span>Incident Management Queue</span>
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Enterprise ITIL incident lifecycle tracking, SLA timers, and AI resolution intelligence.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={loadIncidents}
            className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
            title="Refresh"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
          <button
            onClick={() => {
              // Open modal handled by parent state
            }}
            className="bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold px-3.5 py-2 rounded-lg flex items-center gap-1.5 shadow-md shadow-brand-600/20 transition"
          >
            <Plus className="w-4 h-4" />
            <span>Create Incident</span>
          </button>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-3.5 flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex flex-wrap items-center gap-2.5">
          <span className="text-slate-400 font-medium flex items-center gap-1">
            <Filter className="w-3.5 h-3.5" /> Filters:
          </span>

          <select
            value={priorityFilter}
            onChange={(e) => setPriorityFilter(e.target.value)}
            className="bg-slate-800 border border-slate-700 text-slate-200 rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-brand-500"
          >
            <option value="">All Priorities</option>
            <option value="P1">P1 — Critical</option>
            <option value="P2">P2 — High</option>
            <option value="P3">P3 — Medium</option>
            <option value="P4">P4 — Low</option>
          </select>

          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="bg-slate-800 border border-slate-700 text-slate-200 rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-brand-500"
          >
            <option value="">All Statuses</option>
            <option value="New">New</option>
            <option value="Assigned">Assigned</option>
            <option value="In Progress">In Progress</option>
            <option value="Pending">Pending</option>
            <option value="Resolved">Resolved</option>
            <option value="Closed">Closed</option>
          </select>

          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="bg-slate-800 border border-slate-700 text-slate-200 rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-brand-500"
          >
            <option value="">All Categories</option>
            <option value="Database">Database</option>
            <option value="Authentication">Authentication</option>
            <option value="Network">Network</option>
            <option value="Infrastructure">Infrastructure</option>
            <option value="Security">Security</option>
            <option value="Cloud">Cloud</option>
            <option value="Application">Application</option>
            <option value="Email">Email</option>
            <option value="Hardware">Hardware</option>
            <option value="Software">Software</option>
          </select>
        </div>

        <div className="text-slate-400 font-mono text-[11px]">
          Showing {incidents.length} incidents
        </div>
      </div>

      {/* Incidents Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="bg-slate-950/60 border-b border-slate-800 text-slate-400 font-semibold uppercase text-[10px]">
                <th className="py-3 px-4">Ticket ID</th>
                <th className="py-3 px-4">Summary & Affected Service</th>
                <th className="py-3 px-4">Category</th>
                <th className="py-3 px-4">Priority</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4">Assigned Agent</th>
                <th className="py-3 px-4">SLA Status</th>
                <th className="py-3 px-4">Jira Link</th>
                <th className="py-3 px-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {loading ? (
                <tr>
                  <td colSpan={9} className="text-center py-12 text-slate-400">
                    Loading incident records...
                  </td>
                </tr>
              ) : incidents.length === 0 ? (
                <tr>
                  <td colSpan={9} className="text-center py-12 text-slate-400">
                    No incidents matching current criteria.
                  </td>
                </tr>
              ) : (
                incidents.map((inc) => (
                  <tr
                    key={inc.id}
                    onClick={() => onOpenDetail(inc.id)}
                    className="hover:bg-slate-800/50 cursor-pointer transition"
                  >
                    <td className="py-3 px-4 font-mono font-bold text-brand-400 whitespace-nowrap">
                      {inc.incident_number}
                    </td>
                    <td className="py-3 px-4 max-w-[280px]">
                      <span className="font-semibold text-slate-200 block truncate">{inc.title}</span>
                      <span className="text-[10px] text-slate-400 block truncate">
                        Service: {inc.affected_service || 'Enterprise Cloud'} • Dept: {inc.department_name || 'IT Operations'}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-slate-300 whitespace-nowrap">
                      {inc.category}
                    </td>
                    <td className="py-3 px-4 whitespace-nowrap">
                      <Badge variant={inc.priority.toLowerCase() as any}>{inc.priority}</Badge>
                    </td>
                    <td className="py-3 px-4 whitespace-nowrap">
                      <Badge
                        variant={
                          inc.status === 'Resolved'
                            ? 'success'
                            : inc.status === 'New'
                            ? 'warning'
                            : inc.status === 'In Progress'
                            ? 'info'
                            : 'neutral'
                        }
                      >
                        {inc.status}
                      </Badge>
                    </td>
                    <td className="py-3 px-4 text-slate-300 whitespace-nowrap">
                      {inc.assigned_technician_name || (
                        <span className="text-slate-500 italic">Unassigned</span>
                      )}
                    </td>
                    <td className="py-3 px-4 whitespace-nowrap">
                      {inc.sla_resolution_breached ? (
                        <span className="text-[10px] font-semibold text-red-400 bg-red-500/10 px-1.5 py-0.5 rounded border border-red-500/30">
                          BREACHED
                        </span>
                      ) : inc.status === 'Resolved' || inc.status === 'Closed' ? (
                        <span className="text-[10px] text-emerald-400 bg-emerald-500/10 px-1.5 py-0.5 rounded">
                          SLA Met
                        </span>
                      ) : (
                        <span className="text-[10px] text-amber-300 flex items-center gap-1">
                          <Clock className="w-3 h-3 text-amber-400" /> Active SLA
                        </span>
                      )}
                    </td>
                    <td className="py-3 px-4 font-mono text-[11px] text-indigo-300 whitespace-nowrap">
                      {inc.jira_issue_key ? (
                        <span className="hover:underline flex items-center gap-1">
                          {inc.jira_issue_key}
                        </span>
                      ) : (
                        <span className="text-slate-600">—</span>
                      )}
                    </td>
                    <td className="py-3 px-4 text-right whitespace-nowrap">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          onOpenDetail(inc.id);
                        }}
                        className="text-brand-400 hover:text-brand-300 font-semibold p-1 rounded hover:bg-slate-800"
                      >
                        <ChevronRight className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Create Incident Modal */}
      <Modal
        isOpen={isOpenNewModal}
        onClose={onCloseNewModal}
        title="Raise New IT Incident (ITIL Form)"
        maxWidth="2xl"
      >
        <form onSubmit={handleCreateIncident} className="space-y-4 text-xs">
          <div>
            <label className="block text-slate-300 font-medium mb-1">Incident Title / Summary *</label>
            <input
              type="text"
              required
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Database server connection pool timeout on customer checkout"
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-brand-500"
            />
          </div>

          <div>
            <label className="block text-slate-300 font-medium mb-1">Detailed Description & Error Stack *</label>
            <textarea
              required
              rows={4}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Provide symptoms, error codes, affected users, and reproduction steps..."
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-brand-500"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div>
              <label className="block text-slate-300 font-medium mb-1">Category</label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-brand-500"
              >
                <option value="Database">Database</option>
                <option value="Authentication">Authentication</option>
                <option value="Network">Network</option>
                <option value="Infrastructure">Infrastructure</option>
                <option value="Security">Security</option>
                <option value="Cloud">Cloud</option>
                <option value="Application">Application</option>
                <option value="Email">Email</option>
                <option value="Hardware">Hardware</option>
                <option value="Software">Software</option>
              </select>
            </div>

            <div>
              <label className="block text-slate-300 font-medium mb-1">Impact</label>
              <select
                value={impact}
                onChange={(e) => setImpact(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-brand-500"
              >
                <option value="High">High (Org Wide)</option>
                <option value="Medium">Medium (Dept)</option>
                <option value="Low">Low (Individual)</option>
              </select>
            </div>

            <div>
              <label className="block text-slate-300 font-medium mb-1">Urgency</label>
              <select
                value={urgency}
                onChange={(e) => setUrgency(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-brand-500"
              >
                <option value="High">High (Critical)</option>
                <option value="Medium">Medium (Standard)</option>
                <option value="Low">Low (Minor)</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-slate-300 font-medium mb-1">Affected Service</label>
            <input
              type="text"
              value={affectedService}
              onChange={(e) => setAffectedService(e.target.value)}
              placeholder="e.g. Core Database Cluster / Payment API"
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-brand-500"
            />
          </div>

          <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 flex items-center justify-between text-xs">
            <span className="text-slate-400">Calculated Priority:</span>
            <span className="font-bold text-slate-100 font-mono">
              {impact === 'High' && urgency === 'High' ? 'P1 — Critical' :
               (impact === 'High' || urgency === 'High') ? 'P2 — High' :
               (impact === 'Medium' && urgency === 'Medium') ? 'P3 — Medium' : 'P4 — Low'}
            </span>
          </div>

          <div className="flex items-center justify-end gap-2 pt-2">
            <button
              type="button"
              onClick={onCloseNewModal}
              className="bg-slate-800 hover:bg-slate-700 text-slate-300 px-4 py-2 rounded-lg font-medium"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="bg-brand-600 hover:bg-brand-500 disabled:bg-slate-800 text-white font-semibold px-5 py-2 rounded-lg flex items-center gap-1.5 shadow-md shadow-brand-600/20"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>{isSubmitting ? 'Analyzing & Creating...' : 'Submit Incident'}</span>
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
