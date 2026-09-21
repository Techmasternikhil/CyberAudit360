import React from 'react'
import { Activity, AlertTriangle, ShieldAlert, Server } from 'lucide-react'
import { Finding, Asset } from '../types'

interface MetricCardsProps {
  securityScore: number | null
  findings: Finding[]
  assets: Asset[]
}

export const MetricCards: React.FC<MetricCardsProps> = ({
  securityScore,
  findings,
  assets
}) => {
  const openFindings = findings.filter(f => f.status === 'OPEN')
  const criticalHighCount = openFindings.filter(
    f => f.severity === 'CRITICAL' || f.severity === 'HIGH'
  ).length

  return (
    <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
      {/* Security Score */}
      <div className="bg-slate-900/90 border border-slate-800/80 rounded-2xl p-5 flex flex-col items-center justify-center relative overflow-hidden backdrop-blur shadow-sm">
        <Activity className="w-7 h-7 text-emerald-400 mb-1" />
        <h3 className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Security Score</h3>
        <span className="text-4xl font-black text-white mt-1">
          {securityScore !== null ? securityScore : "--"}
          <span className="text-base text-slate-500 font-normal">/100</span>
        </span>
        <p className="text-[11px] text-slate-500 mt-1">Risk Weighted Score</p>
      </div>

      {/* Active Findings */}
      <div className="bg-slate-900/90 border border-slate-800/80 rounded-2xl p-5 flex flex-col items-center justify-center relative overflow-hidden backdrop-blur shadow-sm">
        <AlertTriangle className="w-7 h-7 text-rose-400 mb-1" />
        <h3 className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Active Findings</h3>
        <span className="text-4xl font-black text-white mt-1">
          {openFindings.length}
          <span className="text-base text-slate-500 font-normal"> / {findings.length} total</span>
        </span>
        <p className="text-[11px] text-slate-500 mt-1">Identified Vulnerabilities</p>
      </div>

      {/* Critical Exposures */}
      <div className="bg-slate-900/90 border border-slate-800/80 rounded-2xl p-5 flex flex-col items-center justify-center relative overflow-hidden backdrop-blur shadow-sm">
        <ShieldAlert className="w-7 h-7 text-amber-400 mb-1" />
        <h3 className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Critical / High</h3>
        <span className="text-4xl font-black text-white mt-1">
          {criticalHighCount}
        </span>
        <p className="text-[11px] text-slate-500 mt-1">Priority Remediation Needed</p>
      </div>

      {/* Discovered Assets */}
      <div className="bg-slate-900/90 border border-slate-800/80 rounded-2xl p-5 flex flex-col items-center justify-center relative overflow-hidden backdrop-blur shadow-sm">
        <Server className="w-7 h-7 text-blue-400 mb-1" />
        <h3 className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Inventoried Assets</h3>
        <span className="text-4xl font-black text-white mt-1">{assets.length}</span>
        <p className="text-[11px] text-slate-500 mt-1">Discovered Workstations & Hosts</p>
      </div>
    </section>
  )
}
