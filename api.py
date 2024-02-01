from fastapi import FastAPI, HTTPException, status, Response, Path, Query, Depends
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse

from fastapi_discord import Unauthorized

from settings import get_settings

import ssl


import crud
# from models import Trait, Item, Spell

from apiroutes.auth import auth_router, admin, discord_credentials
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
        "name": "Creatures",
        "description": ""
    },
    {
        "name": "Users / Authentication",
        "description": ""
    }
]


settings = get_settings()


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


# ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# ssl_context.load_cert_chain(settings.ssl_cert_path,
#                             keyfile=settings.ssl_key_path)

app = FastAPI(title="RPG Hell API",
              description="API for managing all of the data that exists in the RPG Hell tabletop game",
              openapi_tags=tags,
              generate_unique_id_function=custom_generate_unique_id)

origins = ["http://localhost:5173", "https://localhost:5173",
           "http://quiltic.github.io", "https://quiltic.github.io",
           ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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


@app.on_event("startup")
async def startup():
    import json
    import aiofiles

    async with aiofiles.open("./openapi.json", 'w+') as afp:
        my_bytes_value = json.dumps(app.openapi()).encode(
            "utf-8").decode().replace("'", '"')
        await afp.write(my_bytes_value)

    from pathlib import Path as LibPath

    file_path = LibPath("./openapi.json")
    openapi_content = json.loads(file_path.read_text())

    for path_data in openapi_content["paths"].values():
        for operation in path_data.values():
            tag = operation["tags"][0]
            operation_id = operation["operationId"]
            to_remove = f"{tag}-"
            new_operation_id = operation_id[len(to_remove):]
            operation["operationId"] = new_operation_id

    file_path.write_text(json.dumps(openapi_content))


@app.get("/", tags=["Temporary"])
async def root():
    return {"message": "Hello, World!"}


@app.put("/openquery", tags=["Temporary"], dependencies=[Depends(discord_credentials), Depends(admin)])
async def open_query(query: str):
    """Takes in a raw SQL query."""
    return JSONResponse(content={"data": crud.open_query(query)}, status_code=status.HTTP_200_OK)


@app.exception_handler(Unauthorized)
async def unauthorized_error_handler(_, __):
    return JSONResponse({"error": "Unauthorized"}, status_code=401)
