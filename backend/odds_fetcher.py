
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ODDS_API_KEY")

BASE_URL = "https://api.the-odds-api.com/v4"

def get_sports():
    url = f"{BASE_URL}/sports"

    params = {
        "apiKey": API_KEY
    }
    
    print("Sending request to OddsAPI...")
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Error! Status code: {response.status_code}")
        print(f"Message: {response.text}")
        return None
    
    sports = response.json()
    return sports


def get_odds(sport_key, regions="uk,eu", markets="h2h"):

    url = f"{BASE_URL}/sports/{sport_key}/odds"
    
    params = {
        "apiKey": API_KEY,
        "regions": regions,
        "markets": markets,
        "oddsFormat": "decimal", 
    }
    
    print(f"Fetching odds for: {sport_key}")
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Error fetching odds: {response.status_code}")
        print(response.text)
        return []
    
    events = response.json()
    print(f"Got {len(events)} events")
    return events


def extract_best_odds(event):
    best_odds = {} 
    
    for bookmaker in event.get("bookmakers", []):
        bookmaker_name = bookmaker["title"]
        
        for market in bookmaker.get("markets", []):
            if market["key"] != "h2h":
                continue  
                
            for outcome in market.get("outcomes", []):
                outcome_name = outcome["name"]
                outcome_price = outcome["price"]  
                
                
                if outcome_name not in best_odds or outcome_price > best_odds[outcome_name]["odds"]:
                    best_odds[outcome_name] = {
                        "odds": outcome_price,
                        "bookmaker": bookmaker_name
                    }
    
    return best_odds

#test

if __name__ == "__main__":
    print("Step 1: Testing API connection...")
    sports = get_sports()
    
    if sports is None:
        print("Failed to connect. Check your API key in .env file")
    else:
        print(f"Success! Found {len(sports)} available sports")
        print("\nFirst 5 sports available:")
        for sport in sports[:5]:
            print(f"  - {sport['key']}: {sport['title']}")
    
    print("\n" + "=" * 50)
    
    print("\nStep 2: Fetching live tennis odds...")
    events = get_odds("tennis_atp_french_open")
    
    if not events:
        print("No events found. Tennis might be off-season.")
        print("Trying soccer EPL instead...")
        events = get_odds("soccer_epl")
    
    if events:
        print(f"\nShowing first event:")
        event = events[0]
        print(f"  Match: {event['home_team']} vs {event['away_team']}")
        print(f"  Start time: {event['commence_time']}")
        print(f"  Bookmakers available: {len(event['bookmakers'])}")
        
        print("\nBest odds for each outcome:")
        best = extract_best_odds(event)
        for outcome, data in best.items():
            print(f"  {outcome}: {data['odds']} at {data['bookmaker']}")
    else:
        print("No events available right now (might be off-season for chosen sport)")
        print("This is normal — try again when a sport is in season")