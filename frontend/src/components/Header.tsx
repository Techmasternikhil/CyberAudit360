import React from 'react'
import { ShieldAlert, Play, Database, Download, RotateCcw } from 'lucide-react'

interface HeaderProps {
  isScanning: boolean
  onRunScan: () => void
  onLoadDemo: () => void
  onExport: (format: 'docx' | 'md') => void
  onReset: () => void
}

export const Header: React.FC<HeaderProps> = ({
  isScanning,
  onRunScan,
  onLoadDemo,
  onExport,
  onReset
}) => {
  return (
    <header className="flex flex-col lg:flex-row items-start lg:items-center justify-between border-b border-slate-800/80 pb-6 mb-8 gap-4">
      <div className="flex items-center gap-4">
        <div className="p-3 bg-gradient-to-br from-indigo-500/20 to-purple-500/20 border border-indigo-500/30 rounded-2xl shadow-lg shadow-indigo-950/50">
          <ShieldAlert className="w-8 h-8 text-indigo-400" />
        </div>
        <div>
          <div className="flex items-center gap-2.5">
            <h1 className="text-3xl font-extrabold text-white tracking-tight">CyberAudit360</h1>
            <span className="text-[11px] font-semibold tracking-wider uppercase px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              Production Ready
            </span>
          </div>
          <p className="text-slate-400 text-sm mt-1">
            Automated Cybersecurity Audit, Risk Scoring, Cryptographic Evidence & Compliance
          </p>
        </div>
      </div>

      {/* Action Controls */}
      <div className="flex flex-wrap items-center gap-2.5">
        <button 
          id="btn-run-live-scan"
          onClick={onRunScan} 
          disabled={isScanning}
          className="flex items-center gap-2 bg-gradient-to-r from-indigo-600 to-indigo-500 hover:from-indigo-500 hover:to-indigo-400 text-white px-4 py-2.5 rounded-xl font-semibold transition-all shadow-lg shadow-indigo-600/20 disabled:opacity-50 cursor-pointer text-sm"
        >
          <Play className="w-4 h-4" />
          {isScanning ? "Scanning Localhost..." : "Run Live Audit"}
        </button>

        <button 
          id="btn-load-demo-data"
          onClick={onLoadDemo}
          className="flex items-center gap-2 bg-slate-800/90 hover:bg-slate-700 text-slate-200 px-4 py-2.5 rounded-xl font-medium transition-colors border border-slate-700/80 cursor-pointer text-sm"
        >
          <Database className="w-4 h-4 text-fuchsia-400" />
          Load Demo Data
        </button>

        <div className="flex items-center rounded-xl bg-slate-800/90 border border-slate-700/80 p-0.5">
          <button 
            id="btn-export-docx"
            onClick={() => onExport('docx')}
            className="flex items-center gap-1.5 hover:bg-slate-700 text-slate-200 px-3 py-2 rounded-lg font-medium transition-colors cursor-pointer text-xs"
            title="Download Executive Word Report (.docx)"
          >
            <Download className="w-3.5 h-3.5 text-emerald-400" />
            Word (.docx)
          </button>
          <button 
            id="btn-export-md"
            onClick={() => onExport('md')}
            className="hover:bg-slate-700 text-slate-400 hover:text-slate-200 px-2.5 py-2 rounded-lg font-medium transition-colors cursor-pointer text-xs border-l border-slate-700"
            title="Download Markdown Report (.md)"
          >
            MD
          </button>
        </div>

        <button 
          id="btn-reset-data"
          onClick={onReset}
          title="Reset to clean slate"
          className="p-2.5 bg-slate-900/90 hover:bg-rose-950/40 text-slate-400 hover:text-rose-400 rounded-xl border border-slate-800 hover:border-rose-900 transition-colors cursor-pointer"
        >
          <RotateCcw className="w-4 h-4" />
        </button>
      </div>
    </header>
  )
}
