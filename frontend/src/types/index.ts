export type SeverityLevel = 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'INFORMATIONAL'
export type FindingStatus = 'OPEN' | 'RESOLVED'
export type FilterTab = 'ALL' | 'OPEN' | 'RESOLVED' | 'LIVE' | 'DEMO'

export interface Finding {
  id: string
  title: string
  description: string
  category?: string
  severity: SeverityLevel
  likelihood?: number
  impact?: number
  cvss_score?: number
  cvss_vector?: string
  cve?: string
  cwe?: string
  kev_status?: boolean
  internet_exposed?: boolean
  recommendation?: string
  owner?: string
  status: FindingStatus
  is_demo?: boolean
  evidence_id?: string
  risk_score?: number
}

export interface Asset {
  id: string
  hostname: string
  ip_address: string
  os_name?: string
  os_version?: string
  architecture?: string
  asset_type?: string
  discovery_source?: string
  business_criticality?: string
}

export interface ComplianceCoverage {
  [frameworkName: string]: number
}

export interface DashboardSummary {
  findings: Finding[]
  assets: Asset[]
  score: number | null
  score_explanation?: string
  coverage: ComplianceCoverage
}

export interface ScanResult {
  status: string
  asset: string
  new_findings_count: number
  total_open_ports: number
  evidence_id: string
  evidence_hash: string
}
