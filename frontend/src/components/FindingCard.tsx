import React from 'react'
import { ChevronDown, ChevronUp, Lock } from 'lucide-react'
import { Finding } from '../types'

interface FindingCardProps {
  finding: Finding
  isExpanded: boolean
  onToggleExpand: () => void
  onToggleStatus: (id: string, e: React.MouseEvent) => void
}

export const FindingCard: React.FC<FindingCardProps> = ({
  finding: f,
  isExpanded,
  onToggleExpand,
  onToggleStatus
}) => {
  const isResolved = f.status === 'RESOLVED'

  return (
    <div 
      onClick={onToggleExpand}
      className={`p-5 transition-all cursor-pointer ${isResolved ? 'bg-slate-950/40 opacity-70' : 'hover:bg-slate-800/40'}`}
    >
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-2">
        <div className="flex items-center gap-2.5">
          {isExpanded ? (
            <ChevronUp className="w-4 h-4 text-slate-400 flex-shrink-0" />
          ) : (
            <ChevronDown className="w-4 h-4 text-slate-500 flex-shrink-0" />
          )}
          <h3 className={`text-sm font-bold ${isResolved ? 'line-through text-slate-400' : 'text-white'}`}>
            {f.title}
          </h3>
        </div>
        <div className="flex items-center gap-2 flex-shrink-0">
          <span className={`px-2 py-0.5 rounded-md text-[11px] font-bold ${
            f.severity === 'CRITICAL' ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30' : 
            f.severity === 'HIGH' ? 'bg-orange-500/20 text-orange-400 border border-orange-500/30' : 
            f.severity === 'MEDIUM' ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30' : 
            'bg-blue-500/20 text-blue-400 border border-blue-500/30'
          }`}>
            {f.severity}
          </span>

          <button
            id={`toggle-${f.id}`}
            onClick={(e) => onToggleStatus(f.id, e)}
            className={`text-xs px-2.5 py-1 rounded-lg border font-medium transition-colors cursor-pointer ${
              isResolved 
                ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30 hover:bg-rose-500/10 hover:text-rose-400 hover:border-rose-500/30'
                : 'bg-slate-800 text-slate-300 border-slate-700 hover:bg-emerald-600 hover:text-white hover:border-emerald-500'
            }`}
          >
            {isResolved ? 'Resolved ✓' : 'Mark Resolved'}
          </button>
        </div>
      </div>

      <p className="text-slate-400 text-xs mb-3">{f.description}</p>
      
      <div className="flex flex-wrap items-center gap-2 text-xs">
        {f.is_demo ? (
          <span className="inline-flex items-center gap-1 font-semibold text-fuchsia-400 bg-fuchsia-500/10 border border-fuchsia-500/20 px-2 py-0.5 rounded text-[11px]">
            DEMO SCENARIO
          </span>
        ) : (
          <span className="inline-flex items-center gap-1 font-semibold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded text-[11px]">
            LIVE LOCAL SCAN
          </span>
        )}
        {f.risk_score !== undefined && f.risk_score !== null && (
          <span className="text-slate-400 font-mono text-[11px] bg-slate-800/80 px-2 py-0.5 rounded border border-slate-700/60">
            Risk Score: <span className="text-white font-bold">{f.risk_score}</span>
          </span>
        )}
        {f.category && (
          <span className="text-slate-400 text-[11px] bg-slate-800/40 px-2 py-0.5 rounded">
            {f.category}
          </span>
        )}
        {f.evidence_id && (
          <span className="inline-flex items-center gap-1 text-emerald-400 text-[11px] bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
            <Lock className="w-3 h-3" /> SHA-256 Verified
          </span>
        )}
      </div>

      {/* Expandable Finding Details */}
      {isExpanded && (
        <div className="mt-4 pt-4 border-t border-slate-800 space-y-3 animate-fade-in text-xs bg-slate-950/50 p-3.5 rounded-xl border">
          {f.recommendation && (
            <div>
              <span className="font-semibold text-slate-300 block mb-1">Recommended Remediation:</span>
              <p className="text-slate-400 bg-slate-900 p-2.5 rounded-lg border border-slate-800">{f.recommendation}</p>
            </div>
          )}

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1 text-[11px]">
            {f.cvss_score && (
              <div className="text-slate-400">
                <span className="text-slate-500">CVSS Base:</span> <span className="font-mono text-slate-200">{f.cvss_score}</span>
              </div>
            )}
            {f.cve && (
              <div className="text-slate-400">
                <span className="text-slate-500">CVE ID:</span> <span className="font-mono text-indigo-300">{f.cve}</span>
              </div>
            )}
            {f.owner && (
              <div className="text-slate-400">
                <span className="text-slate-500">Remediation Owner:</span> <span className="text-slate-200">{f.owner}</span>
              </div>
            )}
            {f.evidence_id && (
              <div className="text-slate-400 truncate">
                <span className="text-slate-500">Evidence ID:</span> <span className="font-mono text-emerald-300">{f.evidence_id.substring(0, 18)}...</span>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
