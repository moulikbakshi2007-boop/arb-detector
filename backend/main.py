from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import sys, os
sys.path.append(os.path.dirname(__file__))

from odds_fetcher import get_odds, extract_best_odds
from calculator import check_arbitrage, calculate_stakes
from database import create_tables, get_db, Opportunity

ALL_SPORTS = [
    "soccer_fifa_world_cup",
    "soccer_spain_la_liga",
    "soccer_epl",
    "soccer_germany_bundesliga",
    "soccer_france_ligue_1",
    "soccer_italy_serie_a",
    "americanfootball_cfl",
    "americanfootball_ncaaf",
    "americanfootball_ncaaf_championship_winner",
    "americanfootball_nfl",
    "americanfootball_nfl_preseason",
    "americanfootball_nfl_super_bowl_winner",
    "americanfootball_ufl",
    "aussierules_afl",
    "baseball_kbo",
    "baseball_mlb",
    "baseball_mlb_world_series_winner",
    "baseball_ncaa",
    "baseball_npb",
    "basketball_nba",
    "basketball_nba_championship_winner",
    "basketball_wnba",
    "boxing_boxing",
    "cricket_odi",
    "cricket_t20_blast",
    "cricket_test_match",
    "golf_the_open_championship_winner",
    "golf_us_open_winner",
    "handball_germany_bundesliga",
    "icehockey_ahl",
    "icehockey_nhl",
    "icehockey_nhl_championship_winner",
    "lacrosse_pll",
    "mma_mixed_martial_arts",
    "politics_us_presidential_election_winner",
    "rugbyleague_nrl",
    "rugbyleague_nrl_state_of_origin",
    "soccer_brazil_campeonato",
    "soccer_brazil_serie_b",
    "soccer_chile_campeonato",
    "soccer_china_superleague",
    "soccer_conmebol_copa_libertadores",
    "soccer_conmebol_copa_sudamericana",
    "soccer_fifa_world_cup_winner",
    "soccer_finland_veikkausliiga",
    "soccer_japan_j_league",
    "soccer_league_of_ireland",
    "soccer_norway_eliteserien",
    "soccer_spain_segunda_division",
    "soccer_sweden_allsvenskan",
    "soccer_sweden_superettan",
    "tennis_atp_french_open",
    "tennis_wta_french_open",
]


async def auto_scan():
    from database import SessionLocal
    db = SessionLocal()
    for sport in ALL_SPORTS:
        try:
            events = get_odds(sport)
            for event in events:
                best_odds_data = extract_best_odds(event)
                if len(best_odds_data) < 2:
                    continue
                odds_list = [d["odds"] for d in best_odds_data.values()]
                arb_result = check_arbitrage(odds_list)
                if arb_result:
                    stakes = calculate_stakes(odds_list, 10000)
                    record = Opportunity(
                        home_team=event["home_team"],
                        away_team=event["away_team"],
                        sport=sport,
                        profit_margin=arb_result["profit_margin"],
                        arb_sum=arb_result["arb_sum"],
                        stakes=[{"odds": s["odds"], "stake": s["stake"]} for s in stakes],
                        investment=10000,
                        guaranteed_return=stakes[0]["payout_if_wins"] if stakes else 0
                    )
                    db.add(record)
            db.commit()
        except Exception as e:
            print(f"Auto scan error for {sport}: {e}")
    db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(auto_scan, 'interval', minutes=5, id='auto_scan')
    scheduler.start()
    print("Auto-scanner started")
    yield
    scheduler.shutdown()


app = FastAPI(title="Arb Detector API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_tables()


@app.get("/")
def home():
    return {"message": "Arb Detector API is running", "docs": "/docs"}


@app.get("/sports")
def list_sports():
    return {
        "sports": [
            {"key": "soccer_fifa_world_cup", "name": "FIFA World Cup 2026"},
            {"key": "soccer_spain_la_liga", "name": "La Liga"},
            {"key": "soccer_epl", "name": "English Premier League"},
            {"key": "soccer_germany_bundesliga", "name": "Bundesliga"},
            {"key": "soccer_france_ligue_1", "name": "Ligue 1"},
            {"key": "soccer_italy_serie_a", "name": "Serie A"},
            {"key": "americanfootball_cfl", "name": "CFL"},
            {"key": "americanfootball_ncaaf", "name": "NCAAF"},
            {"key": "americanfootball_ncaaf_championship_winner", "name": "NCAAF Championship Winner"},
            {"key": "americanfootball_nfl", "name": "NFL"},
            {"key": "americanfootball_nfl_preseason", "name": "NFL Preseason"},
            {"key": "americanfootball_nfl_super_bowl_winner", "name": "NFL Super Bowl Winner"},
            {"key": "americanfootball_ufl", "name": "UFL"},
            {"key": "aussierules_afl", "name": "AFL"},
            {"key": "baseball_kbo", "name": "KBO"},
            {"key": "baseball_mlb", "name": "MLB"},
            {"key": "baseball_mlb_world_series_winner", "name": "MLB World Series Winner"},
            {"key": "baseball_ncaa", "name": "NCAA Baseball"},
            {"key": "baseball_npb", "name": "NPB"},
            {"key": "basketball_nba", "name": "NBA"},
            {"key": "basketball_nba_championship_winner", "name": "NBA Championship Winner"},
            {"key": "basketball_wnba", "name": "WNBA"},
            {"key": "boxing_boxing", "name": "Boxing"},
            {"key": "cricket_odi", "name": "One Day Internationals"},
            {"key": "cricket_t20_blast", "name": "T20 Blast"},
            {"key": "cricket_test_match", "name": "Test Matches"},
            {"key": "golf_the_open_championship_winner", "name": "The Open Winner"},
            {"key": "golf_us_open_winner", "name": "US Open Winner"},
            {"key": "handball_germany_bundesliga", "name": "Handball-Bundesliga"},
            {"key": "icehockey_ahl", "name": "AHL"},
            {"key": "icehockey_nhl", "name": "NHL"},
            {"key": "icehockey_nhl_championship_winner", "name": "NHL Championship Winner"},
            {"key": "lacrosse_pll", "name": "PLL"},
            {"key": "mma_mixed_martial_arts", "name": "MMA"},
            {"key": "politics_us_presidential_election_winner", "name": "US Presidential Elections Winner"},
            {"key": "rugbyleague_nrl", "name": "NRL"},
            {"key": "rugbyleague_nrl_state_of_origin", "name": "State of Origin"},
            {"key": "soccer_brazil_campeonato", "name": "Brazil Série A"},
            {"key": "soccer_brazil_serie_b", "name": "Brazil Série B"},
            {"key": "soccer_chile_campeonato", "name": "Primera División - Chile"},
            {"key": "soccer_china_superleague", "name": "Super League - China"},
            {"key": "soccer_conmebol_copa_libertadores", "name": "Copa Libertadores"},
            {"key": "soccer_conmebol_copa_sudamericana", "name": "Copa Sudamericana"},
            {"key": "soccer_fifa_world_cup_winner", "name": "FIFA World Cup Winner"},
            {"key": "soccer_finland_veikkausliiga", "name": "Veikkausliiga - Finland"},
            {"key": "soccer_japan_j_league", "name": "J League"},
            {"key": "soccer_league_of_ireland", "name": "League of Ireland"},
            {"key": "soccer_norway_eliteserien", "name": "Eliteserien - Norway"},
            {"key": "soccer_spain_segunda_division", "name": "La Liga 2 - Spain"},
            {"key": "soccer_sweden_allsvenskan", "name": "Allsvenskan - Sweden"},
            {"key": "soccer_sweden_superettan", "name": "Superettan - Sweden"},
            {"key": "tennis_atp_french_open", "name": "ATP French Open"},
            {"key": "tennis_wta_french_open", "name": "WTA French Open"},
        ]
    }


@app.get("/scan/{sport_key}")
def scan_sport(sport_key: str, investment: float = 10000, db: Session = Depends(get_db)):
    events = get_odds(sport_key)

    if not events:
        return {
            "sport": sport_key,
            "events_scanned": 0,
            "opportunities_found": 0,
            "opportunities": [],
            "message": "No events found — league may be off season"
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
            payout = 0

            for i, stake_data in enumerate(stakes):
                stake_details.append({
                    "outcome": outcome_names[i],
                    "bookmaker": bookmaker_names[i],
                    "odds": stake_data["odds"],
                    "stake": stake_data["stake"],
                    "payout_if_wins": stake_data["payout_if_wins"]
                })
                payout = stake_data["payout_if_wins"]

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


@app.get("/scan-all")
def scan_all_sports(investment: float = 10000, db: Session = Depends(get_db)):
    all_opportunities = []
    total_events = 0

    for sport_key in ALL_SPORTS:
        try:
            events = get_odds(sport_key)
            total_events += len(events)

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
                        payout = stake_data["payout_if_wins"]

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
                    all_opportunities.append(db_record.to_dict())

        except Exception as e:
            print(f"Scan-all error for {sport_key}: {e}")
            continue

    return {
        "sports_scanned": len(ALL_SPORTS),
        "events_scanned": total_events,
        "opportunities_found": len(all_opportunities),
        "opportunities": all_opportunities
    }


@app.get("/history")
def get_history(limit: int = 50, db: Session = Depends(get_db)):
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
    from sqlalchemy import func
    total = db.query(func.count(Opportunity.id)).scalar()
    avg_margin = db.query(func.avg(Opportunity.profit_margin)).scalar()
    max_margin = db.query(func.max(Opportunity.profit_margin)).scalar()
    return {
        "total_opportunities_detected": total or 0,
        "average_profit_margin": round(avg_margin or 0, 3),
        "best_profit_margin_ever": round(max_margin or 0, 3),
    }