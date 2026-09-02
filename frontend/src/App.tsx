import React, { useState } from 'react';
import { useAuth } from './context/AuthContext';
import { Sidebar } from './components/layout/Sidebar';
import { Topbar } from './components/layout/Topbar';
import { ScenarioSimulationModal } from './components/simulation/ScenarioSimulationModal';
import { LoginModal } from './components/auth/LoginModal';
import { ProfileModal } from './components/profile/ProfileModal';

// Pages
import { Dashboard } from './pages/Dashboard';
import { Incidents } from './pages/Incidents';
import { IncidentDetail } from './pages/IncidentDetail';
import { ServiceRequests } from './pages/ServiceRequests';
import { Problems } from './pages/Problems';
import { Changes } from './pages/Changes';
import { Assets } from './pages/Assets';
import { Infrastructure } from './pages/Infrastructure';
import { KnowledgeBase } from './pages/KnowledgeBase';
import { AiDashboard } from './pages/AiDashboard';
import { DevOpsHub } from './pages/DevOpsHub';
import { Reports } from './pages/Reports';
import { AuditLogs } from './pages/AuditLogs';

export const App: React.FC = () => {
  const { user, isLoading } = useAuth();
  const [currentTab, setCurrentTab] = useState<string>('dashboard');
  const [selectedIncidentId, setSelectedIncidentId] = useState<number | null>(null);
  const [globalSearch, setGlobalSearch] = useState<string>('');
  
  // Modals
  const [isScenarioOpen, setIsScenarioOpen] = useState<boolean>(false);
  const [isNewIncidentOpen, setIsNewIncidentOpen] = useState<boolean>(false);
  const [isNewRequestOpen, setIsNewRequestOpen] = useState<boolean>(false);
  const [isLoginOpen, setIsLoginOpen] = useState<boolean>(false);
  const [isProfileOpen, setIsProfileOpen] = useState<boolean>(false);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-slate-950 text-slate-400">
        <div className="flex items-center gap-3">
          <div className="w-6 h-6 border-2 border-brand-500 border-t-transparent rounded-full animate-spin"></div>
          <span className="font-semibold text-sm">Initializing Enterprise ITSM Platform...</span>
        </div>
      </div>
    );
  }

  const handleSelectTab = (tab: string) => {
    setSelectedIncidentId(null);
    setCurrentTab(tab);
  };

  const handleOpenIncidentDetail = (id: number) => {
    setSelectedIncidentId(id);
    setCurrentTab('incidents');
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex">
      {/* Sidebar Navigation */}
      <Sidebar
        currentTab={currentTab}
        onSelectTab={handleSelectTab}
        onOpenSimulation={() => setIsScenarioOpen(true)}
        onOpenProfile={() => setIsProfileOpen(true)}
        onOpenLogin={() => setIsLoginOpen(true)}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col pl-64 min-w-0">
        {/* Topbar */}
        <Topbar
          searchQuery={globalSearch}
          onSearchChange={setGlobalSearch}
          onOpenNewIncident={() => {
            setCurrentTab('incidents');
            setSelectedIncidentId(null);
            setIsNewIncidentOpen(true);
          }}
          onOpenNewRequest={() => {
            setCurrentTab('service-requests');
            setIsNewRequestOpen(true);
          }}
          onNavigateTab={handleSelectTab}
          onOpenProfile={() => setIsProfileOpen(true)}
          onOpenLogin={() => setIsLoginOpen(true)}
        />

        {/* Page Content */}
        <main className="flex-1 p-6 overflow-y-auto">
          {currentTab === 'dashboard' && (
            <Dashboard
              onNavigateTab={handleSelectTab}
              onOpenIncidentDetail={handleOpenIncidentDetail}
              onOpenSimulation={() => setIsScenarioOpen(true)}
            />
          )}

          {currentTab === 'incidents' && (
            selectedIncidentId ? (
              <IncidentDetail
                incidentId={selectedIncidentId}
                onBack={() => setSelectedIncidentId(null)}
                onNavigateTab={handleSelectTab}
              />
            ) : (
              <Incidents
                searchQuery={globalSearch}
                onOpenDetail={handleOpenIncidentDetail}
                isOpenNewModal={isNewIncidentOpen}
                onCloseNewModal={() => setIsNewIncidentOpen(false)}
              />
            )
          )}

          {currentTab === 'service-requests' && (
            <ServiceRequests
              isOpenNewModal={isNewRequestOpen}
              onCloseNewModal={() => setIsNewRequestOpen(false)}
            />
          )}

          {currentTab === 'problems' && <Problems />}

          {currentTab === 'changes' && <Changes />}

          {currentTab === 'assets' && <Assets />}

          {currentTab === 'infrastructure' && <Infrastructure />}

          {currentTab === 'knowledge-base' && <KnowledgeBase />}

          {currentTab === 'ai-assistant' && <AiDashboard />}

          {currentTab === 'devops' && <DevOpsHub />}

          {currentTab === 'reports' && <Reports />}

          {currentTab === 'notifications' && <Reports />}

          {currentTab === 'audit-logs' && <AuditLogs />}
        </main>
      </div>

      {/* 23-Step Scenario Interactive Simulation Modal */}
      <ScenarioSimulationModal
        isOpen={isScenarioOpen}
        onClose={() => setIsScenarioOpen(false)}
        onScenarioCompleted={() => {
          // Trigger refresh if needed
        }}
      />

      {/* Interactive Login Portal Modal */}
      <LoginModal
        isOpen={isLoginOpen}
        onClose={() => setIsLoginOpen(false)}
      />

      {/* User Profile & Permissions Modal */}
      <ProfileModal
        isOpen={isProfileOpen}
        onClose={() => setIsProfileOpen(false)}
        onOpenLogin={() => {
          setIsProfileOpen(false);
          setIsLoginOpen(true);
        }}
      />
    </div>
  );
};
