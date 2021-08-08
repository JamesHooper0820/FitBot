from django.contrib.auth.models import AbstractUser
from django.db import models


class DiscordUser(AbstractUser):
    discord_tag = models.CharField(max_length=100)
    avatar = models.CharField(max_length=100)

class CalorieLogEntry(models.Model):
    calories = models.IntegerField()
    user = models.ForeignKey(DiscordUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
