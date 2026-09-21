import React from 'react'
import { Server, ShieldCheck } from 'lucide-react'
import { Asset } from '../types'

interface AssetListProps {
  assets: Asset[]
}

export const AssetList: React.FC<AssetListProps> = ({ assets }) => {
  return (
    <section className="col-span-1 lg:col-span-1">
      <div className="bg-slate-900/90 border border-slate-800/80 rounded-2xl overflow-hidden shadow-sm">
        <div className="p-5 border-b border-slate-800/80">
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <Server className="w-5 h-5 text-blue-400" /> Discovered Assets ({assets.length})
          </h2>
        </div>
        <div className="divide-y divide-slate-800/60">
          {assets.length === 0 ? (
            <div className="p-8 text-center text-slate-500 text-xs">
              No assets discovered yet. Click "Run Live Audit" to detect this machine.
            </div>
          ) : (
            assets.map(a => (
              <div key={a.id} className="p-4 hover:bg-slate-800/30 transition-colors flex items-center justify-between">
                <div>
                  <p className="font-semibold text-slate-200 text-sm">{a.hostname}</p>
                  <p className="text-xs text-slate-500 mt-0.5">{a.ip_address} • {a.os_name || 'Host'}</p>
                  <div className="flex items-center gap-2 mt-1">
                    <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700/60 font-mono">
                      {a.discovery_source}
                    </span>
                    {a.business_criticality && (
                      <span className="text-[10px] px-1.5 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-medium">
                        {a.business_criticality}
                      </span>
                    )}
                  </div>
                </div>
                <ShieldCheck className="w-5 h-5 text-slate-600 flex-shrink-0" />
              </div>
            ))
          )}
        </div>
      </div>
    </section>
  )
}
