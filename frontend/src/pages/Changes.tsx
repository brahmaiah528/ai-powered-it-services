import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { ChangeItem } from '../types';
import { GitPullRequest, Plus, CheckCircle2, AlertTriangle, ShieldCheck, Clock } from 'lucide-react';
import { Badge } from '../components/common/Badge';
import { Modal } from '../components/common/Modal';

export const Changes: React.FC = () => {
  const [changes, setChanges] = useState<ChangeItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [isNewOpen, setIsNewOpen] = useState(false);

  // New Change Form
  const [title, setTitle] = useState('');
  const [changeType, setChangeType] = useState('Normal');
  const [description, setDescription] = useState('');
  const [reason, setReason] = useState('');
  const [implementationPlan, setImplementationPlan] = useState('');
  const [rollbackPlan, setRollbackPlan] = useState('');
  const [riskLevel, setRiskLevel] = useState('Medium');
  const [assignedTeam, setAssignedTeam] = useState('Enterprise Database Systems');

  useEffect(() => {
    loadChanges();
  }, []);

  const loadChanges = async () => {
    setLoading(true);
    try {
      const data = await api.getChanges();
      setChanges(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title || !implementationPlan || !rollbackPlan) return;
    try {
      await api.createChange({
        title,
        change_type: changeType,
        requester_name: 'Lead SRE',
        assigned_team: assignedTeam,
        description,
        reason_for_change: reason,
        risk_level: riskLevel,
        impact_level: riskLevel,
        implementation_plan: implementationPlan,
        rollback_plan: rollbackPlan,
      });
      setTitle('');
      setDescription('');
      setImplementationPlan('');
      setRollbackPlan('');
      setIsNewOpen(false);
      loadChanges();
    } catch (e) {
      console.error(e);
    }
  };

  const handleApprove = async (id: number) => {
    try {
      await api.updateChange(id, { status: 'Approval' });
      loadChanges();
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="space-y-6 pb-12">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <GitPullRequest className="w-5 h-5 text-brand-400" />
            <span>Change Management & CAB Approval (RFC)</span>
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Standard, Normal, and Emergency change workflows with rollback plans and CAB review.
          </p>
        </div>

        <button
          onClick={() => setIsNewOpen(true)}
          className="bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold px-3.5 py-2 rounded-lg flex items-center gap-1.5 shadow-md shadow-brand-600/20 transition"
        >
          <Plus className="w-4 h-4" />
          <span>Request Change (RFC)</span>
        </button>
      </div>

      <div className="grid grid-cols-1 gap-4">
        {loading ? (
          <div className="text-center py-12 text-slate-400 text-xs">Loading change requests...</div>
        ) : (
          changes.map((chg) => (
            <div key={chg.id} className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800/80 pb-3">
                <div className="flex items-center gap-2.5">
                  <span className="font-mono text-sm font-bold text-brand-400">{chg.change_number}</span>
                  <Badge variant={chg.change_type === 'Emergency' ? 'danger' : chg.change_type === 'Standard' ? 'info' : 'neutral'}>
                    {chg.change_type}
                  </Badge>
                  <Badge variant={chg.status === 'Completed' ? 'success' : chg.status === 'Approval' ? 'info' : 'warning'}>
                    {chg.status}
                  </Badge>
                  <Badge variant={chg.risk_level === 'High' ? 'p2' : 'neutral'}>Risk: {chg.risk_level}</Badge>
                </div>
                <div className="text-xs text-slate-400">
                  Requester: <strong className="text-slate-200">{chg.requester_name}</strong> • Team: <strong className="text-slate-200">{chg.assigned_team}</strong>
                </div>
              </div>

              <h3 className="text-sm font-bold text-slate-100">{chg.title}</h3>
              <p className="text-xs text-slate-300">{chg.description}</p>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 space-y-1">
                  <span className="font-bold text-indigo-400 uppercase text-[10px] block">Implementation Plan:</span>
                  <p className="text-slate-300 font-mono text-[11px] whitespace-pre-line leading-relaxed">
                    {chg.implementation_plan}
                  </p>
                </div>

                <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 space-y-1">
                  <span className="font-bold text-red-400 uppercase text-[10px] block">Rollback Plan:</span>
                  <p className="text-slate-300 font-mono text-[11px] whitespace-pre-line leading-relaxed">
                    {chg.rollback_plan}
                  </p>
                </div>
              </div>

              <div className="flex items-center justify-between pt-2 border-t border-slate-800/60 text-xs">
                <span className="text-slate-400">
                  {chg.approver_name ? `Approved by: ${chg.approver_name}` : 'Awaiting CAB Approval'}
                </span>

                {chg.status === 'Requested' && (
                  <button
                    onClick={() => handleApprove(chg.id)}
                    className="bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs px-3 py-1.5 rounded-lg shadow transition flex items-center gap-1"
                  >
                    <ShieldCheck className="w-3.5 h-3.5" />
                    <span>Approve Change (CAB)</span>
                  </button>
                )}
              </div>
            </div>
          ))
        )}
      </div>

      {/* New Change Modal */}
      <Modal isOpen={isNewOpen} onClose={() => setIsNewOpen(false)} title="Request New Change (RFC)" maxWidth="lg">
        <form onSubmit={handleCreate} className="space-y-4 text-xs">
          <div>
            <label className="block text-slate-300 font-medium mb-1">Change Title *</label>
            <input
              type="text"
              required
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Apply index and connection pool optimization on Database-01"
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-brand-500"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-slate-300 font-medium mb-1">Change Type</label>
              <select
                value={changeType}
                onChange={(e) => setChangeType(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-brand-500"
              >
                <option value="Normal">Normal</option>
                <option value="Standard">Standard</option>
                <option value="Emergency">Emergency</option>
              </select>
            </div>
            <div>
              <label className="block text-slate-300 font-medium mb-1">Risk Level</label>
              <select
                value={riskLevel}
                onChange={(e) => setRiskLevel(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-brand-500"
              >
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
                <option value="Critical">Critical</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-slate-300 font-medium mb-1">Change Description & Justification</label>
            <textarea
              rows={2}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-brand-500"
            />
          </div>

          <div>
            <label className="block text-slate-300 font-medium mb-1">Implementation Plan *</label>
            <textarea
              required
              rows={3}
              value={implementationPlan}
              onChange={(e) => setImplementationPlan(e.target.value)}
              placeholder="1. Step one...&#10;2. Step two...&#10;3. Verification..."
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-brand-500 font-mono"
            />
          </div>

          <div>
            <label className="block text-slate-300 font-medium mb-1">Rollback Plan *</label>
            <textarea
              required
              rows={2}
              value={rollbackPlan}
              onChange={(e) => setRollbackPlan(e.target.value)}
              placeholder="Steps to revert changes if validation checks fail..."
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-brand-500 font-mono"
            />
          </div>

          <div className="flex items-center justify-end gap-2 pt-2">
            <button
              type="button"
              onClick={() => setIsNewOpen(false)}
              className="bg-slate-800 text-slate-300 px-4 py-2 rounded-lg font-medium"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="bg-brand-600 hover:bg-brand-500 text-white font-semibold px-5 py-2 rounded-lg shadow"
            >
              Submit RFC
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
