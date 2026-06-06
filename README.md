# Arb Detector — Sports Arbitrage Opportunity Platform

A full-stack web application that detects arbitrage betting opportunities across multiple bookmakers in real time. Built as a software engineering learning project.

---

## What Is Arbitrage Betting?

Arbitrage betting occurs when different bookmakers offer different odds on the same event, creating a situation where betting on all outcomes simultaneously guarantees a profit regardless of the result.

**The math:**
- If the sum of (1 / odds) across all outcomes is less than 1.0, an arbitrage exists
- Profit margin = (1 - arb_sum) × 100
- Stakes are distributed proportionally so every outcome pays the same amount

**Example:**
Bookmaker A: Team X wins @ 2.10 → implied probability = 0.476
Bookmaker B: Team Y wins @ 2.15 → implied probability = 0.465
Sum = 0.941 → Profit margin = 5.9%

---

## Features

- 🔍 **Live odds fetching** from 40+ bookmakers via OddsAPI
- ⚡ **Arbitrage detection algorithm** using implied probability math
- 💰 **Automatic stake calculator** — shows exactly how much to bet on each outcome
- 🗄️ **PostgreSQL database** — saves every detected opportunity with full history
- 📊 **React dashboard** — clean UI with scan controls, results, history, and stats
- 🌍 **Scan All Sports** — scans every configured league in one click
- 🏆 **Multi-sport support** — Football, Basketball, Cricket, Tennis, MMA, and more

---

## Supported Leagues

| Sport | Leagues |
|-------|---------|
| Football | FIFA World Cup, EPL, La Liga, Bundesliga, Ligue 1, Serie A, Copa Libertadores, and more |
| Basketball | NBA, WNBA |
| Cricket | ODI, T20 Blast, Test Matches |
| Tennis | ATP French Open, WTA French Open |
| American Football | NFL, NCAAF, CFL |
| Other | MLB, NHL, MMA, Boxing, AFL, and more |

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Backend | Python 3.11 | Core language |
| API Framework | FastAPI | REST API server |
| Database | PostgreSQL | Persistent storage |
| ORM | SQLAlchemy | Database communication |
| Frontend | React + Vite | Dashboard UI |
| HTTP Client | Axios | Frontend API calls |
| External Data | OddsAPI | Live sports odds |
| Scheduling | APScheduler | Background jobs |

---

## System Architecture
OddsAPI (external)
↓
Odds Fetcher (odds_fetcher.py)
↓
Arbitrage Detector (calculator.py)
↓
PostgreSQL Database (database.py)
↓
FastAPI REST API (main.py)
↓
React Dashboard (Dashboard.jsx)

---

## Project Structure
arb-detector-project/
├── backend/
│   ├── main.py          # FastAPI server, all API endpoints
│   ├── calculator.py    # Arbitrage detection algorithm
│   ├── odds_fetcher.py  # OddsAPI integration
│   ├── scanner.py       # Combined scan pipeline
│   ├── database.py      # PostgreSQL models and connection
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── App.jsx
│       ├── App.css
│       └── components/
│           └── Dashboard.jsx
└── README.md

---

## How to Run Locally

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL
- Free API key from [the-odds-api.com](https://the-odds-api.com)

### 1. Clone the repository
```bash
git clone https://github.com/moulikbakshi2007-boop/arb-detector
cd arb-detector-project
```

### 2. Backend setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

Create a `.env` file inside the `backend` folder:
ODDS_API_KEY=your_api_key_here
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/arbdetector

Run the backend:
```bash
uvicorn main:app --reload
```

Backend runs at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

### 3. Frontend setup
```bash
cd frontend
npm install
npm run dev
```

Dashboard runs at: `http://localhost:5173`

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/sports` | List all supported sports |
| GET | `/scan/{sport_key}` | Scan one sport for arb opportunities |
| GET | `/scan-all` | Scan all configured sports at once |
| GET | `/history` | Get previously detected opportunities |
| GET | `/stats` | Summary statistics |
| GET | `/docs` | Interactive API documentation |

---

## Screenshots

> Dashboard showing scan controls, live results, and detection history

![Dashboard](image.png)

---

## What I Learned Building This

- REST API design and implementation with FastAPI
- Relational database modeling with PostgreSQL and SQLAlchemy
- External API integration and JSON data processing
- React component architecture and state management
- Mathematical algorithm implementation (implied probability, stake distribution)
- Full-stack application architecture
- Git version control and project documentation

---

## Future Improvements

- Add Redis caching for faster API responses
- WebSocket support for real-time dashboard updates without page refresh
- JWT authentication for multi-user support
- Telegram bot notifications when opportunities are detected
- Deploy to cloud (Railway or DigitalOcean)

---

## Disclaimer

This project was built purely for software engineering learning purposes. It demonstrates real-time data pipelines, algorithm implementation, and full-stack development. It is not intended for actual betting use.