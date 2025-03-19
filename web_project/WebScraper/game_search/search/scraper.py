import requests
from bs4 import BeautifulSoup

def scrape_game(game_name, platform):
    search_query = game_name.replace(" ", "+")

    if platform == "steam":
        url = f"https://store.steampowered.com/search/?term={search_query}"
    elif platform == "itch":
        url = f"https://itch.io/search?q={search_query}"
    else:
        return None  # Invalid platform

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None  # Failed request

    soup = BeautifulSoup(response.text, "html5lib")

    if platform == "steam":
        results = soup.select(".search_result_row")
        if results:
            return results[0]["href"]  # Correct Steam link extraction

    elif platform == "itch":
        results = soup.select(".game_cell a.title")  # More reliable selector
        if results:
            return results[0]["href"]  # Correct Itch.io link extraction

    return None  # No results found
