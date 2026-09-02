import React from 'react';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'p1' | 'p2' | 'p3' | 'p4' | 'success' | 'warning' | 'danger' | 'info' | 'neutral' | 'default';
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({ children, variant = 'default', className = '' }) => {
  const getStyles = () => {
    switch (variant) {
      case 'p1':
      case 'danger':
        return 'bg-red-500/15 text-red-400 border border-red-500/30';
      case 'p2':
      case 'warning':
        return 'bg-amber-500/15 text-amber-400 border border-amber-500/30';
      case 'p3':
        return 'bg-yellow-500/15 text-yellow-300 border border-yellow-500/30';
      case 'p4':
      case 'info':
        return 'bg-blue-500/15 text-blue-400 border border-blue-500/30';
      case 'success':
        return 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30';
      case 'neutral':
        return 'bg-slate-700/40 text-slate-300 border border-slate-600/30';
      default:
        return 'bg-slate-800 text-slate-300 border border-slate-700';
    }
  };

  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold tracking-wide ${getStyles()} ${className}`}>
      {children}
    </span>
  );
};
