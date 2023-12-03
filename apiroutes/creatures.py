from fastapi import HTTPException, status, Response, APIRouter, Depends, Path, Query
from fastapi.responses import JSONResponse
import apiroutes.auth as auth

from typing import Annotated

from crud import create_creature, get_creature, delete_creature, update_creature
from models import Creature

creatures_router = APIRouter(tags=["Creatures"])


@creatures_router.get("/creature/", response_model=Creature)
async def creature_search(name: str):
    '''This method will eventually support filtering all values. Not just name.'''
    # return JSONResponse(content={"data": get_creature(name)}, status_code=status.HTTP_200_OK)
    return get_creature(name)


# @spells_router.get("/spells/", tags=["Spells"])
# async def get_all_spells():
#     res = get_all()
#     return JSONResponse(content={"data": res[0], "ids": res[1]}, status_code=status.HTTP_200_OK)


@creatures_router.get("/creature/{id}", response_model=Creature)
async def get_creature_by_id(id: Annotated[int, Path(title="The ID of the creature to get")]):
    # return JSONResponse(content={"data": get_creature(id)}, status_code=status.HTTP_200_OK)
    return get_creature(id)


@creatures_router.patch("/creature/{id}", dependencies=[Depends(auth.admin)])
async def update_creature(id: int, creature: Creature):
    return JSONResponse(content={"data": update_creature(id, creature)}, status_code=status.HTTP_200_OK)


@creatures_router.delete("/creature/{id}", dependencies=[Depends(auth.admin)])
async def delete_creature(id: int):
    return JSONResponse(content={"data": delete_creature(id)}, status_code=status.HTTP_200_OK)


@creatures_router.put("/creature/", dependencies=[Depends(auth.admin)])
async def put_creature(creature: Creature):
    res = create_creature(creature)
    if (res == -1):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"it failed and we don't have proper error catching yet 😨")
    else:
        return JSONResponse(content={"data": res}, status_code=status.HTTP_200_OK)


# @spells_router.get("/filterspells/")
# async def filter_spells_by_tags(tags: Annotated[str, Query(description="csv")]):
#     return JSONResponse(content={"data": filter_spell(tags)}, status_code=status.HTTP_200_OK)
