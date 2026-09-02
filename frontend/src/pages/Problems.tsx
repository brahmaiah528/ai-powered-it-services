import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Problem } from '../types';
import { HelpCircle, Plus, Search, ShieldAlert, CheckCircle2, ChevronRight } from 'lucide-react';
import { Badge } from '../components/common/Badge';
import { Modal } from '../components/common/Modal';

export const Problems: React.FC = () => {
  const [problems, setProblems] = useState<Problem[]>([]);
  const [loading, setLoading] = useState(true);
  const [isNewOpen, setIsNewOpen] = useState(false);

  // New problem form
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState('Database');
  const [description, setDescription] = useState('');
  const [rootCause, setRootCause] = useState('');
  const [workaround, setWorkaround] = useState('');
  const [permanentSolution, setPermanentSolution] = useState('');
  const [assignedTeam, setAssignedTeam] = useState('Enterprise Database Systems');

  useEffect(() => {
    loadProblems();
  }, []);

  const loadProblems = async () => {
    setLoading(true);
    try {
      const data = await api.getProblems();
      setProblems(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title || !description) return;
    try {
      await api.createProblem({
        title,
        category,
        description,
        root_cause: rootCause,
        workaround,
        permanent_solution: permanentSolution,
        assigned_team: assignedTeam,
      });
      setTitle('');
      setDescription('');
      setRootCause('');
      setWorkaround('');
      setPermanentSolution('');
      setIsNewOpen(false);
      loadProblems();
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="space-y-6 pb-12">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <HelpCircle className="w-5 h-5 text-brand-400" />
            <span>Problem Management & Root Cause Analysis</span>
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Identify recurring incident patterns, document known errors, and coordinate permanent architectural fixes.
          </p>
        </div>

        <button
          onClick={() => setIsNewOpen(true)}
          className="bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold px-3.5 py-2 rounded-lg flex items-center gap-1.5 shadow-md shadow-brand-600/20 transition"
        >
          <Plus className="w-4 h-4" />
          <span>Log Problem Record</span>
        </button>
      </div>

      <div className="grid grid-cols-1 gap-4">
        {loading ? (
          <div className="text-center py-12 text-slate-400 text-xs">Loading problems...</div>
        ) : (
          problems.map((prb) => (
            <div key={prb.id} className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800/80 pb-3">
                <div className="flex items-center gap-2.5">
                  <span className="font-mono text-sm font-bold text-brand-400">{prb.problem_number}</span>
                  <Badge variant="neutral">{prb.category}</Badge>
                  <Badge variant={prb.status === 'Resolved' ? 'success' : prb.status === 'Known Error' ? 'warning' : 'info'}>
                    {prb.status}
                  </Badge>
                </div>
                <span className="text-xs text-slate-400">Team: <strong className="text-slate-200">{prb.assigned_team || 'SRE Platform'}</strong></span>
              </div>

              <h3 className="text-sm font-bold text-slate-100">{prb.title}</h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 space-y-1">
                  <span className="font-bold text-amber-400 uppercase text-[10px] block">Root Cause Analysis (RCA):</span>
                  <p className="text-slate-300 font-mono text-[11px] leading-relaxed">
                    {prb.root_cause || 'Investigation underway across production logs.'}
                  </p>
                </div>

                <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 space-y-1">
                  <span className="font-bold text-emerald-400 uppercase text-[10px] block">Permanent Solution:</span>
                  <p className="text-slate-300 font-mono text-[11px] leading-relaxed">
                    {prb.permanent_solution || 'Patch scheduled in upcoming release.'}
                  </p>
                </div>
              </div>

              {prb.incident_numbers && prb.incident_numbers.length > 0 && (
                <div className="flex items-center gap-2 text-xs pt-1">
                  <span className="text-slate-400 font-medium">Linked Incidents:</span>
                  <div className="flex flex-wrap gap-1.5">
                    {prb.incident_numbers.map((num) => (
                      <span key={num} className="font-mono text-[11px] bg-brand-500/10 text-brand-300 border border-brand-500/20 px-1.5 py-0.5 rounded">
                        {num}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))
        )}
      </div>

      {/* New Problem Modal */}
      <Modal isOpen={isNewOpen} onClose={() => setIsNewOpen(false)} title="Log New Problem Record" maxWidth="lg">
        <form onSubmit={handleCreate} className="space-y-4 text-xs">
          <div>
            <label className="block text-slate-300 font-medium mb-1">Problem Title *</label>
            <input
              type="text"
              required
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Database connection exhaustion under concurrent traffic spikes"
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-brand-500"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
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
                <option value="Cloud">Cloud</option>
                <option value="Software">Software</option>
              </select>
            </div>
            <div>
              <label className="block text-slate-300 font-medium mb-1">Assigned Team</label>
              <input
                type="text"
                value={assignedTeam}
                onChange={(e) => setAssignedTeam(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-brand-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-slate-300 font-medium mb-1">Problem Symptoms & Description *</label>
            <textarea
              required
              rows={2}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-brand-500"
            />
          </div>

          <div>
            <label className="block text-slate-300 font-medium mb-1">Root Cause (RCA)</label>
            <textarea
              rows={2}
              value={rootCause}
              onChange={(e) => setRootCause(e.target.value)}
              placeholder="e.g. Memory leak in connection pooler holding idle sessions indefinitely"
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-brand-500"
            />
          </div>

          <div>
            <label className="block text-slate-300 font-medium mb-1">Permanent Solution Plan</label>
            <textarea
              rows={2}
              value={permanentSolution}
              onChange={(e) => setPermanentSolution(e.target.value)}
              placeholder="e.g. Deploy PgBouncer proxy and scoped SQLAlchemy connection lifecycles"
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-brand-500"
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
              Save Problem Record
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
