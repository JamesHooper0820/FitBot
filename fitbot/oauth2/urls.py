from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.discord_login, name='discord_login'),
    path('login/redirect/', views.discord_login_redirect, name='discord_login_redirect'),
    path('user/', views.get_authenticated_user, name='get_authenticated_user'),
]
