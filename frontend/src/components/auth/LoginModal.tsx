import React, { useState } from 'react';
import { Shield, Key, UserCheck, Lock, ArrowRight, CheckCircle2, Server, Terminal, HelpCircle } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

interface LoginModalProps {
  isOpen: boolean;
  onClose?: () => void;
}

export const LoginModal: React.FC<LoginModalProps> = ({ isOpen, onClose }) => {
  const { login, isLoading } = useAuth();
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('admin123');
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleLoginSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      await login(username, password);
      if (onClose) onClose();
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Authentication failed. Please check credentials.');
    }
  };

  const handleQuickRoleLogin = async (uname: string, pwd: string) => {
    setUsername(uname);
    setPassword(pwd);
    setError(null);
    try {
      await login(uname, pwd);
      if (onClose) onClose();
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Authentication failed.');
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fadeIn">
      <div className="w-full max-w-2xl bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden flex flex-col md:flex-row">
        
        {/* Left Side: Role Quick Selection Panel */}
        <div className="w-full md:w-5/12 bg-slate-950/60 p-6 border-b md:border-b-0 md:border-r border-slate-800 flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 rounded-lg bg-brand-600 flex items-center justify-center text-white font-bold">
                <Terminal className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-xs font-bold uppercase tracking-wider text-brand-400">Enterprise ITSM</h3>
                <p className="text-[11px] text-slate-400">Role Authentication</p>
              </div>
            </div>

            <p className="text-xs text-slate-300 mb-3 font-semibold">One-Click Persona Login:</p>

            <div className="space-y-2">
              {[
                {
                  role: 'Administrator',
                  name: 'Marcus Vance',
                  uname: 'admin',
                  pwd: 'admin123',
                  badge: 'bg-red-500/20 text-red-400 border-red-500/30',
                  desc: 'Full system, audit & DevOps pipeline authority',
                },
                {
                  role: 'IT Manager',
                  name: 'Elena Rostova',
                  uname: 'itmanager',
                  pwd: 'admin123',
                  badge: 'bg-amber-500/20 text-amber-400 border-amber-500/30',
                  desc: 'CAB change reviews, SLA metrics & approvals',
                },
                {
                  role: 'Service Desk Agent',
                  name: 'Sarah Connor',
                  uname: 'srelead',
                  pwd: 'admin123',
                  badge: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
                  desc: 'Triage incidents, execute AI runbooks & Jira sync',
                },
                {
                  role: 'End User',
                  name: 'Alex Morgan',
                  uname: 'user1',
                  pwd: 'admin123',
                  badge: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
                  desc: 'Self-service ticketing & hardware/IAM requests',
                },
              ].map((item) => (
                <button
                  key={item.uname}
                  type="button"
                  onClick={() => handleQuickRoleLogin(item.uname, item.pwd)}
                  className="w-full text-left p-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 hover:border-slate-700 transition flex flex-col gap-1 group"
                >
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold text-slate-200 group-hover:text-brand-400 transition">
                      {item.role}
                    </span>
                    <span className={`text-[10px] px-1.5 py-0.5 rounded border font-mono ${item.badge}`}>
                      {item.uname}
                    </span>
                  </div>
                  <p className="text-[10px] text-slate-400 leading-tight">{item.desc}</p>
                </button>
              ))}
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-slate-800/80 text-[10px] text-slate-500 flex items-center justify-between">
            <span>Demo credentials pre-filled</span>
            <span className="text-emerald-400">JWT Enabled</span>
          </div>
        </div>

        {/* Right Side: Standard Login Form */}
        <div className="w-full md:w-7/12 p-6 flex flex-col justify-between">
          <div>
            <div className="mb-5">
              <h2 className="text-base font-bold text-slate-100">Sign in to IT Service Desk</h2>
              <p className="text-xs text-slate-400 mt-0.5">Enter enterprise single sign-on or local credentials</p>
            </div>

            {error && (
              <div className="mb-4 p-3 rounded-lg bg-red-500/10 border border-red-500/30 text-red-400 text-xs flex items-center gap-2">
                <Lock className="w-4 h-4 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            <form onSubmit={handleLoginSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Username or Email</label>
                <div className="relative">
                  <UserCheck className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
                  <input
                    type="text"
                    required
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="e.g. admin or user1"
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-9 pr-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Password</label>
                <div className="relative">
                  <Key className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
                  <input
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Enter password (default: admin123)"
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-9 pr-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full mt-2 bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold py-2.5 rounded-lg flex items-center justify-center gap-2 shadow-lg shadow-brand-600/20 transition disabled:opacity-50"
              >
                {isLoading ? (
                  <>
                    <div className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span>Authenticating...</span>
                  </>
                ) : (
                  <>
                    <span>Authenticate & Access Console</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </form>
          </div>

          <div className="mt-6 pt-4 border-t border-slate-800 text-[11px] text-slate-400 flex items-center justify-between">
            <span className="flex items-center gap-1">
              <Shield className="w-3.5 h-3.5 text-brand-400" />
              Role-Based Access (RBAC)
            </span>
            {onClose && (
              <button
                type="button"
                onClick={onClose}
                className="text-slate-400 hover:text-slate-200 transition underline text-[11px]"
              >
                Close
              </button>
            )}
          </div>
        </div>

      </div>
    </div>
  );
};
