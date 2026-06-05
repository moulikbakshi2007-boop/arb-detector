
from odds_fetcher import get_odds, extract_best_odds
from calculator import check_arbitrage, calculate_stakes

def scan_sport(sport_key, investment=10000):
    print(f"\nScanning {sport_key} for arbitrage opportunities...")
    print("=" * 60)
    
    events = get_odds(sport_key)
    
    if not events:
        print("No events found for this sport right now.")
        return
    
    opportunities_found = 0
    
    for event in events:
        home = event["home_team"]
        away = event["away_team"]
        
        best_odds_data = extract_best_odds(event)
        
        if len(best_odds_data) < 2:
            continue
        
        odds_list = [data["odds"] for data in best_odds_data.values()]
        outcome_names = list(best_odds_data.keys())
        bookmaker_names = [data["bookmaker"] for data in best_odds_data.values()]
        
        result = check_arbitrage(odds_list)
        
        if result:
            opportunities_found += 1
            print(f"\n🚨 ARB FOUND: {home} vs {away}")
            print(f"   Profit margin: {result['profit_margin']}%")
            print(f"   Arb sum: {result['arb_sum']}")
            
            stakes = calculate_stakes(odds_list, investment)
            print(f"\n   Stakes for ₹{investment} investment:")
            for i, stake_data in enumerate(stakes):
                print(f"   → Bet ₹{stake_data['stake']} on {outcome_names[i]}")
                print(f"     at {stake_data['odds']} ({bookmaker_names[i]})")
                print(f"     Payout if wins: ₹{stake_data['payout_if_wins']}")
        
    if opportunities_found == 0:
        print(f"\nNo arbitrage opportunities found in {len(events)} events.")
        print("This is normal — real arbs are rare. The scanner is working correctly.")
    else:
        print(f"\nTotal: {opportunities_found} opportunities found across {len(events)} events")


if __name__ == "__main__":
    scan_sport("soccer_epl")