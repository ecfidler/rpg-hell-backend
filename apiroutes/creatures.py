from fastapi import HTTPException, status, Response, APIRouter, Depends, Path, Query
from fastapi.responses import JSONResponse
import apiroutes.auth as auth

from typing import Annotated

from crud import create_creature
from models import Creature

creatures_router = APIRouter(tags=["Creatures"])


# @spells_router.get("/spell/", tags=["Spells"])
# async def spell_search(name: str):
#     '''This method will eventually support filtering all values. Not just name.'''
#     return JSONResponse(content={"data": search(name)}, status_code=status.HTTP_200_OK)


# @spells_router.get("/spells/", tags=["Spells"])
# async def get_all_spells():
#     res = get_all()
#     return JSONResponse(content={"data": res[0], "ids": res[1]}, status_code=status.HTTP_200_OK)


# @spells_router.get("/spell/{id}", tags=["Spells"])
# async def get_spell_by_id(id: Annotated[int, Path(title="The ID of the spell to get")]):
#     return JSONResponse(content={"data": get_spell(int)}, status_code=status.HTTP_200_OK)


# @spells_router.patch("/spell/{id}", tags=["Spells"], dependencies=[Depends(auth.discord.requires_authorization), Depends(auth.admin)])
# async def update_spell(id: int, spell: Spell):
#     return JSONResponse(content={"data": update_spell(id, spell)}, status_code=status.HTTP_200_OK)


# @spells_router.delete("/spell/{id}", tags=["Spells"], dependencies=[Depends(auth.discord.requires_authorization), Depends(auth.admin)])
# async def delete_spell(id: int):
#     return JSONResponse(content={"data": delete_spell(id)}, status_code=status.HTTP_200_OK)


@creatures_router.put("/creature/", tags=["Creatures"], dependencies=[Depends(auth.discord.requires_authorization), Depends(auth.admin)])
async def put_creature(creature: Creature):
    res = create_creature(creature)
    if (res == -1):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"it failed and we don't have proper error catching yet 😨")
    else:
        return JSONResponse(content={"id": res}, status_code=status.HTTP_200_OK)


# @spells_router.get("/filterspells/")
# async def filter_spells_by_tags(tags: Annotated[str, Query(description="csv")]):
#     return JSONResponse(content={"data": filter_spell(tags)}, status_code=status.HTTP_200_OK)
