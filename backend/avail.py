import requests, os
from dotenv import load_dotenv
load_dotenv()

r = requests.get(
    "https://api.the-odds-api.com/v4/sports",
    params={"apiKey": os.getenv("ODDS_API_KEY")}
)
for s in r.json():
    print(s["key"], "—", s["title"])