from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Game, User
from .serializers import GameSerializer, UserSerializer
from rest_framework import serializers
from rest_framework import status
from django.shortcuts import get_object_or_404

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

@api_view(['GET'])
def view_games(request):
     
    # checking for the parameters from the URL
    if request.query_params:
        games = Game.objects.filter(**request.query_params.dict())
    else:
        games = Game.objects.all()
 
    # if there is something in games else raise error
    if games:
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_games(request, pk):
    game = Game.objects.get(pk=pk)
    data = GameSerializer(instance=game, data=request.data)
 
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_games(request, pk):
    game = get_object_or_404(Game, pk=pk)
    game.delete()
    return Response(status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
def add_users(request):
    user = UserSerializer(data=request.data)
 
    # validating for already existing data
    if User.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
 
    if user.is_valid():
        user.save()
        return Response(user.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)