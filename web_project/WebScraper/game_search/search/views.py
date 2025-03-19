import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .scraper import scrape_game  # Import scraper function

def home(request):
    return render(request, "index.html")

@csrf_exempt
def search_game(request):
    if request.method == "POST":
        data = json.loads(request.body)
        game_name = data.get("game")
        platform = data.get("platform")

        if not game_name or not platform:
            return JsonResponse({"error": "Missing game name or platform"}, status=400)

        game_link = scrape_game(game_name, platform)

        if game_link:
            return JsonResponse({"message": f"Found: {game_link}"})
        else:
            return JsonResponse({"message": "No results found"})
