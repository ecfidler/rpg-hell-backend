from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi_discord import DiscordOAuthClient, Unauthorized, User

from crud import get_create_user, get_user

from models import DBUser

from settings import get_settings

settings = get_settings()

discord = DiscordOAuthClient(
    client_id=settings.discord_client_id,
    client_secret=settings.discord_client_secret,
    redirect_uri=settings.discord_redirect_uri,
    scopes=("identify", "guilds", "email")
)

auth_router = APIRouter(tags=["Users"])


async def admin(user: Annotated[User, Depends(discord.user)]):
    is_user_admin = get_user(user.id).get("is_admin")
    if (user.id == "173839815400357888") or (user.id == "275002179763306517"):  # etan-josh
        return True
    else:
        raise Unauthorized


@auth_router.on_event("startup")
async def on_startup():
    await discord.init()


@auth_router.get("/login")
async def login():
    return {"url": discord.oauth_login_url}


@auth_router.get("/auth/discord/callback")
async def callback(code: str):
    token, refresh_token = await discord.get_access_token(code)

    # user = await get_user(discord.user())

    # userData = DBUser(discord_id=user.id,
    #                   username=user.username, email=user.email)

    response = JSONResponse(
        content={"access_token": token, "refresh_token": refresh_token, })  # "user": userData
    response.set_cookie(key="access_token", value=token,
                        httponly=True, secure=True)
    response.set_cookie(key="refresh_token",
                        value=refresh_token, httponly=True, secure=True)

    return response  # change to a redirect response when working on front-end?


@auth_router.get("/refresh")
async def refresh(refresh_token: str):
    new_token, new_refresh_token = await discord.refresh_access_token(refresh_token)
    response = JSONResponse(
        content={"access_token": new_token, "refresh_token": new_refresh_token})
    response.set_cookie(key="access_token", value=new_token,
                        httponly=True, secure=True)
    response.set_cookie(key="refresh_token",
                        value=new_refresh_token, httponly=True, secure=True)
    return response  # change to a redirect response when working on front-end?


@auth_router.get(
    "/authenticated",
    dependencies=[Depends(discord.requires_authorization)],
    response_model=bool,
)
async def isAuthenticated(token: str = Depends(discord.get_token)):
    try:
        auth = await discord.isAuthenticated(token)
        return auth
    except Unauthorized:
        return False


@auth_router.get("/user", dependencies=[Depends(discord.requires_authorization)], response_model=User)
async def get_discord_user(user: User = Depends(discord.user)):
    return user


@auth_router.get("/me", dependencies=[Depends(discord.requires_authorization)])
async def get_create_database_user(user: User = Depends(discord.user)):
    res = get_create_user(
        DBUser(discord_id=user.id, username=user.username, email=user.email))
    # res.avatar_url = user.avatar_url
    return res
