const API_BASE = '/api';

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem('itsm_token');
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let errorMsg = 'An error occurred';
    try {
      const errData = await response.json();
      errorMsg = errData.detail || errData.message || response.statusText;
    } catch {
      errorMsg = response.statusText;
    }
    throw new ApiError(errorMsg, response.status);
  }

  // If response is CSV or blob, return directly
  const contentType = response.headers.get('content-type');
  if (contentType && contentType.includes('text/csv')) {
    return (await response.text()) as unknown as T;
  }

  return response.json();
}

export const api = {
  // Auth
  login: (data: any) => request<any>('/auth/login', { method: 'POST', body: JSON.stringify(data) }),
  getCurrentUser: () => request<any>('/auth/me'),
  getUsers: () => request<any[]>('/auth/users'),

  // Incidents
  getIncidents: (params?: Record<string, string>) => {
    const searchParams = new URLSearchParams(params);
    return request<any[]>(`/incidents?${searchParams.toString()}`);
  },
  getIncident: (id: number) => request<any>(`/incidents/${id}`),
  createIncident: (data: any) => request<any>('/incidents', { method: 'POST', body: JSON.stringify(data) }),
  updateIncident: (id: number, data: any) => request<any>(`/incidents/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  assignIncident: (id: number, technician_id: number) => request<any>(`/incidents/${id}/assign`, { method: 'POST', body: JSON.stringify({ technician_id }) }),
  resolveIncident: (id: number, data: { resolution_notes: string; root_cause?: string }) => request<any>(`/incidents/${id}/resolve`, { method: 'POST', body: JSON.stringify(data) }),
  reopenIncident: (id: number) => request<any>(`/incidents/${id}/reopen`, { method: 'POST' }),
  closeIncident: (id: number) => request<any>(`/incidents/${id}/close`, { method: 'POST' }),
  getIncidentComments: (id: number) => request<any[]>(`/incidents/${id}/comments`),
  addIncidentComment: (id: number, data: { content: string; is_internal?: boolean }) => request<any>(`/incidents/${id}/comments`, { method: 'POST', body: JSON.stringify(data) }),
  getIncidentHistory: (id: number) => request<any[]>(`/incidents/${id}/history`),

  // Service Requests
  getServiceRequests: (params?: Record<string, string>) => {
    const searchParams = new URLSearchParams(params);
    return request<any[]>(`/service-requests?${searchParams.toString()}`);
  },
  createServiceRequest: (data: any) => request<any>('/service-requests', { method: 'POST', body: JSON.stringify(data) }),
  updateServiceRequest: (id: number, data: any) => request<any>(`/service-requests/${id}`, { method: 'PUT', body: JSON.stringify(data) }),

  // Problems
  getProblems: () => request<any[]>('/problems'),
  createProblem: (data: any) => request<any>('/problems', { method: 'POST', body: JSON.stringify(data) }),
  updateProblem: (id: number, data: any) => request<any>(`/problems/${id}`, { method: 'PUT', body: JSON.stringify(data) }),

  // Changes
  getChanges: () => request<any[]>('/changes'),
  createChange: (data: any) => request<any>('/changes', { method: 'POST', body: JSON.stringify(data) }),
  updateChange: (id: number, data: any) => request<any>(`/changes/${id}`, { method: 'PUT', body: JSON.stringify(data) }),

  // Assets
  getAssets: () => request<any[]>('/assets'),
  createAsset: (data: any) => request<any>('/assets', { method: 'POST', body: JSON.stringify(data) }),
  updateAsset: (id: number, data: any) => request<any>(`/assets/${id}`, { method: 'PUT', body: JSON.stringify(data) }),

  // Infrastructure & Alerts
  getInfrastructure: () => request<any[]>('/infrastructure'),
  simulateMetricSpike: (data: { hostname: string; metric: string; value: number }) => request<any>('/infrastructure/simulate-spike', { method: 'POST', body: JSON.stringify(data) }),
  normalizeNode: (hostname: string) => request<any>(`/infrastructure/normalize/${hostname}`, { method: 'POST' }),
  getAlerts: () => request<any[]>('/infrastructure/alerts'),
  acknowledgeAlert: (id: number) => request<any>(`/infrastructure/alerts/${id}/acknowledge`, { method: 'POST' }),

  // AI Assistant & Ops
  analyzeIncidentAI: (data: any) => request<any>('/ai/analyze-incident', { method: 'POST', body: JSON.stringify(data) }),
  getAIDashboardStats: () => request<any>('/ai/dashboard-stats'),

  // Jira Integration
  getJiraIssues: () => request<any[]>('/jira/issues'),
  createJiraIssue: (data: any) => request<any>('/jira/create-issue', { method: 'POST', body: JSON.stringify(data) }),
  syncJiraIssue: (key: string) => request<any>(`/jira/sync/${key}`, { method: 'POST' }),

  // DevOps Hub
  getDevOpsStatus: () => request<any>('/devops/status'),
  triggerJenkinsBuild: (message?: string) => request<any>('/devops/trigger-build', { method: 'POST', body: JSON.stringify({ message }) }),
  commitFixDevOps: (message?: string) => request<any>('/devops/commit-fix', { method: 'POST', body: JSON.stringify({ message }) }),

  // Knowledge Base
  getKnowledgeArticles: (params?: Record<string, string>) => {
    const searchParams = new URLSearchParams(params);
    return request<any[]>(`/knowledge-base?${searchParams.toString()}`);
  },
  getKnowledgeArticle: (id: number) => request<any>(`/knowledge-base/${id}`),
  markArticleHelpful: (id: number) => request<any>(`/knowledge-base/${id}/helpful`, { method: 'POST' }),

  // Notifications
  getNotifications: () => request<any[]>('/notifications'),
  markNotificationRead: (id: number) => request<any>(`/notifications/${id}/read`, { method: 'POST' }),
  markAllNotificationsRead: () => request<any>('/notifications/mark-all-read', { method: 'POST' }),

  // Reports
  getDashboardKPIs: () => request<any>('/reports/dashboard-kpis'),
  exportCSVUrl: `${API_BASE}/reports/export-csv`,

  // Audit Logs
  getAuditLogs: () => request<any[]>('/audit-logs'),

  // Simulation Runner
  getScenarioSteps: () => request<any>('/simulation/scenario/steps'),
  executeScenarioStep: (step: number) => request<any>(`/simulation/scenario/execute-step/${step}`, { method: 'POST' }),
  resetScenario: () => request<any>('/simulation/scenario/reset', { method: 'POST' }),
};
