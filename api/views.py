from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Game
from .serializers import GameSerializer
from rest_framework import serializers
from rest_framework import status

@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all_games': '/',
        'Search by Title': '/?title=title_name',
        'Search by Developer': '/?developer=developer_name',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': '/game/pk/delete'
    }
    
    return Response(api_urls)

@api_view(['POST'])
def add_games(request):
    game = GameSerializer(data=request.data)
 
    # validating for already existing data
    if Game.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
 
    if game.is_valid():
        game.save()
        return Response(game.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)