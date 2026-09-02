import React, { useState } from 'react';
import { Search, Bell, Plus, Sparkles, Check, ExternalLink, Shield } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useNotifications } from '../../context/NotificationContext';
import { Badge } from '../common/Badge';

interface TopbarProps {
  searchQuery: string;
  onSearchChange: (q: string) => void;
  onOpenNewIncident: () => void;
  onOpenNewRequest: () => void;
  onNavigateTab: (tab: string) => void;
}

export const Topbar: React.FC<TopbarProps> = ({
  searchQuery,
  onSearchChange,
  onOpenNewIncident,
  onOpenNewRequest,
  onNavigateTab,
}) => {
  const { user, switchRole } = useAuth();
  const { notifications, unreadCount, markAsRead, markAllAsRead } = useNotifications();
  const [showNotifications, setShowNotifications] = useState(false);
  const [showPersonaMenu, setShowPersonaMenu] = useState(false);

  return (
    <header className="h-16 border-b border-slate-800 bg-slate-900/80 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-20">
      {/* Search Bar */}
      <div className="flex-1 max-w-xl relative">
        <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => onSearchChange(e.target.value)}
          placeholder="Global Search (INC-1025, Database-01, ITSM-245, VPN, CPU...)"
          className="w-full bg-slate-800/80 border border-slate-700/80 rounded-lg pl-9 pr-4 py-1.5 text-xs text-slate-200 placeholder-slate-400 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition"
        />
      </div>

      {/* Right Controls */}
      <div className="flex items-center gap-4">
        {/* Demo Mode Badge */}
        <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-[11px] font-medium text-emerald-400">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span>Demo / Simulation Mode</span>
        </div>

        {/* Quick Actions */}
        <div className="flex items-center gap-2">
          <button
            onClick={onOpenNewIncident}
            className="bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold px-3 py-1.5 rounded-lg flex items-center gap-1.5 shadow-md shadow-brand-600/20 transition"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>New Incident</span>
          </button>
          
          <button
            onClick={onOpenNewRequest}
            className="hidden md:flex bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-medium px-3 py-1.5 rounded-lg items-center gap-1.5 transition"
          >
            <Plus className="w-3.5 h-3.5 text-slate-400" />
            <span>Service Request</span>
          </button>
        </div>

        {/* Notification Bell with Dropdown */}
        <div className="relative">
          <button
            onClick={() => setShowNotifications(!showNotifications)}
            className="relative p-2 rounded-lg bg-slate-800/80 hover:bg-slate-700 text-slate-300 transition"
          >
            <Bell className="w-4 h-4" />
            {unreadCount > 0 && (
              <span className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 text-white rounded-full text-[9px] font-bold flex items-center justify-center">
                {unreadCount}
              </span>
            )}
          </button>

          {showNotifications && (
            <div className="absolute right-0 mt-2 w-80 sm:w-96 bg-slate-900 border border-slate-800 rounded-xl shadow-2xl z-50 overflow-hidden">
              <div className="p-3 border-b border-slate-800 flex items-center justify-between bg-slate-950/40">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-semibold text-slate-200">Notifications</span>
                  {unreadCount > 0 && (
                    <span className="text-[10px] bg-brand-500/20 text-brand-400 px-1.5 py-0.5 rounded font-mono">
                      {unreadCount} new
                    </span>
                  )}
                </div>
                {unreadCount > 0 && (
                  <button
                    onClick={markAllAsRead}
                    className="text-[11px] text-brand-400 hover:text-brand-300 font-medium"
                  >
                    Mark all read
                  </button>
                )}
              </div>

              <div className="max-h-80 overflow-y-auto divide-y divide-slate-800/50">
                {notifications.length === 0 ? (
                  <div className="p-4 text-center text-xs text-slate-400">No notifications</div>
                ) : (
                  notifications.slice(0, 8).map((n) => (
                    <div
                      key={n.id}
                      onClick={() => markAsRead(n.id)}
                      className={`p-3 text-xs hover:bg-slate-800/50 transition cursor-pointer flex items-start gap-2.5 ${
                        !n.is_read ? 'bg-slate-800/30' : ''
                      }`}
                    >
                      <span className={`w-2 h-2 rounded-full mt-1.5 shrink-0 ${
                        n.severity === 'Critical' ? 'bg-red-500' :
                        n.severity === 'Warning' ? 'bg-amber-400' :
                        n.severity === 'Success' ? 'bg-emerald-400' : 'bg-blue-400'
                      }`} />
                      <div className="flex-1 min-w-0">
                        <p className="font-semibold text-slate-200 truncate">{n.title}</p>
                        <p className="text-slate-400 text-[11px] mt-0.5 line-clamp-2">{n.message}</p>
                      </div>
                    </div>
                  ))
                )}
              </div>

              <div className="p-2 border-t border-slate-800 bg-slate-950/40 text-center">
                <button
                  onClick={() => {
                    setShowNotifications(false);
                    onNavigateTab('notifications');
                  }}
                  className="text-xs text-brand-400 hover:text-brand-300 font-medium"
                >
                  View all notifications
                </button>
              </div>
            </div>
          )}
        </div>

        {/* User Role Pill & Persona Switcher */}
        <div className="relative">
          <button
            onClick={() => setShowPersonaMenu(!showPersonaMenu)}
            className="flex items-center gap-2 pl-2.5 pr-3 py-1 rounded-lg bg-slate-800/80 hover:bg-slate-700 border border-slate-700 text-slate-200 transition text-xs"
            title="Click to Switch Persona / Role"
          >
            <Shield className="w-3.5 h-3.5 text-brand-400" />
            <span className="font-semibold text-slate-200">{user?.role || 'Administrator'}</span>
            <span className="text-[10px] text-slate-400 bg-slate-900/60 px-1.5 py-0.5 rounded border border-slate-700/50">Switch</span>
          </button>

          {showPersonaMenu && (
            <div className="absolute right-0 mt-2 w-72 bg-slate-900 border border-slate-800 rounded-xl shadow-2xl z-50 overflow-hidden">
              <div className="p-3 border-b border-slate-800 bg-slate-950/60">
                <p className="text-xs font-semibold text-slate-200">Switch User Role & Persona</p>
                <p className="text-[11px] text-slate-400 mt-0.5">Test role-specific workflows and permissions</p>
              </div>
              <div className="p-2 space-y-1">
                {[
                  { role: 'Administrator' as const, label: 'Enterprise Administrator', desc: 'Full system & audit authority', badge: 'bg-red-500/20 text-red-400' },
                  { role: 'SRE Lead' as const, label: 'SRE / Incident Commander', desc: 'Telemetry, spikes & DevOps triggers', badge: 'bg-purple-500/20 text-purple-400' },
                  { role: 'Service Desk Agent' as const, label: 'Service Desk Analyst', desc: 'Incident triage & AI runbooks', badge: 'bg-blue-500/20 text-blue-400' },
                  { role: 'CAB Approver' as const, label: 'CAB Board Reviewer', desc: 'RFC risk review & rollback approvals', badge: 'bg-amber-500/20 text-amber-400' },
                  { role: 'Department Manager' as const, label: 'Department Line Manager', desc: 'Service Catalog request approvals', badge: 'bg-emerald-500/20 text-emerald-400' },
                  { role: 'End User' as const, label: 'Standard End-User', desc: 'Self-service ticketing & requests', badge: 'bg-slate-500/20 text-slate-300' },
                ].map((item) => (
                  <button
                    key={item.role}
                    onClick={() => {
                      switchRole(item.role);
                      setShowPersonaMenu(false);
                    }}
                    className={`w-full text-left p-2 rounded-lg text-xs transition flex items-center justify-between ${
                      user?.role === item.role ? 'bg-brand-600/20 border border-brand-500/30' : 'hover:bg-slate-800/60'
                    }`}
                  >
                    <div>
                      <p className="font-semibold text-slate-200">{item.label}</p>
                      <p className="text-[10px] text-slate-400">{item.desc}</p>
                    </div>
                    {user?.role === item.role && <Check className="w-3.5 h-3.5 text-brand-400 shrink-0" />}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

