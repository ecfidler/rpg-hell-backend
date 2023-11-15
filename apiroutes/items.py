from fastapi import HTTPException, status, Response, APIRouter, Depends
from fastapi.responses import JSONResponse
import apiroutes.auth as auth

from crud import create_item, get_all_items as get_all, update_item, delete_item

from models import Item

items_router = APIRouter(tags=["Items"])


@items_router.put("/item/", tags=["Items"], dependencies=[Depends(auth.discord.requires_authorization), Depends(auth.admin)])
async def put_item(item: Item):
    res = create_item(item)
    if (res == -1):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"it failed and we don't have proper error catching yet 😨")
    else:
        return JSONResponse(content={"id": res}, status_code=status.HTTP_200_OK)


@items_router.get("/items/", tags=["Items"])
async def get_all_items():
    res = get_all()
    return JSONResponse(content={"data": res[0], "ids": res[1]}, status_code=status.HTTP_200_OK)


@items_router.patch("/item/{id}", tags=["Items"], dependencies=[Depends(auth.discord.requires_authorization), Depends(auth.admin)])
async def update_item(id: int, item: Item):
    return JSONResponse(content={"data": update_item(id, item)}, status_code=status.HTTP_200_OK)


@items_router.delete("item/{id}", tags=["Items"], dependencies=[Depends(auth.discord.requires_authorization), Depends(auth.admin)])
async def delete_item(id: int):
    return JSONResponse(content={"data": delete_item(id)}, status_code=status.HTTP_200_OK)
