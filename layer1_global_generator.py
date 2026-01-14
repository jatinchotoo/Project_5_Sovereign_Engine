import React, { useState } from 'react';
import { Layout, Shield, BarChart3, Globe, Database, Cpu, Activity, ExternalLink, ChevronRight } from 'lucide-react';

const App = () => {
  const [activeTab, setActiveTab] = useState('overview');

  const projects = [
    {
      id: 'p1',
      name: 'SaaS Intelligence',
      status: 'Completed',
      tech: 'Power BI / DAX',
      color: 'bg-blue-600',
      icon: <BarChart3 className="w-5 h-5" />,
      desc: 'Revenue recognition and churn analysis for subscription-based models.'
    },
    {
      id: 'p2',
      name: 'Global Alpha',
      status: 'Completed',
      tech: 'Python / Pandas',
      color: 'bg-emerald-600',
      icon: <Globe className="w-5 h-5" />,
      desc: 'Automated portfolio tracking and FX risk assessment.'
    },
    {
      id: 'p3',
      name: 'Lumina Cloud',
      status: 'Completed',
      tech: 'Economics / Modeling',
      color: 'bg-amber-600',
      icon: <Cpu className="w-5 h-5" />,
      desc: 'Cloud infrastructure cost-benefit analysis and resource optimization.'
    },
    {
      id: 'p4',
      name: 'Axiom Settlement',
      status: 'Completed',
      tech: 'Data Logic / SQL',
      color: 'bg-indigo-600',
      icon: <Shield className="w-5 h-5" />,
      desc: 'Interbank reconciliation and transaction clearing security logic.'
    },
    {
      id: 'p5',
      name: 'Sovereign Engine',
      status: 'Active',
      tech: 'Python / Global Fin',
      color: 'bg-rose-600',
      icon: <Database className="w-5 h-5" />,
      desc: 'Global multi-entity consolidation with ZAR reporting and eliminations.'
    }
  ];

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans p-4 md:p-8">
      {/* Header */}
      <div className="max-w-6xl mx-auto mb-8">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-slate-800">Sovereign Command Center</h1>
            <p className="text-slate-500 mt-1">Finance Tech Portfolio | South Africa Headquarters</p>
          </div>
          <div className="flex gap-2">
            <span className="px-3 py-1 bg-white border border-slate-200 rounded-full text-xs font-semibold flex items-center gap-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              Engine Status: Live
            </span>
            <span className="px-3 py-1 bg-slate-800 text-white rounded-full text-xs font-semibold">
              v1.0.4
            </span>
          </div>
        </div>
      </div>

      {/* Main Grid */}
      <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left Col: Projects List */}
        <div className="lg:col-span-1 space-y-4">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-400 mb-2">Portfolio Directory</h2>
          {projects.map((p) => (
            <div key={p.id} className="group bg-white p-4 rounded-xl border border-slate-200 shadow-sm hover:border-slate-400 transition-all cursor-pointer">
              <div className="flex items-start justify-between">
                <div className={`p-2 rounded-lg ${p.color} text-white`}>
                  {p.icon}
                </div>
                <span className="text-[10px] font-bold uppercase py-1 px-2 bg-slate-100 rounded text-slate-500">
                  {p.tech}
                </span>
              </div>
              <h3 className="font-bold mt-3 text-slate-800">{p.name}</h3>
              <p className="text-xs text-slate-500 mt-1 line-clamp-2">{p.desc}</p>
              <div className="mt-4 flex items-center text-xs font-bold text-slate-800 opacity-0 group-hover:opacity-100 transition-opacity">
                VIEW REPOSITORY <ChevronRight className="w-3 h-3 ml-1" />
              </div>
            </div>
          ))}
        </div>

        {/* Right Col: Active Project (Sovereign Engine) */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
            <div className="p-6 border-b border-slate-100 flex items-center justify-between bg-slate-800 text-white">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-rose-500 rounded-lg">
                  <Database className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="font-bold">Project 5: Sovereign Engine</h3>
                  <p className="text-xs opacity-70">Global Consolidation Pipeline</p>
                </div>
              </div>
              <Activity className="w-5 h-5 text-rose-400" />
            </div>
            
            <div className="p-8">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
                <div className="space-y-4">
                  <h4 className="text-xs font-bold text-slate-400 uppercase">Live Entity Status</h4>
                  <div className="space-y-2">
                    {['Sovereign USA (USD)', 'Sovereign UK (GBP)', 'Sovereign SA (ZAR)'].map(e => (
                      <div key={e} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-100">
                        <span className="text-sm font-medium">{e}</span>
                        <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="p-6 bg-slate-900 rounded-2xl text-white flex flex-col justify-center">
                  <span className="text-xs font-bold text-rose-400 uppercase">Group Reporting Currency</span>
                  <h2 className="text-4xl font-bold mt-2">ZAR (Rand)</h2>
                  <p className="text-sm opacity-50 mt-1">Multi-entity FX translation active</p>
                </div>
              </div>

              <div className="bg-amber-50 border border-amber-200 p-4 rounded-xl">
                <h4 className="text-sm font-bold text-amber-800 flex items-center gap-2">
                  <Shield className="w-4 h-4" /> Elimination Logic Active
                </h4>
                <p className="text-xs text-amber-700 mt-1">
                  All Account 2000 (Intercompany) transactions are being flagged and removed from the group P&L automatically to prevent revenue inflation.
                </p>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
              <p className="text-xs font-bold text-slate-400 uppercase">Project 6 Goal</p>
              <p className="text-sm font-medium mt-2">Merge all 5 project APIs into this single command center for ultimate portfolio visibility.</p>
            </div>
            <div className="bg-slate-800 p-6 rounded-2xl text-white flex items-center justify-between">
              <div>
                <p className="text-xs font-bold opacity-50 uppercase">Ready for</p>
                <p className="text-lg font-bold">Consolidation</p>
              </div>
              <div className="p-3 bg-white/10 rounded-full">
                <ChevronRight className="w-6 h-6" />
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};

export default App;
