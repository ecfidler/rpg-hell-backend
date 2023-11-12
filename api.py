from fastapi import FastAPI, HTTPException, status, Response, Path, Query
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse

from typing import Annotated

from sqlalchemy import JSON

import crud
from models import Trait, Item, Spell

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


#######################################################################
################################  Temp  ###############################
#######################################################################

@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.put("/openquery", tags=["Temporary"])
async def open_query(query: str):
    """Takes in a raw SQL query."""
    return JSONResponse(content={"data": crud.open_query(query)}, status_code=status.HTTP_200_OK)

#######################################################################
######################## Object CRUD methods ##########################
#######################################################################

# api.example.com/object/?name='something'


@app.get("/object/", tags=["Objects"])
async def object_search(name: str):
    '''This method will eventually support filtering all values. Not just name.'''
    return JSONResponse(content={"data": crud.object_search(name)}, status_code=status.HTTP_200_OK)


# api.example.com/object/5
@app.get("/object/{id}", tags=["Objects"])
async def get_object_by_id(id: Annotated[int, Path(title="The ID of the object to get")]):
    return JSONResponse(content={"data": crud.get_object(id)}, status_code=status.HTTP_200_OK)

#######################################################################
########################  Item CRUD methods  ##########################
#######################################################################


@app.put("/item/", tags=["Items"])
async def put_item(item: Item):
    res = crud.create_item(item)
    if (res == -1):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"it failed and we don't have proper error catching yet 😨")
    else:
        return JSONResponse(content={"id": res}, status_code=status.HTTP_200_OK)


@app.get("/items/", tags=["Items"])
async def get_all_items():
    res = crud.get_all_items()
    return JSONResponse(content={"data": res[0], "ids": res[1]}, status_code=status.HTTP_200_OK)


# @app.patch("/item/{id}", tags=["Items"])
# async def update_item(id: int, item: Item):
#     return JSONResponse(content={"data": update_item(id, item)}, status_code=status.HTTP_200_OK)


@app.delete("item/{id}", tags=["Item"])
async def delete_item(id: int):
    return JSONResponse(content={"data": delete_item(id)}, status_code=status.HTTP_200_OK)

#######################################################################
######################## Trait CRUD methods ###########################
#######################################################################


@app.put("/trait/", tags=["Traits"])
# Annotated[Trait, Query(title="The new trait to be added")]
async def put_trait(trait: Trait):
    res = crud.create_trait(trait)
    if (res == -1):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"it failed and we don't have proper error catching yet 😨")
    else:
        return JSONResponse(content={"id": res}, status_code=status.HTTP_200_OK)


@app.get("/traits/", tags=["Traits"])
async def get_all_traits():
    res = crud.get_all_traits()
    return JSONResponse(content={"data": res[0], "ids": res[1]}, status_code=status.HTTP_200_OK)


# @app.patch("/trait/{id}", tags=["Traits"])
# async def update_trait(id: int, trait: Trait):
#     return JSONResponse(content={"data": crud.update_trait(id, trait)}, status_code=status.HTTP_200_OK)


@app.delete("/trait/{id}", tags=["Trait"])
async def delete_trait(id: int):
    return JSONResponse(content={"data": crud.delete_trait(id)}, status_code=status.HTTP_200_OK)

#######################################################################
######################### Spell CRUD methods ##########################
#######################################################################


@app.get("/spell/", tags=["Spells"])
async def spell_search(name: str):
    '''This method will eventually support filtering all values. Not just name.'''
    return JSONResponse(content={"data": crud.spell_search(name)}, status_code=status.HTTP_200_OK)


@app.get("/spells/", tags=["Spells"])
async def get_all_spells():
    res = crud.get_all_spells()
    return JSONResponse(content={"data": res[0], "ids": res[1]}, status_code=status.HTTP_200_OK)


@app.get("/spell/{id}", tags=["Spells"])
async def get_spell_by_id(id: Annotated[int, Path(title="The ID of the spell to get")]):
    return JSONResponse(content={"data": crud.get_spell(int)}, status_code=status.HTTP_200_OK)


# @app.patch("/spell/{id}", tags=["Spells"])
# async def update_spell(id: int, spell: Spell):
#     return JSONResponse(content={"data": crud.update_spell(id, spell)}, status_code=status.HTTP_200_OK)


@app.delete("/spell/{id}", tags=["Spells"])
async def delete_spell(id: int):
    return JSONResponse(content={"data": crud.delete_spell(id)}, status_code=status.HTTP_200_OK)


@app.put("/spell/", tags=["Spells"])
async def put_spell(spell: Spell):
    res = crud.create_spell(spell)
    if (res == -1):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"it failed and we don't have proper error catching yet 😨")
    else:
        return JSONResponse(content={"id": res}, status_code=status.HTTP_200_OK)

'''

robust "search" functionality for spells & objects

'''
