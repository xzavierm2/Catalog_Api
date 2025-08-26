# fetch_data.py

import requests
import json

RAWG_API_KEY = 'ea75bb1c73c743b99aa936af75239f53'

def fetch_rawg_games(page_size=10):
    """
    Fetch a list of games from RAWG API.
    """
    url = f"https://api.rawg.io/api/games?key={RAWG_API_KEY}&page_size={page_size}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data.get('results', [])

def search_steam_app(game_name):
    """
    Search for a game on Steam store and return its appid and price (if available).
    """
    search_url = f"https://store.steampowered.com/api/storesearch/?term={game_name}&l=english&cc=US"
    response = requests.get(search_url)
    response.raise_for_status()
    results = response.json().get("items", [])
    if not results:
        return None

    first = results[0]
    appid = first.get("id")
    price_overview = first.get("price")

    price = None
    if isinstance(price_overview, dict) and "final" in price_overview:
        price = price_overview["final"] / 100.0
    elif isinstance(price_overview, (int, float)):
        price = price_overview / 100.0

    return {"appid": appid, "price": price}

def fetch_steam_price(appid):
    """
    Fetch detailed price info for a Steam app by its appid.
    """
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=US&l=english"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    app_data = data.get(str(appid))
    if not app_data or not app_data.get("success"):
        return None

    price_overview = app_data["data"].get("price_overview")
    if price_overview:
        return price_overview["final"] / 100.0  # Convert from cents to dollars
    return None

def enrich_games_with_steam_prices(games):
    """
    Enrich RAWG game data with Steam prices and prepare catalog items.
    """
    enriched = []
    for game in games:
        name = game.get("name")
        print(f"Searching Steam for: {name}")
        steam_search = search_steam_app(name)
        price = None
        appid = None
        if steam_search:
            appid = steam_search.get("appid")
            # Sometimes search price is missing, fetch detailed price
            price = fetch_steam_price(appid) or steam_search.get("price")

        item = {
            "id": game.get("id"),
            "name": name,
            "description": game.get("description_raw", ""),
            "price": price or 0.0,
            "quantity": 1,
            "rating": game.get("rating", 0),
            "platform": ", ".join([p["platform"]["name"] for p in game.get("platforms", [])]),
            "release_date": game.get("released", ""),
            "category": "Video Game",
            "genre": ", ".join([g["name"] for g in game.get("genres", [])]),
            "steam_app_id": appid
        }
        enriched.append(item)
    return enriched

def save_catalog(data, filename="catalog_data.json"):
    """
    Save the enriched catalog data to a JSON file, merging with existing data.
    """
    try:
        with open(filename, "r") as f:
            existing = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing = {"catalog": []}

    existing["catalog"].extend(data)

    with open(filename, "w") as f:
        json.dump(existing, f, indent=2)

    print(f"Saved {len(data)} items to {filename}")

if __name__ == "__main__":
    rawg_games = fetch_rawg_games(10)
    enriched_games = enrich_games_with_steam_prices(rawg_games)
    save_catalog(enriched_games)
