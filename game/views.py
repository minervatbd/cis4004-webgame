from django.shortcuts import render
from django.utils.timezone import datetime

# Create your views here.
def main(request):
    # print(request.build_absolute_uri()) #optional
    return render(
        request,
        'game/main.html',
        {
            'date': datetime.now()
        }
    )