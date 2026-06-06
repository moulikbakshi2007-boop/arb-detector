import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ODDS_API_KEY")

SPORTS = [
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
    "soccer_fifa_world_cup",
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

BASE_URL = "https://api.the-odds-api.com/v4"


def get_active_soccer_sports():
    url = f"{BASE_URL}/sports"
    params = {"apiKey": API_KEY}

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error: {response.status_code} — {response.text}")
        return []

    active = []
    for sport in response.json():
        if "soccer" in sport["key"] and sport["active"]:
            active.append(sport)
            print(f"  ACTIVE: {sport['key']} — {sport['title']}")

    return active


def get_sports():
    url = f"{BASE_URL}/sports"
    params = {"apiKey": API_KEY}

    print("Testing API connection...")
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

    print(f"Fetching odds for: {sport_key}...")
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"  Error fetching {sport_key}: {response.status_code}")
        print(f"  {response.text}")
        return []

    events = response.json()
    print(f"  Got {len(events)} events")
    return events


def get_all_odds():
    all_events = []

    for sport_key in SPORTS:
        events = get_odds(sport_key)
        all_events.extend(events)

    print(f"\nTotal events fetched across all leagues: {len(all_events)}")
    return all_events


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


# TEST 

if __name__ == "__main__":
    print("=" * 60)
    print("ODDS FETCHER TEST")
    print("=" * 60)

    print("\nStep 1: Testing API key...")
    sports = get_sports()
    if sports is None:
        print("FAILED — check your API key in .env file")
        exit()
    else:
        print(f"SUCCESS — API connected. {len(sports)} sports available.")


    print("\nStep 2: Active soccer leagues right now:")
    get_active_soccer_sports()

    print("\nStep 3: Fetching all configured leagues...")
    all_events = get_all_odds()

    if all_events:
        print("\nStep 4: Sample event from first result:")
        event = all_events[0]
        print(f"  Match: {event['home_team']} vs {event['away_team']}")
        print(f"  Sport: {event['sport_key']}")
        print(f"  Kickoff: {event['commence_time']}")
        print(f"  Bookmakers available: {len(event['bookmakers'])}")

        print("\n  Best odds for each outcome:")
        best = extract_best_odds(event)
        for outcome, data in best.items():
            print(f"    {outcome}: {data['odds']} at {data['bookmaker']}")
    else:
        print("\nNo events found across any league.")
        print("This likely means all leagues are currently off-season.")
        print("World Cup odds should appear around June 11.")

    print("\n" + "=" * 60)
    print("Fetcher test complete.")