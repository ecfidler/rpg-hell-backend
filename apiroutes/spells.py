from fastapi import HTTPException, status, Response, APIRouter, Depends, Path, Query
from fastapi.responses import JSONResponse
import apiroutes.auth as auth

from typing import Annotated

from crud import create_spell_crud, get_all_spells_crud as get_all, update_spell_crud, spell_delete_crud, spell_search_crud as search, get_spell_crud, filter_spell_crud

from models import Spell

spells_router = APIRouter(tags=["Spells"])


@spells_router.get("/spell/", response_model=Spell)
async def spell_search(name: str):
    '''This method will eventually support filtering all values. Not just name.'''
    # return JSONResponse(content={"data": search(name)}, status_code=status.HTTP_200_OK)
    return search(name)


@spells_router.get("/spells/", response_model=dict[int, Spell])
async def get_all_spells():
    # return JSONResponse(content={"data": res[0], "ids": res[1]}, status_code=status.HTTP_200_OK)
    return get_all()


@spells_router.get("/spell/{id}", response_model=Spell)
async def get_spell_by_id(id: Annotated[int, Path(title="The ID of the spell to get")]):
    # return JSONResponse(content={"data": get_spell(id)}, status_code=status.HTTP_200_OK)
    return get_spell_crud(id)


@spells_router.patch("/spell/{name}", dependencies=[Depends(auth.admin)])
async def update_spell(name: str, spell: Spell):
    return JSONResponse(content={"data": update_spell_crud(name, spell)}, status_code=status.HTTP_200_OK)


@spells_router.delete("/spell/{id}", dependencies=[Depends(auth.admin)])
async def delete_spell(id: int):
    return JSONResponse(content={"data": spell_delete_crud(id)}, status_code=status.HTTP_200_OK)


@spells_router.put("/spell/", tags=["Spells"], dependencies=[Depends(auth.admin)])
async def put_spell(spell: Spell):
    res = create_spell_crud(spell)
    if (res == -1):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"it failed and we don't have proper error catching yet 😨")
    else:
        return JSONResponse(content={"id": res}, status_code=status.HTTP_200_OK)


@spells_router.get("/filterspells/", response_model=dict[int, Spell])
async def filter_spells_by_tags(tags: Annotated[str, Query(description="csv")]):
    # return JSONResponse(content={"data": filter_spell(tags)}, status_code=status.HTTP_200_OK)
    return filter_spell_crud(tags)
