import os
import requests

from django.http import HttpRequest, HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import redirect

DISCORD_CLIENT_ID = os.environ['DISCORD_CLIENT_ID']
DISCORD_CLIENT_SECRET = os.environ['DISCORD_CLIENT_SECRET']
DISCORD_REDIRECT_URL = os.environ['DISCORD_REDIRECT_URL']
DISCORD_API_ENDPOINT = os.environ['DISCORD_API_ENDPOINT']

def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello, world. You're at the oauth2 index.")

def discord_login(request: HttpRequest):
    return redirect(DISCORD_REDIRECT_URL)

def discord_login_redirect(request: HttpRequest):
    code = request.GET.get("code")
    user = exchange_code(code)
    return JsonResponse({"user": user})

def exchange_code(code: str):
    data = {
        "client_id": DISCORD_CLIENT_ID,
        "client_secret": DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_url": "http://localhost:8000/oauth2/login/redirect",
        "scope": "identify"
    }   
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post('%s/oauth2/token' % DISCORD_API_ENDPOINT, data=data, headers=headers)
    credentials = response.json()
    access_token = credentials['access_token']
    response = requests.get("https://discord.com/api/v8/users/@me", headers={
        "Authorization": "Bearer %s" % access_token
    })
    user = response.json()
    return user

