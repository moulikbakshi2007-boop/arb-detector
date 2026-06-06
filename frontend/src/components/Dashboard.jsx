import { useState, useEffect } from 'react'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

function Dashboard() {
  const [opportunities, setOpportunities] = useState([])
  const [history, setHistory] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(false)
  const [selectedSport, setSelectedSport] = useState('soccer_fifa_world_cup')
  const [investment, setInvestment] = useState(10000)
  const [message, setMessage] = useState('')

  const sports = [
    { key: 'soccer_fifa_world_cup', name: 'FIFA World Cup 2026' },
    { key: 'soccer_spain_la_liga', name: 'La Liga' },
    { key: 'soccer_epl', name: 'English Premier League' },
    { key: 'soccer_germany_bundesliga', name: 'Bundesliga' },
    { key: 'soccer_france_ligue_1', name: 'Ligue 1' },
    { key: 'soccer_italy_serie_a', name: 'Serie A' },
    { key: 'americanfootball_cfl', name: 'CFL' },
    { key: 'americanfootball_ncaaf', name: 'NCAAF' },
    { key: 'americanfootball_ncaaf_championship_winner', name: 'NCAAF Championship Winner' },
    { key: 'americanfootball_nfl', name: 'NFL' },
    { key: 'americanfootball_nfl_preseason', name: 'NFL Preseason' },
    { key: 'americanfootball_nfl_super_bowl_winner', name: 'NFL Super Bowl Winner' },
    { key: 'americanfootball_ufl', name: 'UFL' },
    { key: 'aussierules_afl', name: 'AFL' },
    { key: 'baseball_kbo', name: 'KBO' },
    { key: 'baseball_mlb', name: 'MLB' },
    { key: 'baseball_mlb_world_series_winner', name: 'MLB World Series Winner' },
    { key: 'baseball_ncaa', name: 'NCAA Baseball' },
    { key: 'baseball_npb', name: 'NPB' },
    { key: 'basketball_nba', name: 'NBA' },
    { key: 'basketball_nba_championship_winner', name: 'NBA Championship Winner' },
    { key: 'basketball_wnba', name: 'WNBA' },
    { key: 'boxing_boxing', name: 'Boxing' },
    { key: 'cricket_odi', name: 'One Day Internationals' },
    { key: 'cricket_t20_blast', name: 'T20 Blast' },
    { key: 'cricket_test_match', name: 'Test Matches' },
    { key: 'golf_the_open_championship_winner', name: 'The Open Winner' },
    { key: 'golf_us_open_winner', name: 'US Open Winner' },
    { key: 'handball_germany_bundesliga', name: 'Handball-Bundesliga' },
    { key: 'icehockey_ahl', name: 'AHL' },
    { key: 'icehockey_nhl', name: 'NHL' },
    { key: 'icehockey_nhl_championship_winner', name: 'NHL Championship Winner' },
    { key: 'lacrosse_pll', name: 'PLL' },
    { key: 'mma_mixed_martial_arts', name: 'MMA' },
    { key: 'politics_us_presidential_election_winner', name: 'US Presidential Elections Winner' },
    { key: 'rugbyleague_nrl', name: 'NRL' },
    { key: 'rugbyleague_nrl_state_of_origin', name: 'State of Origin' },
    { key: 'soccer_brazil_campeonato', name: 'Brazil Série A' },
    { key: 'soccer_brazil_serie_b', name: 'Brazil Série B' },
    { key: 'soccer_chile_campeonato', name: 'Primera División - Chile' },
    { key: 'soccer_china_superleague', name: 'Super League - China' },
    { key: 'soccer_conmebol_copa_libertadores', name: 'Copa Libertadores' },
    { key: 'soccer_conmebol_copa_sudamericana', name: 'Copa Sudamericana' },
    { key: 'soccer_fifa_world_cup_winner', name: 'FIFA World Cup Winner' },
    { key: 'soccer_finland_veikkausliiga', name: 'Veikkausliiga - Finland' },
    { key: 'soccer_japan_j_league', name: 'J League' },
    { key: 'soccer_league_of_ireland', name: 'League of Ireland' },
    { key: 'soccer_norway_eliteserien', name: 'Eliteserien - Norway' },
    { key: 'soccer_spain_segunda_division', name: 'La Liga 2 - Spain' },
    { key: 'soccer_sweden_allsvenskan', name: 'Allsvenskan - Sweden' },
    { key: 'soccer_sweden_superettan', name: 'Superettan - Sweden' },
    { key: 'tennis_atp_french_open', name: 'ATP French Open' },
    { key: 'tennis_wta_french_open', name: 'WTA French Open' },
  ]

  useEffect(() => {
    loadHistory()
    loadStats()
  }, [])

  async function scanSport() {
    setLoading(true)
    setMessage('Scanning...')
    setOpportunities([])
    try {
      const response = await axios.get(
        `${API_URL}/scan/${selectedSport}?investment=${investment}`
      )
      const data = response.data
      setOpportunities(data.opportunities)
      setMessage(`Scanned ${data.events_scanned} events. Found ${data.opportunities_found} opportunities.`)
      loadHistory()
      loadStats()
    } catch (error) {
      setMessage('Error connecting to backend. Is it running on port 8000?')
      console.error(error)
    }
    setLoading(false)
  }

  async function scanAll() {
    setLoading(true)
    setMessage('Scanning all sports — this takes 20-40 seconds...')
    setOpportunities([])
    try {
      const response = await axios.get(
        `${API_URL}/scan-all?investment=${investment}`
      )
      const data = response.data
      setOpportunities(data.opportunities)
      setMessage(
        `Scanned ${data.sports_scanned} sports, ${data.events_scanned} total events. Found ${data.opportunities_found} opportunities.`
      )
      loadHistory()
      loadStats()
    } catch (error) {
      setMessage('Error connecting to backend. Is it running on port 8000?')
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

      {stats && (
        <div style={{ display: 'flex', gap: '16px', marginBottom: '24px' }}>
          <StatCard title="Total Found" value={stats.total_opportunities_detected} />
          <StatCard title="Avg Margin" value={`${stats.average_profit_margin}%`} />
          <StatCard title="Best Margin" value={`${stats.best_profit_margin_ever}%`} />
        </div>
      )}

      <div style={{ background: '#1e1e2e', padding: '20px', borderRadius: '12px', marginBottom: '24px' }}>
        <h2 style={{ color: '#cdd6f4', marginTop: 0 }}>Scan for Opportunities</h2>

        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', alignItems: 'flex-end' }}>
          <div>
            <label style={{ color: '#a6adc8', display: 'block', marginBottom: '4px' }}>League</label>
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

          <button
            onClick={scanAll}
            disabled={loading}
            style={{
              padding: '8px 24px',
              borderRadius: '8px',
              background: loading ? '#6c7086' : '#f38ba8',
              color: '#1e1e2e',
              fontWeight: 'bold',
              border: 'none',
              cursor: loading ? 'not-allowed' : 'pointer'
            }}
          >
            {loading ? 'Scanning...' : '🌍 Scan All Sports'}
          </button>
        </div>

        {message && (
          <p style={{ color: '#a6e3a1', marginTop: '12px', marginBottom: 0 }}>{message}</p>
        )}
      </div>

      {opportunities.length > 0 && (
        <div style={{ marginBottom: '24px' }}>
          <h2 style={{ color: '#cdd6f4' }}>🚨 Opportunities Found</h2>
          {opportunities.map((opp, i) => (
            <OpportunityCard key={i} opp={opp} />
          ))}
        </div>
      )}

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