
from django.db.models import fields
from rest_framework import serializers
from .models import Game, User, Log
 
class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'title', 'developer', 'year')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ('id', 'user_id', 'game_id', 'title', 'rating', 'progress')