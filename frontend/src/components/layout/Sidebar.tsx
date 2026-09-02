import React from 'react';
import {
  LayoutDashboard,
  AlertTriangle,
  FileCheck2,
  HelpCircle,
  GitPullRequest,
  Server,
  Activity,
  BookOpen,
  Sparkles,
  BarChart3,
  Bell,
  GitBranch,
  ShieldCheck,
  PlayCircle,
  LogOut,
  Layers
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useNotifications } from '../../context/NotificationContext';

interface SidebarProps {
  currentTab: string;
  onSelectTab: (tab: string) => void;
  onOpenSimulation: () => void;
  onOpenProfile?: () => void;
  onOpenLogin?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  currentTab,
  onSelectTab,
  onOpenSimulation,
  onOpenProfile,
  onOpenLogin,
}) => {
  const { user, logout, switchRole } = useAuth();
  const { unreadCount } = useNotifications();

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'incidents', label: 'Incidents', icon: AlertTriangle, badge: '30' },
    { id: 'service-requests', label: 'Service Requests', icon: FileCheck2, badge: '10' },
    { id: 'problems', label: 'Problems', icon: HelpCircle, badge: '5' },
    { id: 'changes', label: 'Changes (RFC)', icon: GitPullRequest, badge: '5' },
    { id: 'assets', label: 'IT Assets', icon: Server, badge: '20' },
    { id: 'infrastructure', label: 'Infrastructure', icon: Activity },
    { id: 'knowledge-base', label: 'Knowledge Base', icon: BookOpen },
    { id: 'ai-assistant', label: 'AI Operations', icon: Sparkles, highlight: true },
    { id: 'reports', label: 'Reports & SLA', icon: BarChart3 },
    { id: 'notifications', label: 'Notifications', icon: Bell, count: unreadCount },
    { id: 'devops', label: 'DevOps & Jira', icon: GitBranch, highlight: true },
    { id: 'audit-logs', label: 'Audit Trail', icon: ShieldCheck },
  ];

  return (
    <aside className="w-64 bg-slate-900/95 border-r border-slate-800 flex flex-col h-screen fixed left-0 top-0 z-30 select-none">
      {/* Brand Header */}
      <div className="p-4 border-b border-slate-800/80 flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 to-indigo-400 flex items-center justify-center shadow-lg shadow-brand-500/25">
          <Layers className="w-5 h-5 text-white" />
        </div>
        <div>
          <h1 className="font-bold text-sm tracking-tight text-white flex items-center gap-1.5">
            AutoOps ITSM
            <span className="text-[10px] uppercase font-mono px-1.5 py-0.5 rounded bg-brand-500/20 text-brand-400 border border-brand-500/30">AI</span>
          </h1>
          <p className="text-[11px] text-slate-400 truncate max-w-[130px]">Enterprise IT Platform</p>
        </div>
      </div>

      {/* Critical Scenario Interactive Runner Banner */}
      <div className="p-3">
        <button
          onClick={onOpenSimulation}
          className="w-full bg-gradient-to-r from-red-600 via-rose-600 to-amber-600 hover:from-red-500 hover:to-amber-500 text-white rounded-lg p-2.5 flex items-center justify-between text-xs font-semibold shadow-lg shadow-red-500/20 transition group"
        >
          <span className="flex items-center gap-2">
            <PlayCircle className="w-4 h-4 text-white animate-pulse" />
            <span>Critical DB Scenario</span>
          </span>
          <span className="text-[10px] bg-white/20 px-1.5 py-0.5 rounded text-white font-mono">23 Steps</span>
        </button>
      </div>

      {/* Navigation List */}
      <nav className="flex-1 overflow-y-auto px-3 py-1 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onSelectTab(item.id)}
              className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-xs font-medium transition ${
                isActive
                  ? 'bg-brand-600 text-white shadow-md shadow-brand-600/30'
                  : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/60'
              } ${item.highlight && !isActive ? 'text-indigo-300 font-semibold' : ''}`}
            >
              <div className="flex items-center gap-2.5">
                <Icon className={`w-4 h-4 ${isActive ? 'text-white' : item.highlight ? 'text-indigo-400' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span className={`text-[10px] px-1.5 py-0.2 rounded font-mono ${isActive ? 'bg-white/20 text-white' : 'bg-slate-800 text-slate-400'}`}>
                  {item.badge}
                </span>
              )}
              {item.count !== undefined && item.count > 0 && (
                <span className="text-[10px] px-1.5 py-0.2 rounded-full font-mono bg-red-500 text-white font-bold animate-pulse">
                  {item.count}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* User Role Switcher & Profile footer */}
      <div className="p-3 border-t border-slate-800/80 bg-slate-950/50 space-y-2">
        <div className="flex items-center justify-between text-[11px] text-slate-400 px-1">
          <span>Active Role:</span>
          <select
            value={user?.role || 'Administrator'}
            onChange={(e) => switchRole(e.target.value as any)}
            className="bg-slate-800 border border-slate-700 text-slate-200 text-[11px] rounded px-1.5 py-0.5 focus:outline-none focus:border-brand-500"
          >
            <option value="Administrator">Administrator</option>
            <option value="IT Manager">IT Manager</option>
            <option value="Service Desk Agent">Service Desk Agent</option>
            <option value="End User">End User</option>
          </select>
        </div>

        <div className="flex items-center justify-between pt-1">
          <div
            onClick={onOpenProfile}
            className="flex items-center gap-2 overflow-hidden cursor-pointer hover:opacity-80 transition flex-1"
            title="Click to view full Profile Info & Permissions"
          >
            <div className="w-7 h-7 rounded-full bg-brand-500/20 border border-brand-500/40 flex items-center justify-center text-brand-300 font-bold text-xs shrink-0">
              {user?.full_name ? user.full_name.charAt(0) : 'A'}
            </div>
            <div className="truncate">
              <p className="text-xs font-medium text-slate-200 truncate">{user?.full_name || 'Administrator'}</p>
              <p className="text-[10px] text-slate-500 truncate">{user?.job_title || 'Ops Lead'}</p>
            </div>
          </div>
          <button
            onClick={() => {
              logout();
              if (onOpenLogin) onOpenLogin();
            }}
            title="Logout / Switch User"
            className="text-slate-400 hover:text-red-400 p-1 rounded hover:bg-slate-800 transition"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </aside>
  );
};
