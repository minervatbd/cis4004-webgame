from django.shortcuts import render
from django.utils.timezone import datetime

# Create your views here.
def main(request):
    # print(request.build_absolute_uri()) #optional
    return render(
        request,
        'game/main.html'
    )

def games(request):
    return render(request, 'game/games.html')

def register(request):
    return render(request, 'game/register.html')

def collection(request):
    return render(request, 'game/collection.html')