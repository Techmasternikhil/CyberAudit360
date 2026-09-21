import { useEffect, useState } from 'react'
import { Shield, ShieldCheck, CheckCircle2 } from 'lucide-react'
import { Finding, Asset, FilterTab, ComplianceCoverage } from './types'
import { ApiService } from './services/api'
import { Header } from './components/Header'
import { MetricCards } from './components/MetricCards'
import { ComplianceCoverageWidget } from './components/ComplianceCoverageWidget'
import { FindingCard } from './components/FindingCard'
import { AssetList } from './components/AssetList'

const FILTER_TABS: FilterTab[] = ['ALL', 'OPEN', 'RESOLVED', 'LIVE', 'DEMO']

export default function App() {
  const [findings, setFindings] = useState<Finding[]>([])
  const [assets, setAssets] = useState<Asset[]>([])
  const [securityScore, setSecurityScore] = useState<number | null>(null)
  const [coverage, setCoverage] = useState<ComplianceCoverage>({})
  const [isScanning, setIsScanning] = useState(false)
  const [activeFilter, setActiveFilter] = useState<FilterTab>('ALL')
  const [expandedFindingId, setExpandedFindingId] = useState<string | null>(null)
  const [actionMessage, setActionMessage] = useState<string | null>(null)

  const showNotification = (msg: string) => {
    setActionMessage(msg)
    setTimeout(() => setActionMessage(null), 3500)
  }

  const loadDashboardData = async () => {
    try {
      const data = await ApiService.getDashboard()
      setFindings(data.findings || [])
      setAssets(data.assets || [])
      setSecurityScore(data.score)
      setCoverage(data.coverage || {})
    } catch (err) {
      console.error("Dashboard fetch error:", err)
    }
  }

  useEffect(() => {
    loadDashboardData()
  }, [])

  const handleRunLiveScan = async () => {
    setIsScanning(true)
    try {
      const data = await ApiService.runLiveScan()
      showNotification(`Live audit completed! Found ${data.total_open_ports} open ports on ${data.asset}. SHA-256 evidence logged.`)
      await loadDashboardData()
    } catch (e) {
      console.error(e)
    } finally {
      setIsScanning(false)
    }
  }

  const handleLoadDemo = async () => {
    try {
      await ApiService.seedDemoScenario()
      showNotification("Loaded Enterprise Demo Scenario (NexusBridge)")
      await loadDashboardData()
    } catch (e) {
      console.error(e)
    }
  }

  const handleResetData = async () => {
    if (!confirm("Are you sure you want to clear all current audit findings and assets?")) return
    try {
      await ApiService.resetData()
      showNotification("All data reset to clean slate")
      await loadDashboardData()
    } catch (e) {
      console.error(e)
    }
  }

  const handleToggleFindingStatus = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation()
    try {
      await ApiService.toggleFindingStatus(id)
      await loadDashboardData()
    } catch (e) {
      console.error(e)
    }
  }

  const handleExport = (format: 'docx' | 'md') => {
    window.open(ApiService.getReportUrl(format), '_blank')
  }

  const filteredFindings = findings.filter((f) => {
    if (activeFilter === 'OPEN') return f.status === 'OPEN'
    if (activeFilter === 'RESOLVED') return f.status === 'RESOLVED'
    if (activeFilter === 'LIVE') return !f.is_demo
    if (activeFilter === 'DEMO') return f.is_demo
    return true
  })

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 p-6 md:p-10 font-sans selection:bg-indigo-500 selection:text-white">
      {/* Toast Notification */}
      {actionMessage && (
        <div className="fixed bottom-6 right-6 z-50 bg-indigo-600 text-white px-5 py-3 rounded-xl shadow-2xl flex items-center gap-3 animate-fade-in border border-indigo-400">
          <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
          <span className="text-sm font-medium">{actionMessage}</span>
        </div>
      )}

      {/* Header */}
      <Header 
        isScanning={isScanning}
        onRunScan={handleRunLiveScan}
        onLoadDemo={handleLoadDemo}
        onExport={handleExport}
        onReset={handleResetData}
      />

      <main className="space-y-8">
        {/* Metric Cards */}
        <MetricCards 
          securityScore={securityScore}
          findings={findings}
          assets={assets}
        />

        {/* Regulatory & Compliance Framework Coverage */}
        <ComplianceCoverageWidget coverage={coverage} />

        {/* Findings and Assets Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Findings List with Filters */}
          <section className="col-span-1 lg:col-span-2">
            <div className="bg-slate-900/90 border border-slate-800/80 rounded-2xl overflow-hidden shadow-sm">
              <div className="p-5 border-b border-slate-800/80 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <h2 className="text-base font-bold text-white flex items-center gap-2">
                  <Shield className="w-5 h-5 text-indigo-400" /> Security Findings ({filteredFindings.length})
                </h2>

                {/* Filter Tabs */}
                <div className="flex flex-wrap gap-1 bg-slate-950 p-1 rounded-xl border border-slate-800">
                  {FILTER_TABS.map((tab) => (
                    <button
                      key={tab}
                      id={`tab-filter-${tab.toLowerCase()}`}
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
                  filteredFindings.map((f) => (
                    <FindingCard 
                      key={f.id}
                      finding={f}
                      isExpanded={expandedFindingId === f.id}
                      onToggleExpand={() => setExpandedFindingId(expandedFindingId === f.id ? null : f.id)}
                      onToggleStatus={handleToggleFindingStatus}
                    />
                  ))
                )}
              </div>
            </div>
          </section>
          
          {/* Discovered Assets Sidebar */}
          <AssetList assets={assets} />
        </div>
      </main>
    </div>
  )
}
