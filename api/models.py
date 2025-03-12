from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=255)
    developer = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
 
    def __str__(self) -> str:
        return self.title

class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return self.username