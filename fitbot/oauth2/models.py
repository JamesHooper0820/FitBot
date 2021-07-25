from django.contrib.auth.models import AbstractUser
from django.db import models


class DiscordUser(AbstractUser):
    discord_tag = models.CharField(max_length=100)
    avatar = models.CharField(max_length=100)
