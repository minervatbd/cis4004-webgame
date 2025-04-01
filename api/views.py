from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Game, User, Log
from .serializers import GameSerializer, UserSerializer, LogSerializer
from rest_framework import serializers
from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404
import requests
from bs4 import BeautifulSoup
import urllib.parse
import json

# Your existing API views
@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all_games': '/',
        'Search by Title': '/?title=title_name',
        'Search by Developer': '/?developer=developer_name',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': '/game/pk/delete',
        'Register': '/register',
        'Login': '/login',
        'Get Game from ID': '/game/pk/get',
        'Get User Logs': '/user/pk',
        'Get a Log': '/log/user_id/game_id',
        'Add Log': '/createlog',
        'Edit Log': '/log/pk/update',
        'Delete Log': '/log/pk/delete',
    }
    return Response(api_urls)

# Add Games
@api_view(['POST'])
def add_games(request):
    game = GameSerializer(data=request.data)
    if Game.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
 
    if game.is_valid():
        game.save()
        return Response(game.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

# View Games
@api_view(['GET'])
def view_games(request):
    if request.query_params:
        games = Game.objects.filter(**request.query_params.dict())
    else:
        games = Game.objects.all()
 
    if games:
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

# Update Games
@api_view(['POST'])
def update_games(request, pk):
    game = Game.objects.get(pk=pk)
    data = GameSerializer(instance=game, data=request.data)
 
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

# Delete Games
@api_view(['DELETE'])
def delete_games(request, pk):
    game = get_object_or_404(Game, pk=pk)
    game.delete()
    return Response(status=status.HTTP_202_ACCEPTED)

# Add Users
@api_view(['POST'])
def add_users(request):
    user = UserSerializer(data=request.data)
    if User.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
 
    if user.is_valid():
        user.save()
        return Response(user.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

# Login
@api_view(['POST'])
def login(request):
    data = request.data
    userObj = get_object_or_404(User, username=data["username"], password=data["password"])
    user = UserSerializer(userObj)
    return Response(user.data)

# Get Game by ID
@api_view(['GET'])
def get_game_from_id(request, pk):
    gameObj = get_object_or_404(Game, pk=pk)
    game = GameSerializer(gameObj)
    return Response(game.data)

# Add Log
@api_view(['POST'])
def add_log(request):
    log = LogSerializer(data=request.data)
    if Log.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
    
    if log.is_valid():
        log.save()
        return Response(log.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

# Get User Logs
@api_view(['GET'])
def get_user_logs(request, pk):
    logs = get_list_or_404(Log, user_id=pk)
    if request.query_params:
        r = request.query_params.dict()
        r["user_id"] = pk
        logs = Log.objects.filter(**r)
    
    serializer = LogSerializer(logs, many=True)
    return Response(serializer.data)

# Get Log
@api_view(['GET'])
def get_log(request, user, game):
    log = get_object_or_404(Log, user_id=user, game_id=game)
    serializer = LogSerializer(log)
    return Response(serializer.data)

# Delete Logs
@api_view(['DELETE'])
def delete_logs(request, pk):
    log = get_object_or_404(Log, pk=pk)
    log.delete()
    return Response(status=status.HTTP_202_ACCEPTED)

# Update Logs
@api_view(['POST'])
def update_logs(request, pk):
    log = Log.objects.get(pk=pk)
    data = LogSerializer(instance=log, data=request.data, partial=True)
 
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

# **Integrated Search Online Game with Scraping**
@api_view(['GET'])
def search_online_game(request):
    query = request.GET.get("query", "").strip()
    if not query:
        return Response({"error": "No search term provided"}, status=status.HTTP_400_BAD_REQUEST)

    # URL encode the query to handle special characters
    encoded_query = urllib.parse.quote(query)
    
    steam_url = f"https://store.steampowered.com/search/?term={encoded_query}"
    itch_url = f"https://itch.io/search?q={encoded_query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    results = {"steam": [], "itch": []}

    # Scrape Steam
    try:
        steam_response = requests.get(steam_url, headers=headers)
        steam_soup = BeautifulSoup(steam_response.text, "html.parser")
        steam_results = steam_soup.select(".search_result_row")  # Get all search result rows

        for steam_result in steam_results[:5]:  # Limit to 5 results
            title_element = steam_result.select_one(".title")
            link_element = steam_result.get("href")
            
            if title_element and link_element:
                results["steam"].append({
                    "title": title_element.text.strip(),
                    "url": link_element,
                })
    except Exception as e:
        results["steam"] = [{"error": f"Steam search failed: {str(e)}"}]

    # Scrape Itch.io
    try:
        itch_response = requests.get(itch_url, headers=headers)
        itch_soup = BeautifulSoup(itch_response.text, "html.parser")

        itch_results = itch_soup.select("div.game_cell a.title")  # Get all matching game titles

        for itch_result in itch_results[:5]:  # Limit to 5 results
            results["itch"].append({
                "title": itch_result.text.strip(),
                "url": itch_result["href"],
            })

        if not results["itch"]:
            results["itch"] = [{"error": "No results found on Itch.io"}]
    except Exception as e:
        results["itch"] = [{"error": f"Itch.io search failed: {str(e)}"}]

    # If both fail, return an error
    if not results["steam"] and not results["itch"]:
        return Response({"error": "No results found on Steam or Itch.io."}, status=status.HTTP_404_NOT_FOUND)

    return Response(results)
