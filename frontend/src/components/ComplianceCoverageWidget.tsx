import React from 'react'
import { Award } from 'lucide-react'
import { ComplianceCoverage } from '../types'

interface ComplianceCoverageWidgetProps {
  coverage: ComplianceCoverage
}

const FRAMEWORKS = [
  { name: 'NIST CSF 2.0', key: 'NIST CSF 2.0', barColor: 'bg-indigo-500' },
  { name: 'CIS Controls v8.1', key: 'CIS Controls v8.1', barColor: 'bg-purple-500' },
  { name: 'ISO / IEC 27001', key: 'ISO 27001', barColor: 'bg-emerald-500' },
]

export const ComplianceCoverageWidget: React.FC<ComplianceCoverageWidgetProps> = ({ coverage }) => {
  return (
    <section className="bg-slate-900/90 border border-slate-800/80 rounded-2xl p-6 backdrop-blur">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
          <Award className="w-4 h-4 text-amber-400" /> Regulatory & Compliance Framework Coverage
        </h2>
        <span className="text-xs text-slate-500">Auto-mapped by FrameworkMapper</span>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {FRAMEWORKS.map(f => {
          const val = coverage[f.key] !== undefined ? coverage[f.key] : 100
          return (
            <div key={f.name} className="bg-slate-950/60 rounded-xl p-4 border border-slate-800">
              <div className="flex justify-between items-center mb-2">
                <span className="text-xs font-semibold text-slate-300">{f.name}</span>
                <span className="text-sm font-bold text-white font-mono">{val}%</span>
              </div>
              <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                <div 
                  className={`h-full ${f.barColor} transition-all duration-500`} 
                  style={{ width: `${Math.min(100, Math.max(0, val))}%` }}
                />
              </div>
              <p className="text-[10px] text-slate-500 mt-2">
                {val >= 90 ? "Strong Assurance" : val >= 75 ? "Moderate Gaps Identified" : "Significant Remediation Required"}
              </p>
            </div>
          )
        })}
      </div>
    </section>
  )
}
