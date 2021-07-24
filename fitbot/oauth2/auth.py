from django.contrib.auth.backends import BaseBackend
from .models import DiscordUser


class DiscordAuthenticationBackend(BaseBackend):
    def authenticate(self, request, user, backend) -> DiscordUser:
        find_user = DiscordUser.objects.filter(id=user['id'])
        if len(find_user) == 0:
            new_user = DiscordUser.objects.create_new_discord_user(user)
            new_user.is_active = True
            return new_user
        find_user.is_active = True
        return find_user

    def get_user(self, user_id):
        try:
            return DiscordUser.objects.get(pk=user_id)
        except DiscordUser.DoesNotExist:
            return None
