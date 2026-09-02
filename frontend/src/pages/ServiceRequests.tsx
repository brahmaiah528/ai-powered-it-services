import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { ServiceRequest } from '../types';
import { FileCheck2, Plus, CheckCircle2, Clock, Check, X } from 'lucide-react';
import { Badge } from '../components/common/Badge';
import { Modal } from '../components/common/Modal';

interface ServiceRequestsProps {
  isOpenNewModal: boolean;
  onCloseNewModal: () => void;
}

export const ServiceRequests: React.FC<ServiceRequestsProps> = ({
  isOpenNewModal,
  onCloseNewModal,
}) => {
  const [requests, setRequests] = useState<ServiceRequest[]>([]);
  const [loading, setLoading] = useState(true);

  // Form State
  const [title, setTitle] = useState('');
  const [requestType, setRequestType] = useState('VPN access');
  const [description, setDescription] = useState('');
  const [urgency, setUrgency] = useState('Medium');
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    loadRequests();
  }, []);

  const loadRequests = async () => {
    setLoading(true);
    try {
      const data = await api.getServiceRequests();
      setRequests(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title || !description) return;
    setIsSubmitting(true);
    try {
      await api.createServiceRequest({
        title,
        request_type: requestType,
        description,
        urgency,
      });
      setTitle('');
      setDescription('');
      onCloseNewModal();
      loadRequests();
    } catch (e) {
      console.error(e);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleUpdateStatus = async (id: number, status: any) => {
    try {
      await api.updateServiceRequest(id, { status });
      loadRequests();
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="space-y-6 pb-12">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <FileCheck2 className="w-5 h-5 text-brand-400" />
            <span>Service Request Catalog & Fulfillment</span>
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Manage user provisioning, hardware requests, VPN access, and approval workflows.
          </p>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="bg-slate-950/60 border-b border-slate-800 text-slate-400 font-semibold uppercase text-[10px]">
                <th className="py-3 px-4">Request ID</th>
                <th className="py-3 px-4">Title & Request Type</th>
                <th className="py-3 px-4">Requester</th>
                <th className="py-3 px-4">Urgency</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4">Assigned To</th>
                <th className="py-3 px-4 text-right">Approval Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {loading ? (
                <tr>
                  <td colSpan={7} className="text-center py-12 text-slate-400">Loading requests...</td>
                </tr>
              ) : (
                requests.map((r) => (
                  <tr key={r.id} className="hover:bg-slate-800/40 transition">
                    <td className="py-3 px-4 font-mono font-bold text-brand-400 whitespace-nowrap">
                      {r.request_number}
                    </td>
                    <td className="py-3 px-4 max-w-[260px]">
                      <span className="font-semibold text-slate-200 block truncate">{r.title}</span>
                      <span className="text-[10px] text-slate-400">{r.request_type}</span>
                    </td>
                    <td className="py-3 px-4 text-slate-300 whitespace-nowrap">
                      {r.requester_name || 'Enterprise User'}
                    </td>
                    <td className="py-3 px-4 whitespace-nowrap">
                      <Badge variant={r.urgency === 'High' ? 'p2' : 'neutral'}>{r.urgency}</Badge>
                    </td>
                    <td className="py-3 px-4 whitespace-nowrap">
                      <Badge variant={r.status === 'Completed' ? 'success' : r.status === 'Approved' ? 'info' : 'warning'}>
                        {r.status}
                      </Badge>
                    </td>
                    <td className="py-3 px-4 text-slate-300 whitespace-nowrap">
                      {r.assigned_to || <span className="text-slate-500 italic">Unassigned</span>}
                    </td>
                    <td className="py-3 px-4 text-right whitespace-nowrap space-x-1.5">
                      {r.status === 'Submitted' || r.status === 'Pending Approval' ? (
                        <>
                          <button
                            onClick={() => handleUpdateStatus(r.id, 'Approved')}
                            className="bg-emerald-600/80 hover:bg-emerald-600 text-white text-[11px] font-semibold px-2 py-1 rounded transition"
                          >
                            Approve
                          </button>
                          <button
                            onClick={() => handleUpdateStatus(r.id, 'Rejected')}
                            className="bg-red-600/80 hover:bg-red-600 text-white text-[11px] font-semibold px-2 py-1 rounded transition"
                          >
                            Reject
                          </button>
                        </>
                      ) : r.status === 'Approved' || r.status === 'In Progress' ? (
                        <button
                          onClick={() => handleUpdateStatus(r.id, 'Completed')}
                          className="bg-brand-600 hover:bg-brand-500 text-white text-[11px] font-semibold px-2.5 py-1 rounded shadow transition"
                        >
                          Complete
                        </button>
                      ) : (
                        <span className="text-slate-500 text-[11px]">Fulfillment Done</span>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* New Service Request Modal */}
      <Modal
        isOpen={isOpenNewModal}
        onClose={onCloseNewModal}
        title="Submit New Service Request"
        maxWidth="lg"
      >
        <form onSubmit={handleCreate} className="space-y-4 text-xs">
          <div>
            <label className="block text-slate-300 font-medium mb-1">Request Title *</label>
            <input
              type="text"
              required
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Request GPU workstation allocation for AI training"
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-brand-500"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-slate-300 font-medium mb-1">Request Type</label>
              <select
                value={requestType}
                onChange={(e) => setRequestType(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-brand-500"
              >
                <option value="Password reset">Password reset</option>
                <option value="Software installation">Software installation</option>
                <option value="Hardware request">Hardware request</option>
                <option value="New user account">New user account</option>
                <option value="VPN access">VPN access</option>
                <option value="Email access">Email access</option>
                <option value="System access">System access</option>
                <option value="Laptop request">Laptop request</option>
              </select>
            </div>
            <div>
              <label className="block text-slate-300 font-medium mb-1">Urgency</label>
              <select
                value={urgency}
                onChange={(e) => setUrgency(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-brand-500"
              >
                <option value="High">High</option>
                <option value="Medium">Medium</option>
                <option value="Low">Low</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-slate-300 font-medium mb-1">Business Justification & Details *</label>
            <textarea
              required
              rows={3}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="State reason, project name, or hardware specifications needed..."
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-brand-500"
            />
          </div>

          <div className="flex items-center justify-end gap-2 pt-2">
            <button
              type="button"
              onClick={onCloseNewModal}
              className="bg-slate-800 text-slate-300 px-4 py-2 rounded-lg font-medium"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="bg-brand-600 hover:bg-brand-500 text-white font-semibold px-5 py-2 rounded-lg shadow"
            >
              Submit Request
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
