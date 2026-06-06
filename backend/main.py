from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc
import sys, os
sys.path.append(os.path.dirname(__file__))

from odds_fetcher import get_odds, extract_best_odds
from calculator import check_arbitrage, calculate_stakes
from database import create_tables, get_db, Opportunity

app = FastAPI(title="Arb Detector API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables when server starts
create_tables()


@app.get("/")
def home():
    return {"message": "Arb Detector API is running", "docs": "/docs"}


@app.get("/scan/{sport_key}")
def scan_sport(sport_key: str, investment: float = 10000, db: Session = Depends(get_db)):
    """
    Scans a sport for arbitrage opportunities AND saves findings to database.
    """
    events = get_odds(sport_key)
    
    if not events:
        return {"sport": sport_key, "events_scanned": 0, "opportunities": []}
    
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
            payout = 0
            
            for i, stake_data in enumerate(stakes):
                stake_details.append({
                    "outcome": outcome_names[i],
                    "bookmaker": bookmaker_names[i],
                    "odds": stake_data["odds"],
                    "stake": stake_data["stake"],
                    "payout_if_wins": stake_data["payout_if_wins"]
                })
                payout = stake_data["payout_if_wins"]  # all payouts are equal
            
            # Save to database
            db_record = Opportunity(
                home_team=event["home_team"],
                away_team=event["away_team"],
                sport=sport_key,
                profit_margin=arb_result["profit_margin"],
                arb_sum=arb_result["arb_sum"],
                stakes=stake_details,
                investment=investment,
                guaranteed_return=payout
            )
            db.add(db_record)
            db.commit()
            db.refresh(db_record)
            
            opportunities.append(db_record.to_dict())
    
    return {
        "sport": sport_key,
        "events_scanned": len(events),
        "opportunities_found": len(opportunities),
        "opportunities": opportunities
    }


@app.get("/history")
def get_history(limit: int = 50, db: Session = Depends(get_db)):
    """
    Returns previously detected opportunities from the database.
    Sorted by most recent first.
    """
    records = db.query(Opportunity)\
                .order_by(desc(Opportunity.detected_at))\
                .limit(limit)\
                .all()
    return {
        "count": len(records),
        "opportunities": [r.to_dict() for r in records]
    }


@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """Returns summary statistics about all detected opportunities."""
    from sqlalchemy import func
    
    total = db.query(func.count(Opportunity.id)).scalar()
    avg_margin = db.query(func.avg(Opportunity.profit_margin)).scalar()
    max_margin = db.query(func.max(Opportunity.profit_margin)).scalar()
    
    return {
        "total_opportunities_detected": total or 0,
        "average_profit_margin": round(avg_margin or 0, 3),
        "best_profit_margin_ever": round(max_margin or 0, 3),
    }