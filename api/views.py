from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Game
from .serializers import GameSerializer

@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all_games': '/',
        'Search by Title': '/?title=title_name',
        'Search by Subcategory': '/?developer=developer_name',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': '/game/pk/delete'
    }
    
    return Response(api_urls)