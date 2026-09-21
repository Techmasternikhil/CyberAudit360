import { useEffect, useState } from 'react'
import { 
  ShieldAlert, 
  Shield, 
  ShieldCheck, 
  Activity, 
  Server, 
  AlertTriangle, 
  Play, 
  Download, 
  RotateCcw, 
  Database,
  CheckCircle2
} from 'lucide-react'

export default function App() {
  const [findings, setFindings] = useState([])
  const [assets, setAssets] = useState([])
  const [securityScore, setSecurityScore] = useState<number | null>(null)
  const [isScanning, setIsScanning] = useState(false)
  const [activeFilter, setActiveFilter] = useState<'ALL' | 'OPEN' | 'RESOLVED' | 'LIVE' | 'DEMO'>('ALL')
  const [actionMessage, setActionMessage] = useState<string | null>(null)

  const showNotification = (msg: string) => {
    setActionMessage(msg)
    setTimeout(() => setActionMessage(null), 3000)
  }

  const fetchData = () => {
    fetch('http://127.0.0.1:8000/api/findings')
      .then(res => res.json())
      .then(data => setFindings(data))
      .catch(err => console.error("API error", err))
      
    fetch('http://127.0.0.1:8000/api/assets')
      .then(res => res.json())
      .then(data => setAssets(data))
      .catch(err => console.error("API error", err))

    fetch('http://127.0.0.1:8000/api/score')
      .then(res => res.json())
      .then(data => setSecurityScore(data.score))
      .catch(err => console.error("API error", err))
  }

  useEffect(() => {
    fetchData()
  }, [])

  const runLiveScan = async () => {
    setIsScanning(true)
    try {
      const res = await fetch('http://127.0.0.1:8000/api/scan', { method: 'POST' })
      const data = await res.json()
      if (res.ok) {
        showNotification(`Live audit completed! Found ${data.total_open_ports} ports on ${data.asset}.`)
        fetchData()
      }
    } catch (e) {
      console.error(e)
    } finally {
      setIsScanning(false)
    }
  }

  const loadDemoScenario = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/demo/seed', { method: 'POST' })
      if (res.ok) {
        showNotification("Loaded Enterprise Demo Scenario (NexusBridge)")
        fetchData()
      }
    } catch (e) {
      console.error(e)
    }
  }

  const resetData = async () => {
    if (!confirm("Are you sure you want to clear all current audit findings and assets?")) return
    try {
      const res = await fetch('http://127.0.0.1:8000/api/demo/reset', { method: 'POST' })
      if (res.ok) {
        showNotification("All data reset to clean slate")
        fetchData()
      }
    } catch (e) {
      console.error(e)
    }
  }

  const toggleFindingStatus = async (id: string) => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/findings/${id}/toggle-status`, { method: 'PATCH' })
      if (res.ok) {
        fetchData()
      }
    } catch (e) {
      console.error(e)
    }
  }

  const downloadReport = () => {
    window.open('http://127.0.0.1:8000/api/report/export', '_blank')
  }

  const filteredFindings = findings.filter((f: any) => {
    if (activeFilter === 'OPEN') return f.status === 'OPEN'
    if (activeFilter === 'RESOLVED') return f.status === 'RESOLVED'
    if (activeFilter === 'LIVE') return !f.is_demo
    if (activeFilter === 'DEMO') return f.is_demo
    return true
  })

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 p-6 md:p-10 font-sans">
      {/* Toast Notification */}
      {actionMessage && (
        <div className="fixed bottom-6 right-6 z-50 bg-indigo-600 text-white px-5 py-3 rounded-xl shadow-2xl flex items-center gap-3 animate-fade-in border border-indigo-400">
          <CheckCircle2 className="w-5 h-5" />
          <span className="text-sm font-medium">{actionMessage}</span>
        </div>
      )}

      {/* Header */}
      <header className="flex flex-col lg:flex-row items-start lg:items-center justify-between border-b border-slate-800 pb-6 mb-8 gap-4">
        <div className="flex items-center gap-4">
          <div className="p-3 bg-indigo-600/10 border border-indigo-500/20 rounded-xl">
            <ShieldAlert className="w-8 h-8 text-indigo-400" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-white tracking-tight">CyberAudit360</h1>
            <p className="text-slate-400 text-sm mt-1">Automated Cybersecurity Audit, Risk Scoring & Compliance</p>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex flex-wrap items-center gap-3">
          <button 
            onClick={runLiveScan} 
            disabled={isScanning}
            className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2.5 rounded-lg font-semibold transition-all shadow-lg shadow-indigo-600/20 disabled:opacity-50 cursor-pointer text-sm"
          >
            <Play className="w-4 h-4" />
            {isScanning ? "Scanning Localhost..." : "Run Live Audit"}
          </button>

          <button 
            onClick={loadDemoScenario}
            className="flex items-center gap-2 bg-slate-800 hover:bg-slate-700 text-slate-200 px-4 py-2.5 rounded-lg font-medium transition-colors border border-slate-700 cursor-pointer text-sm"
          >
            <Database className="w-4 h-4 text-fuchsia-400" />
            Load Demo Data
          </button>

          <button 
            onClick={downloadReport}
            className="flex items-center gap-2 bg-slate-800 hover:bg-slate-700 text-slate-200 px-4 py-2.5 rounded-lg font-medium transition-colors border border-slate-700 cursor-pointer text-sm"
          >
            <Download className="w-4 h-4 text-emerald-400" />
            Export Word Report (.docx)
          </button>

          <button 
            onClick={resetData}
            title="Reset to clean slate"
            className="p-2.5 bg-slate-900 hover:bg-rose-950/40 text-slate-400 hover:text-rose-400 rounded-lg border border-slate-800 hover:border-rose-900 transition-colors cursor-pointer"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>
      </header>

      <main className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Metric Cards */}
        <section className="col-span-1 lg:col-span-3 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-slate-900/90 border border-slate-800/80 rounded-2xl p-6 flex flex-col items-center justify-center relative overflow-hidden backdrop-blur">
             <Activity className="w-8 h-8 text-emerald-400 mb-2" />
             <h3 className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Overall Security Score</h3>
             <span className="text-5xl font-extrabold text-white mt-2">
               {securityScore !== null ? securityScore : "--"}
               <span className="text-lg text-slate-500 font-normal">/100</span>
             </span>
             <p className="text-xs text-slate-500 mt-2">Calculated by Multi-Factor Risk Engine</p>
          </div>

          <div className="bg-slate-900/90 border border-slate-800/80 rounded-2xl p-6 flex flex-col items-center justify-center relative overflow-hidden backdrop-blur">
             <AlertTriangle className="w-8 h-8 text-rose-400 mb-2" />
             <h3 className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Active Findings</h3>
             <span className="text-5xl font-extrabold text-white mt-2">
               {findings.filter((f: any) => f.status === 'OPEN').length}
               <span className="text-lg text-slate-500 font-normal"> / {findings.length} total</span>
             </span>
             <p className="text-xs text-slate-500 mt-2">Identified Vulnerabilities & Exposures</p>
          </div>

          <div className="bg-slate-900/90 border border-slate-800/80 rounded-2xl p-6 flex flex-col items-center justify-center relative overflow-hidden backdrop-blur">
             <Server className="w-8 h-8 text-blue-400 mb-2" />
             <h3 className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Inventoried Assets</h3>
             <span className="text-5xl font-extrabold text-white mt-2">{assets.length}</span>
             <p className="text-xs text-slate-500 mt-2">Discovered Hosts & Workstations</p>
          </div>
        </section>

        {/* Findings List with Filters */}
        <section className="col-span-1 lg:col-span-2">
          <div className="bg-slate-900/90 border border-slate-800/80 rounded-2xl overflow-hidden">
            <div className="p-6 border-b border-slate-800/80 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <Shield className="w-5 h-5 text-indigo-400" /> Security Findings ({filteredFindings.length})
              </h2>

              {/* Filter Tabs */}
              <div className="flex flex-wrap gap-1.5 bg-slate-950 p-1 rounded-xl border border-slate-800">
                {(['ALL', 'OPEN', 'RESOLVED', 'LIVE', 'DEMO'] as const).map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setActiveFilter(tab)}
                    className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                      activeFilter === tab 
                        ? 'bg-indigo-600 text-white shadow' 
                        : 'text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    {tab}
                  </button>
                ))}
              </div>
            </div>

            <div className="divide-y divide-slate-800/60">
              {filteredFindings.length === 0 ? (
                <div className="p-12 text-center text-slate-500">
                  <ShieldCheck className="w-12 h-12 mx-auto text-slate-600 mb-3" />
                  <p className="text-base font-medium">No findings match the selected filter.</p>
                  <p className="text-xs mt-1">Click "Run Live Audit" or "Load Demo Data" above to generate findings.</p>
                </div>
              ) : (
                filteredFindings.map((f: any) => {
                  const isResolved = f.status === 'RESOLVED'
                  return (
                    <div 
                      key={f.id} 
                      className={`p-6 transition-colors ${isResolved ? 'bg-slate-950/40 opacity-70' : 'hover:bg-slate-800/40'}`}
                    >
                      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-2">
                        <div className="flex items-center gap-3">
                          <h3 className={`text-base font-semibold ${isResolved ? 'line-through text-slate-400' : 'text-white'}`}>
                            {f.title}
                          </h3>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold ${
                            f.severity === 'CRITICAL' ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30' : 
                            f.severity === 'HIGH' ? 'bg-orange-500/20 text-orange-400 border border-orange-500/30' : 
                            f.severity === 'MEDIUM' ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30' : 
                            'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                          }`}>
                            {f.severity}
                          </span>

                          <button
                            onClick={() => toggleFindingStatus(f.id)}
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

                      <p className="text-slate-400 text-sm mb-3">{f.description}</p>
                      
                      <div className="flex flex-wrap items-center gap-3 text-xs">
                        {f.is_demo ? (
                          <span className="inline-flex items-center gap-1 font-semibold text-fuchsia-400 bg-fuchsia-500/10 border border-fuchsia-500/20 px-2 py-0.5 rounded">
                            DEMO DATA
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1 font-semibold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded">
                            LIVE LOCAL SCAN
                          </span>
                        )}
                        {f.risk_score && (
                          <span className="text-slate-400 font-mono">
                            Risk Score: <span className="text-white font-semibold">{f.risk_score}</span>
                          </span>
                        )}
                        {f.category && (
                          <span className="text-slate-500">
                            Category: <span className="text-slate-300">{f.category}</span>
                          </span>
                        )}
                      </div>
                    </div>
                  )
                })
              )}
            </div>
          </div>
        </section>
        
        {/* Assets List */}
        <section className="col-span-1 lg:col-span-1">
           <div className="bg-slate-900/90 border border-slate-800/80 rounded-2xl overflow-hidden">
            <div className="p-6 border-b border-slate-800/80">
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <Server className="w-5 h-5 text-blue-400" /> Discovered Assets ({assets.length})
              </h2>
            </div>
            <div className="divide-y divide-slate-800/60">
              {assets.length === 0 ? (
                <div className="p-8 text-center text-slate-500 text-sm">
                  No assets discovered yet. Run a live scan to detect this machine.
                </div>
              ) : (
                assets.map((a: any) => (
                  <div key={a.id} className="p-4 hover:bg-slate-800/30 transition-colors flex items-center justify-between">
                    <div>
                      <p className="font-semibold text-slate-200 text-sm">{a.hostname}</p>
                      <p className="text-xs text-slate-500 mt-0.5">{a.ip_address} • {a.os_name || 'Host'}</p>
                      <span className="inline-block mt-1 text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700/60 font-mono">
                        {a.discovery_source}
                      </span>
                    </div>
                    <ShieldCheck className="w-5 h-5 text-slate-600" />
                  </div>
                ))
              )}
            </div>
          </div>
        </section>
      </main>
    </div>
  )
}
