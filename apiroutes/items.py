from logging import Filter
from fastapi import HTTPException, status, Response, APIRouter, Depends, Path, Query
from fastapi.responses import JSONResponse
import apiroutes.auth as auth

from typing import Annotated

from crud import create_item, get_all_items as get_all, update_item, delete_item, filter_item

from models import Item

from enumeration import FilterOption

items_router = APIRouter(tags=["Items"])


@items_router.put("/item/", tags=["Items"], dependencies=[Depends(auth.discord.requires_authorization), Depends(auth.admin)])
async def put_item(item: Item):
    res = create_item(item)
    if (res == -1):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"it failed and we don't have proper error catching yet 😨")
    else:
        return JSONResponse(content={"id": res}, status_code=status.HTTP_200_OK)


@items_router.get("/items/")
async def get_all_items():
    res = get_all()
    return JSONResponse(content={"data": res[0], "ids": res[1]}, status_code=status.HTTP_200_OK)


@items_router.patch("/item/{id}", dependencies=[Depends(auth.discord.requires_authorization), Depends(auth.admin)])
async def update_item(id: int, item: Item):
    return JSONResponse(content={"data": update_item(id, item)}, status_code=status.HTTP_200_OK)


@items_router.delete("/item/{id}", dependencies=[Depends(auth.discord.requires_authorization), Depends(auth.admin)])
async def delete_item(id: int):
    return JSONResponse(content={"data": delete_item(id)}, status_code=status.HTTP_200_OK)


@items_router.get("/filteritems/{option}")
async def filter_items_by_tags_or_requirements(option: Annotated[FilterOption, Path(description=" 0 = tags, 1 = requirements")], filters: Annotated[str, Query(description="csv")]):
    return JSONResponse(content={"data": filter_item(filters, option)}, status_code=status.HTTP_200_OK)