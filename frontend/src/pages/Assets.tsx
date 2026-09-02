import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { Asset } from '../types';
import { Server, Plus, Search, HardDrive, Laptop, Router, Cpu, ShieldCheck } from 'lucide-react';
import { Badge } from '../components/common/Badge';
import { Modal } from '../components/common/Modal';

export const Assets: React.FC = () => {
  const [assets, setAssets] = useState<Asset[]>([]);
  const [loading, setLoading] = useState(true);
  const [typeFilter, setTypeFilter] = useState('');
  const [isNewOpen, setIsNewOpen] = useState(false);

  // Form state
  const [assetTag, setAssetTag] = useState('');
  const [assetName, setAssetName] = useState('');
  const [assetType, setAssetType] = useState('Server');
  const [owner, setOwner] = useState('');
  const [department, setDepartment] = useState('DevOps & Site Reliability');
  const [ipAddress, setIpAddress] = useState('');

  useEffect(() => {
    loadAssets();
  }, []);

  const loadAssets = async () => {
    setLoading(true);
    try {
      const data = await api.getAssets();
      setAssets(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!assetTag || !assetName) return;
    try {
      await api.createAsset({
        asset_tag: assetTag,
        asset_name: assetName,
        asset_type: assetType,
        owner,
        department,
        ip_address: ipAddress,
        status: 'Active',
      });
      setAssetTag('');
      setAssetName('');
      setOwner('');
      setIpAddress('');
      setIsNewOpen(false);
      loadAssets();
    } catch (e) {
      console.error(e);
    }
  };

  const filteredAssets = typeFilter
    ? assets.filter((a) => a.asset_type === typeFilter)
    : assets;

  return (
    <div className="space-y-6 pb-12">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <Server className="w-5 h-5 text-brand-400" />
            <span>IT Asset Management & CMDB</span>
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Centralized configuration management database tracking servers, cloud instances, databases, and laptops.
          </p>
        </div>

        <button
          onClick={() => setIsNewOpen(true)}
          className="bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold px-3.5 py-2 rounded-lg flex items-center gap-1.5 shadow-md shadow-brand-600/20 transition"
        >
          <Plus className="w-4 h-4" />
          <span>Add CMDB Asset</span>
        </button>
      </div>

      {/* Type Filter Pills */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1 text-xs">
        {['', 'Database server', 'Server', 'Cloud instance', 'Laptop', 'Router', 'Switch', 'Application'].map((t) => (
          <button
            key={t}
            onClick={() => setTypeFilter(t)}
            className={`px-3 py-1.5 rounded-lg border whitespace-nowrap transition font-medium ${
              typeFilter === t
                ? 'bg-brand-600 text-white border-brand-500 shadow'
                : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-slate-200'
            }`}
          >
            {t || 'All Assets (20)'}
          </button>
        ))}
      </div>

      {/* Asset Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {loading ? (
          <div className="col-span-3 text-center py-12 text-slate-400 text-xs">Loading assets...</div>
        ) : (
          filteredAssets.map((asset) => (
            <div
              key={asset.id}
              className="bg-slate-900 border border-slate-800 rounded-xl p-4.5 space-y-3 hover:border-slate-700 transition"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs font-bold text-brand-400">{asset.asset_tag}</span>
                  <Badge variant="neutral">{asset.asset_type}</Badge>
                </div>
                <Badge variant={asset.status === 'Active' ? 'success' : 'warning'}>{asset.status}</Badge>
              </div>

              <div>
                <h3 className="text-sm font-bold text-slate-100 truncate">{asset.asset_name}</h3>
                <p className="text-[11px] text-slate-400 mt-0.5 truncate">
                  Owner: <span className="text-slate-200">{asset.owner || 'IT Operations'}</span> • {asset.department}
                </p>
              </div>

              <div className="bg-slate-950 p-2.5 rounded-lg border border-slate-800/80 grid grid-cols-2 gap-2 text-[11px] font-mono">
                <div>
                  <span className="text-slate-500 block text-[9px]">IP ADDRESS</span>
                  <span className="text-slate-300">{asset.ip_address || '10.0.4.12'}</span>
                </div>
                <div>
                  <span className="text-slate-500 block text-[9px]">OPERATING SYSTEM</span>
                  <span className="text-slate-300 truncate block">{asset.operating_system || 'Linux Ubuntu'}</span>
                </div>
              </div>

              <div className="flex items-center justify-between text-xs pt-1 border-t border-slate-800/60 text-slate-400">
                <span>Spec: {asset.cpu_cores || 16} vCPU / {asset.ram_gb || 64}GB</span>
                <span className="text-[10px] text-brand-300">Linked Incidents: {asset.linked_incidents_count || 1}</span>
              </div>
            </div>
          ))
        )}
      </div>

      {/* New Asset Modal */}
      <Modal isOpen={isNewOpen} onClose={() => setIsNewOpen(false)} title="Register New CMDB Asset" maxWidth="md">
        <form onSubmit={handleCreate} className="space-y-4 text-xs">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-slate-300 font-medium mb-1">Asset Tag *</label>
              <input
                type="text"
                required
                value={assetTag}
                onChange={(e) => setAssetTag(e.target.value)}
                placeholder="e.g. AST-5021"
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-brand-500"
              />
            </div>
            <div>
              <label className="block text-slate-300 font-medium mb-1">Asset Type</label>
              <select
                value={assetType}
                onChange={(e) => setAssetType(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-brand-500"
              >
                <option value="Server">Server</option>
                <option value="Database server">Database server</option>
                <option value="Cloud instance">Cloud instance</option>
                <option value="Laptop">Laptop</option>
                <option value="Router">Router</option>
                <option value="Switch">Switch</option>
                <option value="Application">Application</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-slate-300 font-medium mb-1">Asset Name *</label>
            <input
              type="text"
              required
              value={assetName}
              onChange={(e) => setAssetName(e.target.value)}
              placeholder="e.g. PostgreSQL Standby Replica 03"
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-brand-500"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-slate-300 font-medium mb-1">Owner / Custodian</label>
              <input
                type="text"
                value={owner}
                onChange={(e) => setOwner(e.target.value)}
                placeholder="e.g. Sarah Connor"
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-brand-500"
              />
            </div>
            <div>
              <label className="block text-slate-300 font-medium mb-1">IP Address</label>
              <input
                type="text"
                value={ipAddress}
                onChange={(e) => setIpAddress(e.target.value)}
                placeholder="e.g. 10.0.4.15"
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-slate-200 focus:outline-none focus:border-brand-500"
              />
            </div>
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
              Register Asset
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
