// ============================================================
// DASHBOARD COMPONENT
// This is the main dashboard page.
// It:
// 1. Lets you choose a sport and scan it
// 2. Shows live results
// 3. Shows historical opportunities
// 4. Shows summary statistics
// ============================================================

import { useState, useEffect } from 'react'
import axios from 'axios'

// The URL of your Python backend
const API_URL = 'http://localhost:8000'

function Dashboard() {
  // useState creates variables that, when changed, automatically update the UI
  const [opportunities, setOpportunities] = useState([])
  const [history, setHistory] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(false)
  const [selectedSport, setSelectedSport] = useState('soccer_epl')
  const [investment, setInvestment] = useState(10000)
  const [message, setMessage] = useState('')

  const sports = [
    { key: 'soccer_epl', name: 'English Premier League' },
    { key: 'soccer_uefa_champs_league', name: 'Champions League' },
    { key: 'basketball_nba', name: 'NBA' },
    { key: 'tennis_atp_french_open', name: 'ATP Tennis' },
    { key: 'americanfootball_nfl', name: 'NFL' },
  ]

  // Load history and stats when page first opens
  useEffect(() => {
    loadHistory()
    loadStats()
  }, [])

  async function scanSport() {
    setLoading(true)
    setMessage('Scanning...')
    setOpportunities([])

    try {
      // This calls your Python backend: GET /scan/soccer_epl?investment=10000
      const response = await axios.get(
        `${API_URL}/scan/${selectedSport}?investment=${investment}`
      )
      const data = response.data
      setOpportunities(data.opportunities)
      setMessage(
        `Scanned ${data.events_scanned} events. Found ${data.opportunities_found} opportunities.`
      )
      // Refresh history and stats after scan
      loadHistory()
      loadStats()
    } catch (error) {
      setMessage('Error connecting to backend. Is it running?')
      console.error(error)
    }

    setLoading(false)
  }

  async function loadHistory() {
    try {
      const response = await axios.get(`${API_URL}/history?limit=20`)
      setHistory(response.data.opportunities)
    } catch (error) {
      console.error('Could not load history:', error)
    }
  }

  async function loadStats() {
    try {
      const response = await axios.get(`${API_URL}/stats`)
      setStats(response.data)
    } catch (error) {
      console.error('Could not load stats:', error)
    }
  }

  return (
    <div style={{ padding: '20px', maxWidth: '1000px', margin: '0 auto' }}>

      {/* STATS PANEL */}
      {stats && (
        <div style={{ display: 'flex', gap: '16px', marginBottom: '24px' }}>
          <StatCard title="Total Found" value={stats.total_opportunities_detected} />
          <StatCard title="Avg Margin" value={`${stats.average_profit_margin}%`} />
          <StatCard title="Best Margin" value={`${stats.best_profit_margin_ever}%`} />
        </div>
      )}

      {/* SCAN CONTROLS */}
      <div style={{ background: '#1e1e2e', padding: '20px', borderRadius: '12px', marginBottom: '24px' }}>
        <h2 style={{ color: '#cdd6f4', marginTop: 0 }}>Scan for Opportunities</h2>

        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', alignItems: 'flex-end' }}>
          <div>
            <label style={{ color: '#a6adc8', display: 'block', marginBottom: '4px' }}>Sport</label>
            <select
              value={selectedSport}
              onChange={(e) => setSelectedSport(e.target.value)}
              style={{ padding: '8px 12px', borderRadius: '8px', background: '#313244', color: '#cdd6f4', border: 'none' }}
            >
              {sports.map(s => (
                <option key={s.key} value={s.key}>{s.name}</option>
              ))}
            </select>
          </div>

          <div>
            <label style={{ color: '#a6adc8', display: 'block', marginBottom: '4px' }}>Investment (₹)</label>
            <input
              type="number"
              value={investment}
              onChange={(e) => setInvestment(e.target.value)}
              style={{ padding: '8px 12px', borderRadius: '8px', background: '#313244', color: '#cdd6f4', border: 'none', width: '120px' }}
            />
          </div>

          <button
            onClick={scanSport}
            disabled={loading}
            style={{
              padding: '8px 24px',
              borderRadius: '8px',
              background: loading ? '#6c7086' : '#89b4fa',
              color: '#1e1e2e',
              fontWeight: 'bold',
              border: 'none',
              cursor: loading ? 'not-allowed' : 'pointer'
            }}
          >
            {loading ? 'Scanning...' : '🔍 Scan Now'}
          </button>
        </div>

        {message && (
          <p style={{ color: '#a6e3a1', marginTop: '12px', marginBottom: 0 }}>{message}</p>
        )}
      </div>

      {/* CURRENT SCAN RESULTS */}
      {opportunities.length > 0 && (
        <div style={{ marginBottom: '24px' }}>
          <h2 style={{ color: '#cdd6f4' }}>🚨 Opportunities Found</h2>
          {opportunities.map((opp, i) => (
            <OpportunityCard key={i} opp={opp} />
          ))}
        </div>
      )}

      {/* HISTORY */}
      <div>
        <h2 style={{ color: '#cdd6f4' }}>📋 Detection History</h2>
        {history.length === 0 ? (
          <p style={{ color: '#6c7086' }}>No history yet. Run a scan to start.</p>
        ) : (
          history.map((opp, i) => (
            <OpportunityCard key={i} opp={opp} compact />
          ))
        )}
      </div>
    </div>
  )
}


// ============================================================
// SMALLER COMPONENTS
// Each component is a reusable UI building block
// ============================================================

function StatCard({ title, value }) {
  return (
    <div style={{
      flex: 1, background: '#1e1e2e', padding: '16px', borderRadius: '12px',
      textAlign: 'center', border: '1px solid #313244'
    }}>
      <p style={{ color: '#a6adc8', margin: '0 0 4px 0', fontSize: '14px' }}>{title}</p>
      <p style={{ color: '#89b4fa', margin: 0, fontSize: '24px', fontWeight: 'bold' }}>{value}</p>
    </div>
  )
}

function OpportunityCard({ opp, compact }) {
  return (
    <div style={{
      background: '#1e1e2e', border: '1px solid #313244',
      borderRadius: '12px', padding: '16px', marginBottom: '12px'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <p style={{ color: '#cdd6f4', fontWeight: 'bold', margin: '0 0 4px 0', fontSize: '16px' }}>
            {opp.home_team} vs {opp.away_team}
          </p>
          <p style={{ color: '#6c7086', margin: 0, fontSize: '13px' }}>
            {opp.sport} {opp.detected_at && `• ${new Date(opp.detected_at).toLocaleString()}`}
          </p>
        </div>
        <div style={{
          background: '#a6e3a1', color: '#1e1e2e',
          padding: '6px 14px', borderRadius: '20px', fontWeight: 'bold'
        }}>
          +{opp.profit_margin?.toFixed(2)}%
        </div>
      </div>

      {!compact && opp.stakes && (
        <div style={{ marginTop: '12px', paddingTop: '12px', borderTop: '1px solid #313244' }}>
          <p style={{ color: '#a6adc8', margin: '0 0 8px 0', fontSize: '13px' }}>
            Invest ₹{opp.investment?.toLocaleString()} → Guaranteed ₹{opp.guaranteed_return?.toLocaleString()}
          </p>
          {opp.stakes.map((s, i) => (
            <p key={i} style={{ color: '#cdd6f4', margin: '4px 0', fontSize: '13px' }}>
              • ₹{s.stake?.toLocaleString()} on <strong>{s.outcome}</strong> @ {s.odds} ({s.bookmaker})
            </p>
          ))}
        </div>
      )}
    </div>
  )
}

export default Dashboard