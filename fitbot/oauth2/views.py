import os
import requests

from django.http import HttpRequest
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

DISCORD_CLIENT_ID = os.environ['DISCORD_CLIENT_ID']
DISCORD_CLIENT_SECRET = os.environ['DISCORD_CLIENT_SECRET']
DISCORD_REDIRECT_URL = os.environ['DISCORD_REDIRECT_URL']
DISCORD_REDIRECT_URI = os.environ['DISCORD_REDIRECT_URI']
DISCORD_API_ENDPOINT = os.environ['DISCORD_API_ENDPOINT']


def discord_login(request: HttpRequest) -> HttpResponseRedirect:
    return redirect(DISCORD_REDIRECT_URL)


def discord_login_redirect(request: HttpRequest) -> HttpResponseRedirect:
    code = request.GET.get("code")
    user = exchange_code(code)

    discord_user = authenticate(request, user=user)
    discord_user = list(discord_user).pop()
    login(request, discord_user)

    return redirect("/oauth2/user")


def exchange_code(code: str):
    data = {
        "client_id": DISCORD_CLIENT_ID,
        "client_secret": DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": DISCORD_REDIRECT_URI
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(
        '%s/oauth2/token' %
        DISCORD_API_ENDPOINT,
        data=data,
        headers=headers)
    credentials = response.json()
    access_token = credentials['access_token']

    response = requests.get('%s/users/@me' % DISCORD_API_ENDPOINT, headers={
        "Authorization": "Bearer %s" % access_token
    })

    return response.json()


@login_required(login_url="/oauth2/login")
def get_authenticated_user(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"msg": "Authenticated"})
