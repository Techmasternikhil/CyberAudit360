import { DashboardSummary, ScanResult } from '../types'

const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api'

export const ApiService = {
  /**
   * Consolidated high-performance dashboard fetch (single roundtrip)
   * with seamless fallback to individual endpoints for backwards compatibility.
   */
  async getDashboard(): Promise<DashboardSummary> {
    try {
      const res = await fetch(`${API_BASE}/dashboard`)
      if (res.ok) {
        return await res.json()
      }
    } catch {
      // Fall back to parallel individual endpoints
    }

    const [findingsRes, assetsRes, scoreRes, coverageRes] = await Promise.all([
      fetch(`${API_BASE}/findings`).then(r => r.json()).catch(() => []),
      fetch(`${API_BASE}/assets`).then(r => r.json()).catch(() => []),
      fetch(`${API_BASE}/score`).then(r => r.json()).catch(() => ({ score: null })),
      fetch(`${API_BASE}/compliance/coverage`).then(r => r.json()).catch(() => ({ coverage: {} }))
    ])

    return {
      findings: findingsRes,
      assets: assetsRes,
      score: scoreRes.score ?? null,
      coverage: coverageRes.coverage || {}
    }
  },

  async runLiveScan(): Promise<ScanResult> {
    const res = await fetch(`${API_BASE}/scan`, { method: 'POST' })
    if (!res.ok) {
      throw new Error(`Live scan failed with status: ${res.status}`)
    }
    return await res.json()
  },

  async seedDemoScenario(): Promise<{ status: string; message: string }> {
    const res = await fetch(`${API_BASE}/demo/seed`, { method: 'POST' })
    if (!res.ok) {
      throw new Error(`Demo seed failed with status: ${res.status}`)
    }
    return await res.json()
  },

  async resetData(): Promise<{ status: string; message: string }> {
    const res = await fetch(`${API_BASE}/demo/reset`, { method: 'POST' })
    if (!res.ok) {
      throw new Error(`Data reset failed with status: ${res.status}`)
    }
    return await res.json()
  },

  async toggleFindingStatus(id: string): Promise<{ status: string; id: string; new_status: string }> {
    const res = await fetch(`${API_BASE}/findings/${id}/toggle-status`, { method: 'PATCH' })
    if (!res.ok) {
      throw new Error(`Toggle status failed with status: ${res.status}`)
    }
    return await res.json()
  },

  getReportUrl(format: 'docx' | 'md' = 'docx'): string {
    return `${API_BASE}/report/export?format=${format}`
  }
}
