import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { DevOpsStatus } from '../types';
import {
  GitBranch,
  GitPullRequest,
  CheckCircle2,
  Play,
  RotateCcw,
  Terminal,
  ExternalLink,
  Layers,
  Activity,
  Server,
  RefreshCw,
  Clock,
  ShieldCheck
} from 'lucide-react';
import { Badge } from '../components/common/Badge';

export const DevOpsHub: React.FC = () => {
  const [status, setStatus] = useState<DevOpsStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [isTriggering, setIsTriggering] = useState(false);
  const [buildMsg, setBuildMsg] = useState('');

  useEffect(() => {
    loadDevOps();
  }, []);

  const loadDevOps = async () => {
    setLoading(true);
    try {
      const data = await api.getDevOpsStatus();
      setStatus(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleTriggerBuild = async () => {
    setIsTriggering(true);
    try {
      await api.triggerJenkinsBuild(buildMsg || 'Manual Jenkins build triggered from ITSM console');
      setBuildMsg('');
      loadDevOps();
    } catch (e) {
      console.error(e);
    } finally {
      setIsTriggering(false);
    }
  };

  const handleSimulateCommit = async () => {
    try {
      await api.commitFixDevOps('fix(db): add partial index and connection pool tuning for Database-01');
      loadDevOps();
    } catch (e) {
      console.error(e);
    }
  };

  if (loading || !status) {
    return (
      <div className="flex items-center justify-center h-96 text-slate-400">
        <div className="flex items-center gap-3">
          <div className="w-5 h-5 border-2 border-brand-500 border-t-transparent rounded-full animate-spin"></div>
          <span>Loading DevOps & Jira Ecosystem...</span>
        </div>
      </div>
    );
  }

  const { github, jira, jenkins, docker } = status;

  return (
    <div className="space-y-6 pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
              <GitBranch className="w-5 h-5 text-brand-400" />
              <span>DevOps Integration & Issue Sync Hub</span>
            </h2>
            <Badge variant="success">{status.mode}</Badge>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            Orchestration and telemetry for GitHub, Jira Issue Sync, Jenkins 11-Stage CI/CD, and Docker Containers.
          </p>
        </div>

        <button
          onClick={loadDevOps}
          className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
          title="Refresh"
        >
          <RefreshCw className="w-4 h-4" />
        </button>
      </div>

      {/* 4 Cards Status Overview */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* GitHub */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4.5 space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <GitPullRequest className="w-4 h-4 text-slate-200" />
              <span className="text-xs font-bold text-slate-200">GitHub Repo</span>
            </div>
            <Badge variant="success">Connected</Badge>
          </div>
          <div className="font-mono text-xs text-brand-400 truncate">{github.repository}</div>
          <div className="text-[11px] text-slate-400">
            Default Branch: <span className="text-slate-200 font-mono font-bold">{github.default_branch}</span> • {github.open_pull_requests} open PRs
          </div>
        </div>

        {/* Jira */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4.5 space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <GitBranch className="w-4 h-4 text-blue-400" />
              <span className="text-xs font-bold text-slate-200">Jira Cloud</span>
            </div>
            <Badge variant="info">{jira.mode}</Badge>
          </div>
          <div className="font-mono text-xs text-blue-400">Project Key: {jira.project}</div>
          <div className="text-[11px] text-slate-400">
            Linked Issues: <span className="text-slate-200 font-bold font-mono">{jira.open_issues_count}</span> in sync
          </div>
        </div>

        {/* Jenkins */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4.5 space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Activity className="w-4 h-4 text-emerald-400" />
              <span className="text-xs font-bold text-slate-200">Jenkins CI/CD</span>
            </div>
            <Badge variant="success">Passing</Badge>
          </div>
          <div className="font-mono text-xs text-emerald-400">Build #{jenkins.latest_build.number} ({jenkins.latest_build.status})</div>
          <div className="text-[11px] text-slate-400">
            Duration: <span className="text-slate-200 font-mono font-bold">{jenkins.latest_build.duration}</span> • 11 stages
          </div>
        </div>

        {/* Docker */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4.5 space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Server className="w-4 h-4 text-cyan-400" />
              <span className="text-xs font-bold text-slate-200">Docker Engine</span>
            </div>
            <Badge variant="success">Healthy</Badge>
          </div>
          <div className="font-mono text-xs text-cyan-400">3/3 Containers Active</div>
          <div className="text-[11px] text-slate-400">
            Compose: <span className="text-slate-200">frontend, backend, postgres</span>
          </div>
        </div>
      </div>

      {/* Main Grid: Jenkins 11-Stage Pipeline & Jira Issue Feed */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column (7 cols): Jenkins 11-Stage Pipeline */}
        <div className="lg:col-span-7 space-y-6">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
                  <Activity className="w-4 h-4 text-emerald-400" />
                  <span>Jenkins 11-Stage Pipeline Execution Flow</span>
                </h3>
                <p className="text-xs text-slate-400">Build #{jenkins.latest_build.number} • Triggered by {jenkins.latest_build.triggered_by}</p>
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={handleSimulateCommit}
                  className="bg-slate-800 hover:bg-slate-700 text-slate-200 text-[11px] font-semibold px-2.5 py-1.5 rounded-lg border border-slate-700 transition"
                >
                  Simulate Commit & Push
                </button>
                <button
                  onClick={handleTriggerBuild}
                  disabled={isTriggering}
                  className="bg-brand-600 hover:bg-brand-500 disabled:bg-slate-800 text-white text-[11px] font-semibold px-3 py-1.5 rounded-lg flex items-center gap-1 shadow transition"
                >
                  <Play className="w-3 h-3 fill-white" />
                  <span>{isTriggering ? 'Running...' : 'Trigger Pipeline'}</span>
                </button>
              </div>
            </div>

            {/* 11 Pipeline Stages */}
            <div className="space-y-2">
              {jenkins.latest_build.stages.map((st, idx) => (
                <div
                  key={st.name}
                  className="bg-slate-950 p-2.5 rounded-lg border border-slate-800/80 flex items-center justify-between text-xs"
                >
                  <div className="flex items-center gap-2.5">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                    <div>
                      <span className="font-semibold text-slate-200">{st.name}</span>
                    </div>
                  </div>

                  <div className="flex items-center gap-3 font-mono text-[11px]">
                    <span className="text-slate-500">{st.duration}</span>
                    <Badge variant="success">{st.status}</Badge>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Docker Containers Grid */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
            <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
              <Server className="w-4 h-4 text-cyan-400" />
              <span>Docker Compose Microservices Status</span>
            </h3>

            <div className="space-y-2.5">
              {docker.containers.map((c) => (
                <div
                  key={c.name}
                  className="bg-slate-950 p-3 rounded-lg border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs"
                >
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-slate-100 font-mono">{c.name}</span>
                      <Badge variant="success">{c.health}</Badge>
                    </div>
                    <span className="text-[10px] text-slate-500 font-mono">Image: {c.image} • Port: {c.port}</span>
                  </div>

                  <div className="flex items-center gap-4 text-right font-mono text-[11px] text-slate-400">
                    <div>CPU: <strong className="text-slate-200">{c.cpu}</strong></div>
                    <div>Memory: <strong className="text-slate-200">{c.memory}</strong></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column (5 cols): Jira Issues & GitHub Commit Stream */}
        <div className="lg:col-span-5 space-y-6">
          {/* Jira Issues Stream */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
                <GitBranch className="w-4 h-4 text-blue-400" />
                <span>Synchronized Jira Work Items</span>
              </h3>
              <Badge variant="info">Jira Cloud</Badge>
            </div>

            <div className="space-y-2.5">
              {jira.recent_issues.map((issue: any) => (
                <div key={issue.key} className="bg-slate-950 p-3 rounded-xl border border-slate-800 space-y-1.5 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="font-mono font-bold text-blue-400">{issue.key}</span>
                    <Badge variant={issue.status === 'Done' ? 'success' : 'warning'}>{issue.status}</Badge>
                  </div>
                  <h4 className="font-semibold text-slate-200 leading-snug">{issue.summary}</h4>
                  <div className="flex items-center justify-between text-[11px] text-slate-400 pt-1 font-mono">
                    <span>Assignee: {issue.assignee}</span>
                    <a
                      href={issue.url}
                      target="_blank"
                      rel="noreferrer"
                      className="text-brand-400 hover:text-brand-300 flex items-center gap-0.5"
                    >
                      <span>View</span>
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* GitHub Commit Stream */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
            <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
              <GitPullRequest className="w-4 h-4 text-slate-200" />
              <span>Recent GitHub Commits</span>
            </h3>

            <div className="space-y-2 font-mono text-xs">
              {github.recent_commits.map((cmt: any) => (
                <div key={cmt.sha} className="bg-slate-950 p-2.5 rounded-lg border border-slate-800">
                  <div className="flex items-center justify-between text-[11px] text-slate-400 mb-0.5">
                    <span className="font-bold text-brand-400">{cmt.sha}</span>
                    <span className="text-[10px] text-slate-500">{cmt.time}</span>
                  </div>
                  <p className="text-slate-300 text-[11px] truncate">{cmt.message}</p>
                  <span className="text-[10px] text-slate-500 block mt-0.5">Author: {cmt.author}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
