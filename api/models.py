from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=255)
    developer = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
 
    def __str__(self) -> str:
        return self.title