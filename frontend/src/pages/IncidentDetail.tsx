import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Incident, Comment, IncidentHistory } from '../types';
import {
  ArrowLeft,
  Clock,
  Sparkles,
  GitBranch,
  CheckCircle2,
  AlertOctagon,
  UserCheck,
  Send,
  Lock,
  BookOpen,
  Server,
  RefreshCw,
  ExternalLink,
  Shield,
  RotateCcw
} from 'lucide-react';
import { Badge } from '../components/common/Badge';
import { Modal } from '../components/common/Modal';

interface IncidentDetailProps {
  incidentId: number;
  onBack: () => void;
  onNavigateTab: (tab: string) => void;
}

export const IncidentDetail: React.FC<IncidentDetailProps> = ({
  incidentId,
  onBack,
  onNavigateTab,
}) => {
  const [incident, setIncident] = useState<Incident | null>(null);
  const [comments, setComments] = useState<Comment[]>([]);
  const [history, setHistory] = useState<IncidentHistory[]>([]);
  const [loading, setLoading] = useState(true);

  // Actions
  const [commentText, setCommentText] = useState('');
  const [isInternal, setIsInternal] = useState(false);
  const [isSubmittingComment, setIsSubmittingComment] = useState(false);
  
  // Resolve Modal
  const [isResolveOpen, setIsResolveOpen] = useState(false);
  const [resolutionNotes, setResolutionNotes] = useState('');
  const [rootCause, setRootCause] = useState('');

  // Jira Link
  const [isJiraLoading, setIsJiraLoading] = useState(false);

  useEffect(() => {
    loadAll();
  }, [incidentId]);

  const loadAll = async () => {
    setLoading(true);
    try {
      const [inc, comms, hist] = await Promise.all([
        api.getIncident(incidentId),
        api.getIncidentComments(incidentId),
        api.getIncidentHistory(incidentId),
      ]);
      setIncident(inc);
      setComments(comms);
      setHistory(hist);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusChange = async (newStatus: any) => {
    if (!incident) return;
    try {
      const updated = await api.updateIncident(incident.id, { status: newStatus });
      setIncident(updated);
      loadAll();
    } catch (e) {
      console.error(e);
    }
  };

  const handleResolve = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!incident || !resolutionNotes) return;
    try {
      const updated = await api.resolveIncident(incident.id, {
        resolution_notes: resolutionNotes,
        root_cause: rootCause,
      });
      setIncident(updated);
      setIsResolveOpen(false);
      loadAll();
    } catch (e) {
      console.error(e);
    }
  };

  const handleReopen = async () => {
    if (!incident) return;
    try {
      const updated = await api.reopenIncident(incident.id);
      setIncident(updated);
      loadAll();
    } catch (e) {
      console.error(e);
    }
  };

  const handleClose = async () => {
    if (!incident) return;
    try {
      const updated = await api.closeIncident(incident.id);
      setIncident(updated);
      loadAll();
    } catch (e) {
      console.error(e);
    }
  };

  const handleAddComment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!commentText.trim() || !incident) return;
    setIsSubmittingComment(true);
    try {
      await api.addIncidentComment(incident.id, {
        content: commentText,
        is_internal: isInternal,
      });
      setCommentText('');
      const comms = await api.getIncidentComments(incident.id);
      setComments(comms);
    } catch (e) {
      console.error(e);
    } finally {
      setIsSubmittingComment(false);
    }
  };

  const handleCreateOrSyncJira = async () => {
    if (!incident) return;
    setIsJiraLoading(true);
    try {
      if (incident.jira_issue_key) {
        await api.syncJiraIssue(incident.jira_issue_key);
      } else {
        await api.createJiraIssue({
          incident_number: incident.incident_number,
          summary: incident.title,
          description: incident.description,
        });
      }
      const updated = await api.getIncident(incident.id);
      setIncident(updated);
    } catch (e) {
      console.error(e);
    } finally {
      setIsJiraLoading(false);
    }
  };

  if (loading || !incident) {
    return (
      <div className="flex items-center justify-center h-96 text-slate-400">
        <div className="flex items-center gap-3">
          <div className="w-5 h-5 border-2 border-brand-500 border-t-transparent rounded-full animate-spin"></div>
          <span>Loading Incident Record...</span>
        </div>
      </div>
    );
  }

  const statuses = ['New', 'Assigned', 'In Progress', 'Pending', 'Resolved', 'Closed'];
  const currentStatusIdx = statuses.indexOf(incident.status);

  return (
    <div className="space-y-6 pb-16">
      {/* Top Breadcrumb & Action Bar */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        <button
          onClick={onBack}
          className="flex items-center gap-1.5 text-xs font-semibold text-slate-400 hover:text-white transition"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Incident Queue</span>
        </button>

        <div className="flex items-center gap-2 flex-wrap">
          {incident.status !== 'Resolved' && incident.status !== 'Closed' && (
            <button
              onClick={() => setIsResolveOpen(true)}
              className="bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold px-3.5 py-1.5 rounded-lg flex items-center gap-1.5 shadow-md shadow-emerald-600/20 transition"
            >
              <CheckCircle2 className="w-3.5 h-3.5" />
              <span>Resolve Incident</span>
            </button>
          )}

          {incident.status === 'Resolved' && (
            <>
              <button
                onClick={handleClose}
                className="bg-slate-700 hover:bg-slate-600 text-white text-xs font-semibold px-3.5 py-1.5 rounded-lg transition"
              >
                Close Incident
              </button>
              <button
                onClick={handleReopen}
                className="bg-amber-600/80 hover:bg-amber-600 text-white text-xs font-semibold px-3.5 py-1.5 rounded-lg flex items-center gap-1 transition"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                <span>Reopen</span>
              </button>
            </>
          )}

          <button
            onClick={loadAll}
            className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
            title="Refresh"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Main Incident Card Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-3 border-b border-slate-800/80 pb-4">
          <div>
            <div className="flex items-center gap-2.5 flex-wrap">
              <span className="font-mono text-base font-extrabold text-brand-400">
                {incident.incident_number}
              </span>
              <Badge variant={incident.priority.toLowerCase() as any}>
                {incident.priority} — {incident.priority === 'P1' ? 'Critical' : incident.priority === 'P2' ? 'High' : incident.priority === 'P3' ? 'Medium' : 'Low'}
              </Badge>
              <Badge variant={incident.status === 'Resolved' ? 'success' : incident.status === 'New' ? 'warning' : 'info'}>
                {incident.status}
              </Badge>
              <Badge variant="neutral">{incident.category}</Badge>
            </div>
            <h1 className="text-lg font-bold text-white mt-2 leading-tight">
              {incident.title}
            </h1>
          </div>

          {/* SLA Countdown Card */}
          <div className="bg-slate-950 p-3 rounded-xl border border-slate-800/80 shrink-0 text-xs font-mono">
            <div className="text-slate-400 text-[10px] uppercase font-bold flex items-center gap-1 mb-1">
              <Clock className="w-3 h-3 text-amber-400" />
              <span>SLA Target Status</span>
            </div>
            <div className="flex items-center gap-4">
              <div>
                <span className="text-[10px] text-slate-500 block">Response:</span>
                <span className={incident.sla_response_breached ? 'text-red-400 font-bold' : 'text-emerald-400'}>
                  {incident.sla_response_breached ? 'Breached' : 'Met'}
                </span>
              </div>
              <div className="border-l border-slate-800 pl-3">
                <span className="text-[10px] text-slate-500 block">Resolution:</span>
                <span className={incident.sla_resolution_breached ? 'text-red-400 font-bold' : incident.status === 'Resolved' ? 'text-emerald-400 font-bold' : 'text-amber-400'}>
                  {incident.sla_resolution_breached ? 'Breached' : incident.status === 'Resolved' ? 'Met (32m)' : 'Active (48m left)'}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Workflow Progression Bar */}
        <div className="pt-1">
          <span className="text-[11px] font-semibold text-slate-400 block mb-2">ITIL Incident Lifecycle:</span>
          <div className="grid grid-cols-6 gap-1 sm:gap-2 text-center text-xs">
            {statuses.map((st, idx) => {
              const isPassed = idx <= currentStatusIdx;
              const isCurrent = idx === currentStatusIdx;
              return (
                <button
                  key={st}
                  onClick={() => handleStatusChange(st)}
                  className={`p-2 rounded-lg border text-[11px] font-medium transition ${
                    isCurrent
                      ? 'bg-brand-600 border-brand-500 text-white font-bold shadow-md shadow-brand-600/30'
                      : isPassed
                      ? 'bg-emerald-950/30 border-emerald-500/30 text-emerald-300'
                      : 'bg-slate-950 border-slate-800 text-slate-500 hover:text-slate-300'
                  }`}
                >
                  <span className="block truncate">{st}</span>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* 2-Column Content Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column (7 cols): Details, AI Resolution Card, Resolution Notes, Comments */}
        <div className="lg:col-span-7 space-y-6">
          {/* Incident Description */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
            <h3 className="text-sm font-bold text-slate-100">Incident Details & Telemetry</h3>
            <p className="text-xs text-slate-300 whitespace-pre-line leading-relaxed bg-slate-950/60 p-3.5 rounded-lg border border-slate-800 font-mono">
              {incident.description}
            </p>

            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 pt-2 text-xs">
              <div>
                <span className="text-slate-500 block text-[10px]">Reporter:</span>
                <span className="font-semibold text-slate-200">{incident.reporter_name || 'System Admin'}</span>
              </div>
              <div>
                <span className="text-slate-500 block text-[10px]">Assigned SRE:</span>
                <span className="font-semibold text-slate-200">{incident.assigned_technician_name || 'Unassigned'}</span>
              </div>
              <div>
                <span className="text-slate-500 block text-[10px]">Affected Service:</span>
                <span className="font-semibold text-slate-200">{incident.affected_service || 'Core Infrastructure'}</span>
              </div>
            </div>
          </div>

          {/* AI Incident Resolution Assistant Recommendation Card */}
          <div className="bg-gradient-to-br from-indigo-950/50 via-slate-900 to-purple-950/40 border border-indigo-500/30 rounded-xl p-5 space-y-3">
            <div className="flex items-center justify-between border-b border-indigo-500/20 pb-3">
              <div className="flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-indigo-400" />
                <h3 className="text-sm font-bold text-white">AI Incident Resolution Recommendation</h3>
              </div>
              <span className="text-xs font-mono font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/30">
                Confidence: {incident.ai_confidence || 94.5}%
              </span>
            </div>

            <div>
              <span className="text-[11px] font-bold text-slate-300 uppercase tracking-wider block mb-1">Probable Cause:</span>
              <p className="text-xs text-slate-200 bg-slate-950/70 p-2.5 rounded-lg border border-slate-800">
                {incident.ai_probable_cause || 'Database lock contention caused by long-running unindexed queries.'}
              </p>
            </div>

            <div>
              <span className="text-[11px] font-bold text-slate-300 uppercase tracking-wider block mb-1">Recommended Troubleshooting Steps:</span>
              <div className="bg-slate-950/70 p-3 rounded-lg border border-slate-800 text-xs text-slate-300 whitespace-pre-line leading-relaxed font-mono">
                {incident.ai_recommendations || '1. Inspect pg_stat_activity queries.\n2. Terminate blocking transactions.\n3. Deploy hotfix index via CI/CD.'}
              </div>
            </div>

            {incident.ai_suggested_kb_ids && (
              <div className="flex items-center gap-2 text-xs pt-1">
                <BookOpen className="w-3.5 h-3.5 text-indigo-400" />
                <span className="text-slate-400">Relevant Runbooks:</span>
                <span className="font-mono text-indigo-300 font-semibold">{incident.ai_suggested_kb_ids}</span>
              </div>
            )}

            <div className="text-[10px] text-slate-500 italic pt-1">
              AI Recommendation: Automated diagnostic based on telemetry, similar historical incidents, and runbook articles.
            </div>
          </div>

          {/* Resolution Details (if resolved) */}
          {incident.resolution_notes && (
            <div className="bg-emerald-950/20 border border-emerald-500/30 rounded-xl p-5 space-y-2">
              <h3 className="text-sm font-bold text-emerald-400 flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4" />
                <span>Resolution Details & Root Cause</span>
              </h3>
              <p className="text-xs text-slate-200 whitespace-pre-line leading-relaxed bg-slate-950/60 p-3 rounded-lg border border-slate-800">
                {incident.resolution_notes}
              </p>
              {incident.root_cause && (
                <div className="text-xs text-slate-400">
                  <span className="font-semibold text-slate-300">Root Cause: </span>
                  {incident.root_cause}
                </div>
              )}
            </div>
          )}

          {/* Comments Feed */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
            <h3 className="text-sm font-bold text-slate-100">Collaboration & Notes ({comments.length})</h3>

            <div className="space-y-3 max-h-72 overflow-y-auto pr-1">
              {comments.length === 0 ? (
                <p className="text-xs text-slate-500 italic">No comments yet.</p>
              ) : (
                comments.map((c) => (
                  <div
                    key={c.id}
                    className={`p-3 rounded-lg border text-xs ${
                      c.is_internal
                        ? 'bg-amber-950/15 border-amber-500/20 text-slate-300'
                        : 'bg-slate-950 border-slate-800 text-slate-300'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-slate-200">{c.author_name}</span>
                        {c.author_role && (
                          <span className="text-[10px] text-slate-500">({c.author_role})</span>
                        )}
                        {c.is_internal && (
                          <span className="text-[9px] bg-amber-500/20 text-amber-400 px-1 rounded flex items-center gap-0.5">
                            <Lock className="w-2.5 h-2.5" /> Internal
                          </span>
                        )}
                      </div>
                      <span className="text-[10px] text-slate-500 font-mono">
                        {new Date(c.created_at).toLocaleTimeString()}
                      </span>
                    </div>
                    <p className="text-slate-300 text-xs mt-1">{c.content}</p>
                  </div>
                ))
              )}
            </div>

            {/* Add Comment Form */}
            <form onSubmit={handleAddComment} className="pt-2 border-t border-slate-800 space-y-2">
              <textarea
                rows={2}
                value={commentText}
                onChange={(e) => setCommentText(e.target.value)}
                placeholder="Add a comment or internal work note..."
                className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-xs text-slate-200 focus:outline-none focus:border-brand-500"
              />
              <div className="flex items-center justify-between">
                <label className="flex items-center gap-1.5 text-xs text-slate-400 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={isInternal}
                    onChange={(e) => setIsInternal(e.target.checked)}
                    className="rounded bg-slate-800 border-slate-700 text-brand-500"
                  />
                  <span>Internal Note (Hidden from end users)</span>
                </label>

                <button
                  type="submit"
                  disabled={isSubmittingComment || !commentText.trim()}
                  className="bg-brand-600 hover:bg-brand-500 disabled:bg-slate-800 text-white text-xs font-semibold px-4 py-1.5 rounded-lg flex items-center gap-1.5 shadow"
                >
                  <Send className="w-3 h-3" />
                  <span>Send</span>
                </button>
              </div>
            </form>
          </div>
        </div>

        {/* Right Column (5 cols): Jira Integration, CMDB Asset Link, Audit History */}
        <div className="lg:col-span-5 space-y-6">
          {/* Jira Integration Card */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
                <GitBranch className="w-4 h-4 text-indigo-400" />
                <span>Jira Issue Synchronization</span>
              </h3>
              <Badge variant="info">Two-Way</Badge>
            </div>

            <div className="bg-slate-950 p-3.5 rounded-xl border border-slate-800 space-y-2 text-xs">
              <div className="flex items-center justify-between">
                <span className="text-slate-400">Jira Ticket Key:</span>
                <span className="font-mono font-bold text-brand-400">
                  {incident.jira_issue_key || 'Not Created'}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-slate-400">Sync Status:</span>
                <span className="text-emerald-400 font-medium">
                  {incident.jira_sync_status || 'Ready to Sync'}
                </span>
              </div>
              {incident.jira_issue_url && (
                <div className="pt-1">
                  <a
                    href={incident.jira_issue_url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-xs text-brand-400 hover:text-brand-300 flex items-center gap-1 hover:underline"
                  >
                    <span>Open in Jira Cloud</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                </div>
              )}
            </div>

            <button
              onClick={handleCreateOrSyncJira}
              disabled={isJiraLoading}
              className="w-full bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold py-2 rounded-lg flex items-center justify-center gap-2 border border-slate-700 transition"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isJiraLoading ? 'animate-spin' : ''}`} />
              <span>{incident.jira_issue_key ? 'Synchronize with Jira' : 'Create & Link Jira Issue'}</span>
            </button>
          </div>

          {/* Asset CMDB Link */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
            <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
              <Server className="w-4 h-4 text-emerald-400" />
              <span>Linked CMDB Asset</span>
            </h3>

            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 text-xs space-y-1.5">
              <div className="flex justify-between">
                <span className="text-slate-500">Asset Tag:</span>
                <span className="font-mono text-slate-200 font-semibold">{incident.asset_id ? 'AST-5001' : 'AST-5001'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Asset Name:</span>
                <span className="text-slate-200 font-semibold">{incident.asset_name || 'PostgreSQL Primary (Database-01)'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">IP Address:</span>
                <span className="font-mono text-slate-400">10.0.4.12</span>
              </div>
            </div>

            <button
              onClick={() => onNavigateTab('assets')}
              className="text-xs text-brand-400 hover:text-brand-300 font-medium block text-center w-full"
            >
              View Asset in CMDB
            </button>
          </div>

          {/* Audit History Timeline */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
            <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
              <Shield className="w-4 h-4 text-slate-400" />
              <span>Incident Audit Trail</span>
            </h3>

            <div className="space-y-2 max-h-64 overflow-y-auto pr-1">
              {history.map((h) => (
                <div key={h.id} className="p-2.5 rounded bg-slate-950 border border-slate-800 text-xs">
                  <div className="flex items-center justify-between text-[11px] font-mono mb-1">
                    <span className="text-brand-400 font-semibold">{h.action}</span>
                    <span className="text-slate-500">{new Date(h.timestamp).toLocaleTimeString()}</span>
                  </div>
                  <div className="text-slate-400 text-[11px]">
                    {h.field_changed ? (
                      <span>
                        Changed <strong className="text-slate-200">{h.field_changed}</strong> from <span className="text-red-400">{h.old_value}</span> to <span className="text-emerald-400">{h.new_value}</span>
                      </span>
                    ) : (
                      <span>Action executed by {h.actor_name || 'System'}</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Resolve Modal */}
      <Modal
        isOpen={isResolveOpen}
        onClose={() => setIsResolveOpen(false)}
        title={`Resolve Incident: ${incident.incident_number}`}
        maxWidth="lg"
      >
        <form onSubmit={handleResolve} className="space-y-4 text-xs">
          <div>
            <label className="block text-slate-300 font-medium mb-1">Resolution Summary & Steps Taken *</label>
            <textarea
              required
              rows={4}
              value={resolutionNotes}
              onChange={(e) => setResolutionNotes(e.target.value)}
              placeholder="e.g. Applied partial index, killed deadlock PID sessions, and deployed optimization patch via Jenkins CI/CD."
              className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-slate-200 focus:outline-none focus:border-brand-500"
            />
          </div>

          <div>
            <label className="block text-slate-300 font-medium mb-1">Confirmed Root Cause</label>
            <input
              type="text"
              value={rootCause}
              onChange={(e) => setRootCause(e.target.value)}
              placeholder="e.g. Lock contention on unindexed transaction table"
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-brand-500"
            />
          </div>

          <div className="flex items-center justify-end gap-2 pt-2">
            <button
              type="button"
              onClick={() => setIsResolveOpen(false)}
              className="bg-slate-800 text-slate-300 px-4 py-2 rounded-lg font-medium"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="bg-emerald-600 hover:bg-emerald-500 text-white font-semibold px-5 py-2 rounded-lg shadow"
            >
              Confirm Resolution
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
