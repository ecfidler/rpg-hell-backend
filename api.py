from fastapi import FastAPI, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse

import bl

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
    """Takes in a raw SQL query. """
    return JSONResponse(content={"data": bl.open_query(query)}, status_code=status.HTTP_200_OK)

#######################################################################
######################## Object CRUD methods ##########################
#######################################################################

# api.com/object/?name='something'
@app.get("/object/", tags=["Objects"])
async def object_search(name: str):
    '''This method will eventually support filtering all values. Not just name.'''
    return JSONResponse(content={"data": bl.object_search(name)}, status_code=status.HTTP_200_OK)


# api.com/object/5
@app.get("/object/{id}", tags=["Objects"])
async def get_object_by_id(id: int):
    return JSONResponse(content={"data": bl.get_object(id)}, status_code=status.HTTP_200_OK)

#######################################################################
########################  Item CRUD methods  ##########################
#######################################################################


@app.put("/item/", tags=["Items"])
async def put_item(name: str, effect: str, cost: int, craft: int, tags: str, req: str = ""):
    res = bl.create_item(name, effect, cost, craft, tags, req)
    if (res == -1):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"it failed and we don't have proper error catching yet 😨")
    else:
        return JSONResponse(content={"data": res}, status_code=status.HTTP_200_OK)


#######################################################################
######################## Trait CRUD methods ###########################
#######################################################################


@app.put("/trait/", tags=["Traits"])
async def put_trait(name: str, effect: str, req: str, dice: int, is_passive: bool):
    res = bl.create_trait(name, effect, req, dice, is_passive)
    if (res == -1):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"it failed and we don't have proper error catching yet 😨")
    else:
        return JSONResponse(content={"data": res}, status_code=status.HTTP_200_OK)


#######################################################################
######################### Spell CRUD methods ##########################
#######################################################################


@app.get("/spell/", tags=["Spells"])
async def spell_search(name: str):
    '''This method will eventually support filtering all values. Not just name.'''
    return JSONResponse(content={"data": bl.spell_search(name)}, status_code=status.HTTP_200_OK)


@app.get("/spell/{id}", tags=["Spells"])
async def get_spell_by_id(id: int):
    return JSONResponse(content={"data": bl.get_spell(int)}, status_code=status.HTTP_200_OK)


@app.put("/spell/", tags=["Spells"])
async def put_spell(name: str, effect: str, dice: int, level: int, tags: str):
    res = bl.create_spell(name, effect, dice, level, tags)
    if (res == -1):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"it failed and we don't have proper error catching yet 😨")
    else:
        return JSONResponse(content={"data": res}, status_code=status.HTTP_200_OK)

'''

get all formal route
update item
update trait
update spell
robust "search" functionality for spells & objects
delete object 
delete spell

'''
