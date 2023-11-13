from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi_discord import DiscordOAuthClient, Unauthorized, User

from settings import get_settings

settings = get_settings()

discord = DiscordOAuthClient(
    client_id=settings.discord_client_id,
    client_secret=settings.discord_client_secret,
    redirect_uri=settings.discord_redirect_uri,
    scopes=("identify", "guilds", "email")
)

router = APIRouter(tags=["Users"])


async def admin(user: Annotated[User, Depends(discord.user)]):
    # TODO: ef - make this reference a database table
    if (user.id == "173839815400357888"):
        return True
    else:
        raise Unauthorized


@router.on_event("startup")
async def on_startup():
    await discord.init()


@router.get("/login")
async def login():
    return {"url": discord.oauth_login_url}


@router.get("/auth/discord/callback")
async def callback(code: str):
    token, refresh_token = await discord.get_access_token(code)
    return {"access_token": token, "refresh_token": refresh_token}


@router.get(
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


@router.get("/user", dependencies=[Depends(discord.requires_authorization)], response_model=User)
async def get_user(user: User = Depends(discord.user)):
    return user
