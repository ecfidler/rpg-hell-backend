from fastapi import FastAPI, HTTPException, status, Response, Path, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from fastapi_discord import Unauthorized

from typing import Annotated

import crud
from models import Trait, Item, Spell

from apiroutes.auth import auth_router, admin, discord
from apiroutes.traits import traits_router
from apiroutes.items import items_router
from apiroutes.spells import spells_router
from apiroutes.objects import objects_router
from apiroutes.creatures import creatures_router

tags = [
    {
        "name": "Temporary",
        "description": "A temporary endpoint that will not exist when this api has been depoloyed to production."
    },
    {
        "name": "Objects",
        "description": ""
    },
    {
        "name": "Traits",
        "description": ""
    },
    {
        "name": "Spells",
        "description": ""
    },
    {
        "name": "Items",
        "description": ""
    },
    {
        "name": "Users",
        "description": ""
    },
    {
        "name": "Creatures",
        "description": ""
    }
]

app = FastAPI(title="RPG Hell API",
              description="API for managing all of the data that exists in the RPG Hell tabletop game",
              openapi_tags=tags)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(traits_router)
app.include_router(items_router)
app.include_router(spells_router)
app.include_router(objects_router)
app.include_router(creatures_router)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.put("/openquery", tags=["Temporary"], dependencies=[Depends(discord.requires_authorization), Depends(admin)])
async def open_query(query: str):
    """Takes in a raw SQL query."""
    return JSONResponse(content={"data": crud.open_query(query)}, status_code=status.HTTP_200_OK)


@app.exception_handler(Unauthorized)
async def unauthorized_error_handler(_, __):
    return JSONResponse({"error": "Unauthorized"}, status_code=401)
