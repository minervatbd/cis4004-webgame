from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Game, User, Log
from .serializers import GameSerializer, UserSerializer, LogSerializer
from rest_framework import serializers
from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404

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

@api_view(['POST'])
def login(request):
    data = request.data
    userObj = get_object_or_404(User, username=data["username"], password=data["password"])

    user = UserSerializer(userObj)
    return Response(user.data)

@api_view(['GET'])
def get_game_from_id(request, pk):
    gameObj = get_object_or_404(Game, pk=pk)

    game = GameSerializer(gameObj)
    return Response(game.data)

@api_view(['POST'])
def add_log(request):
    log = LogSerializer(data=request.data)

    # validating for already existing data
    if Log.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
    
    if log.is_valid():
        log.save()
        return Response(log.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_user_logs(request, pk):
    # checking for the parameters from the URL
    logs = get_list_or_404(Log, user_id = pk)

    if request.query_params:
        r = request.query_params.dict()
        r["user_id"] = pk
        logs = Log.objects.filter(**r)
    
    serializer = LogSerializer(logs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_log(request, user, game):
    # checking for the parameters from the URL
    log = get_object_or_404(Log, user_id = user, game_id = game)
    
    serializer = LogSerializer(log)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_logs(request, pk):
    log = get_object_or_404(Log, pk=pk)
    log.delete()
    return Response(status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
def update_logs(request, pk):
    log = Log.objects.get(pk=pk)
    data = LogSerializer(instance=log, data=request.data, partial=True)
 
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)