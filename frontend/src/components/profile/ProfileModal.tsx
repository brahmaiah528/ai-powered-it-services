import React from 'react';
import { Shield, User as UserIcon, Mail, Briefcase, Building, CheckCircle, X, Key, LogOut, Award, RefreshCw } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { Badge } from '../common/Badge';

interface ProfileModalProps {
  isOpen: boolean;
  onClose: () => void;
  onOpenLogin: () => void;
}

export const ProfileModal: React.FC<ProfileModalProps> = ({ isOpen, onClose, onOpenLogin }) => {
  const { user, logout, switchRole } = useAuth();

  if (!isOpen || !user) return null;

  const getRoleBadgeColor = (role: string): 'default' | 'p1' | 'p2' | 'p3' | 'p4' | 'success' | 'warning' | 'danger' | 'info' | 'neutral' => {
    switch (role) {
      case 'Administrator':
        return 'danger';
      case 'SRE Lead':
        return 'info';
      case 'IT Manager':
        return 'warning';
      case 'Service Desk Agent':
        return 'info';
      default:
        return 'neutral';
    }
  };

  const getPermissionsForRole = (role: string) => {
    switch (role) {
      case 'Administrator':
        return [
          { name: 'Full System Administration & User Provisioning', allowed: true },
          { name: 'SLA Policy Configuration & Matrix Override', allowed: true },
          { name: 'Global Audit Log Inspection & Security Compliance', allowed: true },
          { name: 'Jenkins CI/CD Trigger & Docker Orchestration', allowed: true },
          { name: 'CAB Change Approval & Rollback Authorizations', allowed: true },
          { name: 'Incident Desk Triage & Root Cause Investigation', allowed: true },
        ];
      case 'IT Manager':
        return [
          { name: 'Executive Operations KPI & MTTR Tracking', allowed: true },
          { name: 'CAB Change Approval & Rollback Authorizations', allowed: true },
          { name: 'Department Service Request Approvals', allowed: true },
          { name: 'SLA Breach Review & Reporting Escalation', allowed: true },
          { name: 'Incident Desk Oversight & Reassignment', allowed: true },
          { name: 'Global System Configuration Editing', allowed: false },
        ];
      case 'SRE Lead':
        return [
          { name: 'Infrastructure Real-Time Telemetry & Alert Feeds', allowed: true },
          { name: 'Metric Spike Fault Injection Testing (>90% CPU)', allowed: true },
          { name: 'Jenkins 11-Stage CI/CD Trigger & Hotfix Rollouts', allowed: true },
          { name: 'Jira Issue Synchronization & Commit Tracking', allowed: true },
          { name: 'Critical P1 Incident Diagnosis & Runbook Execution', allowed: true },
          { name: 'User Account Creation & Password Resets', allowed: false },
        ];
      case 'Service Desk Agent':
        return [
          { name: 'Incident Intake, Categorization & Priority Assignment', allowed: true },
          { name: 'Cognitive AI Diagnostic Runbook Execution', allowed: true },
          { name: 'Status Transitions (Assigned -> In Progress -> Resolved)', allowed: true },
          { name: 'Internal Work Notes & Knowledge Base Authoring', allowed: true },
          { name: 'Jira Cloud Ticket Creation & Synchronization', allowed: true },
          { name: 'CAB Change Proposal Approval Authorization', allowed: false },
        ];
      default: // End User
        return [
          { name: 'Self-Service Incident Ticket Reporting', allowed: true },
          { name: 'Service Request Submission (Hardware, IAM, SaaS)', allowed: true },
          { name: 'Personal Ticket SLA Countdown Tracking', allowed: true },
          { name: 'Knowledge Base & Runbook Search Access', allowed: true },
          { name: 'Triage Other Users’ Incident Queues', allowed: false },
          { name: 'Infrastructure Telemetry Monitoring & Spikes', allowed: false },
        ];
    }
  };

  const permissions = getPermissionsForRole(user.role);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fadeIn">
      <div className="w-full max-w-xl bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden">
        
        {/* Modal Header */}
        <div className="p-5 border-b border-slate-800 flex items-center justify-between bg-slate-950/40">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-brand-600/20 border border-brand-500/30 flex items-center justify-center text-brand-400 font-bold">
              <UserIcon className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-sm font-bold text-slate-100">{user.full_name}</h2>
              <p className="text-xs text-slate-400">{user.email}</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-slate-200 transition"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Body Content */}
        <div className="p-6 space-y-5 max-h-[75vh] overflow-y-auto">
          
          {/* User Meta Information Grid */}
          <div className="grid grid-cols-2 gap-3 bg-slate-950/60 p-4 rounded-xl border border-slate-800/80">
            <div>
              <span className="text-[11px] text-slate-400 block">Current Persona / Role</span>
              <div className="mt-1">
                <Badge variant={getRoleBadgeColor(user.role)} className="text-xs font-semibold">
                  <Shield className="w-3 h-3 mr-1" />
                  {user.role}
                </Badge>
              </div>
            </div>

            <div>
              <span className="text-[11px] text-slate-400 block">Username</span>
              <span className="text-xs font-mono font-medium text-slate-200 mt-1 block">@{user.username}</span>
            </div>

            <div>
              <span className="text-[11px] text-slate-400 block">Job Title</span>
              <span className="text-xs font-medium text-slate-200 mt-1 flex items-center gap-1">
                <Briefcase className="w-3 h-3 text-slate-400" />
                {user.job_title || 'Systems Specialist'}
              </span>
            </div>

            <div>
              <span className="text-[11px] text-slate-400 block">Department</span>
              <span className="text-xs font-medium text-slate-200 mt-1 flex items-center gap-1">
                <Building className="w-3 h-3 text-slate-400" />
                {user.department_name || 'Information Technology'}
              </span>
            </div>
          </div>

          {/* Role Capabilities & RBAC Matrix */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-1.5">
                <Award className="w-3.5 h-3.5 text-brand-400" />
                Active Role Permissions & RBAC Scope
              </h3>
              <span className="text-[10px] text-slate-500">JWT Token Enforced</span>
            </div>

            <div className="space-y-1.5 bg-slate-950/40 p-3 rounded-xl border border-slate-800">
              {permissions.map((perm, idx) => (
                <div key={idx} className="flex items-center justify-between text-xs py-1">
                  <span className={perm.allowed ? 'text-slate-200' : 'text-slate-500 line-through'}>
                    {perm.name}
                  </span>
                  {perm.allowed ? (
                    <span className="flex items-center gap-1 text-[11px] text-emerald-400 font-medium">
                      <CheckCircle className="w-3.5 h-3.5" />
                      Allowed
                    </span>
                  ) : (
                    <span className="flex items-center gap-1 text-[11px] text-slate-500 font-medium">
                      <X className="w-3.5 h-3.5" />
                      Restricted
                    </span>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Quick Switch Persona Buttons */}
          <div>
            <span className="text-[11px] text-slate-400 font-semibold block mb-2">Instant Role Switching:</span>
            <div className="grid grid-cols-2 gap-2">
              {[
                { role: 'Administrator' as const, label: 'Administrator', icon: '👑' },
                { role: 'IT Manager' as const, label: 'IT Manager', icon: '💼' },
                { role: 'Service Desk Agent' as const, label: 'Service Desk Agent', icon: '🎧' },
                { role: 'End User' as const, label: 'End User', icon: '👤' },
              ].map((item) => (
                <button
                  key={item.role}
                  type="button"
                  onClick={() => switchRole(item.role)}
                  className={`p-2 rounded-lg text-xs font-medium border transition flex items-center gap-2 ${
                    user.role === item.role
                      ? 'bg-brand-600 text-white border-brand-500'
                      : 'bg-slate-800 hover:bg-slate-700 text-slate-300 border-slate-700'
                  }`}
                >
                  <span>{item.icon}</span>
                  <span>{item.label}</span>
                </button>
              ))}
            </div>
          </div>

        </div>

        {/* Modal Footer */}
        <div className="p-4 border-t border-slate-800 bg-slate-950/60 flex items-center justify-between">
          <button
            type="button"
            onClick={() => {
              onClose();
              onOpenLogin();
            }}
            className="text-xs text-brand-400 hover:text-brand-300 font-semibold flex items-center gap-1.5 transition"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            Switch Account / Login Portal
          </button>

          <button
            type="button"
            onClick={() => {
              logout();
              onClose();
              onOpenLogin();
            }}
            className="px-3 py-1.5 rounded-lg bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/30 text-xs font-semibold flex items-center gap-1.5 transition"
          >
            <LogOut className="w-3.5 h-3.5" />
            Sign Out
          </button>
        </div>

      </div>
    </div>
  );
};
