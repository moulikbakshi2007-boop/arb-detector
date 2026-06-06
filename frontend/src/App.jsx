// ============================================================
// MAIN APP COMPONENT
// This is the root of your React application.
// Think of it as the main page that loads everything else.
// ============================================================

import { useState } from 'react'
import Dashboard from './components/Dashboard'
import './App.css'

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>🎯 Arb Detector</h1>
        <p>Real-time Sports Arbitrage Opportunity Scanner</p>
      </header>
      <main>
        <Dashboard />
      </main>
    </div>
  )
}

export default App