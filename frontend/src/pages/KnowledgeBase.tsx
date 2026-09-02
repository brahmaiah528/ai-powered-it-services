import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { KnowledgeArticle } from '../types';
import { BookOpen, Search, ThumbsUp, Eye, Tag, ChevronDown, ChevronUp } from 'lucide-react';
import { Badge } from '../components/common/Badge';

export const KnowledgeBase: React.FC = () => {
  const [articles, setArticles] = useState<KnowledgeArticle[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [expandedId, setExpandedId] = useState<number | null>(null);

  useEffect(() => {
    loadArticles();
  }, [search, selectedCategory]);

  const loadArticles = async () => {
    setLoading(true);
    try {
      const params: Record<string, string> = {};
      if (search) params.search = search;
      if (selectedCategory) params.category = selectedCategory;
      const data = await api.getKnowledgeArticles(params);
      setArticles(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleHelpful = async (id: number) => {
    try {
      const res = await api.markArticleHelpful(id);
      setArticles((prev) =>
        prev.map((a) => (a.id === id ? { ...a, helpful_count: res.helpful_count } : a))
      );
    } catch (e) {
      console.error(e);
    }
  };

  const categories = ['', 'Database', 'Authentication', 'Infrastructure', 'Network', 'Security', 'Cloud', 'Software', 'Hardware'];

  return (
    <div className="space-y-6 pb-12">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-brand-400" />
            <span>ITSM Diagnostic Knowledge Base & Runbooks</span>
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Verified step-by-step diagnostic runbooks, resolution guides, and automated AI references.
          </p>
        </div>
      </div>

      {/* Search & Category Filter */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 text-xs">
        <div className="flex-1 relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search runbooks by symptom, error code, or keyword (VPN, deadlock, SSL...)"
            className="w-full bg-slate-800 border border-slate-700 rounded-lg pl-9 pr-4 py-2 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-brand-500"
          />
        </div>

        <div className="flex items-center gap-2 overflow-x-auto pb-1 sm:pb-0">
          {categories.map((c) => (
            <button
              key={c}
              onClick={() => setSelectedCategory(c)}
              className={`px-3 py-1.5 rounded-lg border whitespace-nowrap font-medium transition ${
                selectedCategory === c
                  ? 'bg-brand-600 text-white border-brand-500 shadow'
                  : 'bg-slate-800 border-slate-700 text-slate-300 hover:text-white'
              }`}
            >
              {c || 'All Categories'}
            </button>
          ))}
        </div>
      </div>

      {/* Articles List */}
      <div className="space-y-3">
        {loading ? (
          <div className="text-center py-12 text-slate-400 text-xs">Loading knowledge articles...</div>
        ) : articles.length === 0 ? (
          <div className="text-center py-12 text-slate-400 text-xs">No articles found matching your query.</div>
        ) : (
          articles.map((art) => {
            const isExpanded = expandedId === art.id;
            return (
              <div
                key={art.id}
                className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3 hover:border-slate-700 transition"
              >
                <div
                  onClick={() => setExpandedId(isExpanded ? null : art.id)}
                  className="flex items-start justify-between gap-3 cursor-pointer"
                >
                  <div>
                    <div className="flex items-center gap-2.5 mb-1">
                      <span className="font-mono text-xs font-bold text-brand-400">{art.article_number}</span>
                      <Badge variant="neutral">{art.category}</Badge>
                      <div className="flex items-center gap-3 text-[11px] text-slate-500 font-mono">
                        <span className="flex items-center gap-1"><Eye className="w-3 h-3" /> {art.views_count} views</span>
                        <span className="flex items-center gap-1 text-emerald-400"><ThumbsUp className="w-3 h-3" /> {art.helpful_count} helpful</span>
                      </div>
                    </div>
                    <h3 className="text-sm font-bold text-slate-100">{art.title}</h3>
                    <p className="text-xs text-slate-400 mt-1">{art.problem_summary}</p>
                  </div>

                  <button className="text-slate-400 hover:text-slate-200 p-1">
                    {isExpanded ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
                  </button>
                </div>

                {isExpanded && (
                  <div className="pt-3 border-t border-slate-800/80 space-y-3 text-xs animate-fadeIn">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
                        <span className="font-bold text-amber-400 uppercase text-[10px] block mb-1">Symptoms & Trigger:</span>
                        <p className="text-slate-300 font-mono text-[11px]">{art.symptoms}</p>
                      </div>

                      <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
                        <span className="font-bold text-indigo-400 uppercase text-[10px] block mb-1">Root Cause:</span>
                        <p className="text-slate-300 font-mono text-[11px]">{art.cause}</p>
                      </div>
                    </div>

                    <div className="bg-slate-950 p-3.5 rounded-lg border border-slate-800">
                      <span className="font-bold text-emerald-400 uppercase text-[10px] block mb-1.5">Resolution Runbook Steps:</span>
                      <p className="text-slate-200 font-mono text-[11px] whitespace-pre-line leading-relaxed">
                        {art.resolution}
                      </p>
                    </div>

                    <div className="flex items-center justify-between pt-1">
                      <div className="flex items-center gap-1.5">
                        <Tag className="w-3 h-3 text-slate-500" />
                        <span className="text-[10px] text-slate-400 font-mono">{art.tags || 'runbook, diagnostic'}</span>
                      </div>

                      <button
                        onClick={() => handleHelpful(art.id)}
                        className="bg-slate-800 hover:bg-slate-700 text-emerald-400 font-semibold text-xs px-3 py-1.5 rounded-lg flex items-center gap-1.5 border border-slate-700 transition"
                      >
                        <ThumbsUp className="w-3.5 h-3.5" />
                        <span>Helpful ({art.helpful_count})</span>
                      </button>
                    </div>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
