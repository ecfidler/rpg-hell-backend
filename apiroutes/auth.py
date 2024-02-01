from os import name
from typing import Annotated
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse, RedirectResponse, Response
from fastapi_discord import DiscordOAuthClient, Unauthorized, User

from models import Trait, Item, Spell, DBUser, Creature
# from models import Trait, Item, Spell, DBUser, Creature

from crud import get_create_user, get_user

from models import DBUser

from settings import get_settings
import logging

import ssl
import aiohttp
import certifi


settings = get_settings()

ssl_context = ssl.create_default_context(cafile=certifi.where())
conn = aiohttp.TCPConnector(ssl=ssl_context)

discord = DiscordOAuthClient(
    client_id=settings.discord_client_id,
    client_secret=settings.discord_client_secret,
    redirect_uri=settings.discord_redirect_uri,
    scopes=("identify", "email"),  # , "guilds"
)

auth_router = APIRouter(tags=["Users"])

redirect = "https://quiltic.github.io/rpg-hell-frontend/callback" if settings.mode == "prod" else "http://localhost:5173/callback"


async def discord_credentials(request: Request):
    # auth_token = request.cookies.get("discord_access_token")
    # auth_token = request.cookies.get("db_access")

    # logging.debug(auth_token)
    # if auth_token is None or await discord.isAuthenticated(auth_token) == False:
    #     raise Unauthorized
    # return User(**(await discord.request("/users/@me", auth_token)))
    if (settings.secret_password == settings.database_password):
        return "275002179763306517"
    return "1"


async def refresh_credentials(request: Request):
    refresh_token = request.cookies.get("discord_refresh_token")
    if refresh_token is None:
        raise Unauthorized
    return refresh_token


async def admin(user: Annotated[User, Depends(discord_credentials)]):
    # is_user_admin = get_user(user.id).get("is_admin") # this is the actual logic
    # if (user.id == "173839815400357888") or (user.id == "275002179763306517"):  # etan-josh
    if (user == "275002179763306517"):  # etan-josh
        return True
    else:
        raise Unauthorized


@auth_router.on_event("startup")
async def on_startup():
    discord.client_session = aiohttp.ClientSession(connector=conn)
    await discord.init()


@auth_router.get("/login")
async def login():
    return {"url": discord.oauth_login_url}


@auth_router.get("/logout")
async def logout():
    response = RedirectResponse(url=redirect)
    response.delete_cookie(key="discord_access_token",
                           httponly=True, secure=True)
    response.delete_cookie(key="discord_refresh_token",
                           httponly=True, secure=True)

    return response


@auth_router.get("/auth/discord/callback")
async def callback(code: str):
    token, refresh_token = await discord.get_access_token(code)

    response = RedirectResponse(url=redirect)

    response.set_cookie(key="discord_access_token",
                        value=token, httponly=True, secure=True)
    response.set_cookie(key="discord_refresh_token",
                        value=refresh_token, httponly=True, secure=True)
    print(response)
    return response


@auth_router.get("/refresh")
async def refresh(refresh_token: str = Depends(refresh_credentials)):

    try:
        new_token, new_refresh_token = await discord.refresh_access_token(refresh_token)
        response = Response(content=True, status_code=status.HTTP_202_ACCEPTED)
        response.set_cookie(key="discord_access_token",
                            value=new_token, httponly=True, secure=True)
        response.set_cookie(key="discord_refresh_token",
                            value=new_refresh_token, httponly=True, secure=True)
    except Unauthorized:
        response = Response(
            content=False, status_code=status.HTTP_401_UNAUTHORIZED)
    except:
        response = Response(
            content=False, status_code=status.HTTP_400_BAD_REQUEST)
    finally:
        return response

    # TODO: CHANGE THIS URL TO BE AN ACTUAL URL ON THE SITE


# @auth_router.get(
#     "/authenticated",
#     dependencies=[Depends(discord.requires_authorization)],
#     response_model=bool,
# )
# async def isAuthenticated(token: str = Depends(discord.get_token)):
#     try:
#         auth = await discord.isAuthenticated(token)
#         return auth
#     except Unauthorized:
#         return False

@auth_router.get("/user", dependencies=[Depends(discord_credentials)])
async def get_discord_user(user: User = Depends(discord_credentials)):
    return user


@auth_router.get("/me", dependencies=[Depends(discord_credentials)], response_model=DBUser)
async def get_or_create_database_user(user: User = Depends(discord_credentials)):
    res = get_create_user(
        DBUser(discord_id=user.id, username=user.username, email=user.email))
    res["avatar_url"] = user.avatar_url
    return res


@auth_router.get("/auth/cookie")
async def cookie(code: str):

    response = Response(content="as", status_code=status.HTTP_202_ACCEPTED)

    response.set_cookie(key="cookie_thing", value=code)

    print(response)
    return response
