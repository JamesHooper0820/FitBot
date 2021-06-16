from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.discord_login, name='discord_login'),
    path('login/redirect', views.discord_login_redirect, name='discord_login_redirect'),
]
