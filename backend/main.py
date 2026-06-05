from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import sys
import os
sys.path.append(os.path.dirname(__file__))

from odds_fetcher import get_odds, extract_best_odds
from calculator import check_arbitrage, calculate_stakes

app = FastAPI(
    title="Arb Detector API",
    description="Real-time sports arbitrage opportunity detection",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    """
    The root endpoint. Visit http://localhost:8000 to see this.
    Good for checking if the server is running.
    """
    return {
        "message": "Arb Detector API is running",
        "version": "1.0.0",
        "docs": "Visit /docs for interactive API documentation"
    }


@app.get("/health")
def health_check():
    """Simple health check — confirms server is alive."""
    return {"status": "healthy"}


@app.get("/scan/{sport_key}")
def scan_sport(sport_key: str, investment: float = 10000):
    """
    Scan a specific sport for arbitrage opportunities.
    
    URL example: http://localhost:8000/scan/soccer_epl
    URL with investment: http://localhost:8000/scan/soccer_epl?investment=50000
    
    sport_key: the sport identifier (soccer_epl, basketball_nba, etc.)
    investment: how much money to calculate stakes for
    """
    events = get_odds(sport_key)
    
    if not events:
        return {
            "sport": sport_key,
            "events_scanned": 0,
            "opportunities": [],
            "message": "No events found for this sport"
        }
    
    opportunities = []
    
    for event in events:
        best_odds_data = extract_best_odds(event)
        
        if len(best_odds_data) < 2:
            continue
        
        odds_list = [data["odds"] for data in best_odds_data.values()]
        outcome_names = list(best_odds_data.keys())
        bookmaker_names = [data["bookmaker"] for data in best_odds_data.values()]
        
        arb_result = check_arbitrage(odds_list)
        
        if arb_result:
            stakes = calculate_stakes(odds_list, investment)
            
            stake_details = []
            for i, stake_data in enumerate(stakes):
                stake_details.append({
                    "outcome": outcome_names[i],
                    "bookmaker": bookmaker_names[i],
                    "odds": stake_data["odds"],
                    "stake": stake_data["stake"],
                    "payout_if_wins": stake_data["payout_if_wins"]
                })
            
            opportunities.append({
                "home_team": event["home_team"],
                "away_team": event["away_team"],
                "sport": sport_key,
                "profit_margin": arb_result["profit_margin"],
                "arb_sum": arb_result["arb_sum"],
                "investment": investment,
                "stakes": stake_details
            })
    
    return {
        "sport": sport_key,
        "events_scanned": len(events),
        "opportunities_found": len(opportunities),
        "opportunities": opportunities
    }


@app.get("/sports")
def list_sports():
    """Returns a list of useful sport keys to scan."""
    return {
        "sports": [
            {"key": "soccer_epl", "name": "English Premier League"},
            {"key": "soccer_uefa_champs_league", "name": "Champions League"},
            {"key": "basketball_nba", "name": "NBA Basketball"},
            {"key": "tennis_atp_french_open", "name": "ATP Tennis"},
            {"key": "americanfootball_nfl", "name": "NFL"},
        ]
    }