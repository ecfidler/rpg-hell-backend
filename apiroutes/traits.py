from fastapi import HTTPException, status, Response, APIRouter, Depends
from fastapi.responses import JSONResponse
import apiroutes.auth as auth

from crud import create_trait, get_all_traits as get_all, update_trait, delete_trait

from models import Trait

traits_router = APIRouter(tags=["Traits"])


@traits_router.put("/trait/", tags=["Traits"], dependencies=[Depends(auth.discord.requires_authorization), Depends(auth.admin)])
# Annotated[Trait, Query(title="The new trait to be added")]
async def put_trait(trait: Trait):
    res = create_trait(trait)
    if (res == -1):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"it failed and we don't have proper error catching yet 😨")
    else:
        return JSONResponse(content={"id": res}, status_code=status.HTTP_200_OK)


@traits_router.get("/traits/", tags=["Traits"])
async def get_all_traits():
    res = get_all()
    return JSONResponse(content={"data": res[0], "ids": res[1]}, status_code=status.HTTP_200_OK)


@traits_router.patch("/trait/{id}", tags=["Traits"], dependencies=[Depends(auth.discord.requires_authorization), Depends(auth.admin)])
async def update_trait(id: int, trait: Trait):
    return JSONResponse(content={"data": update_trait(id, trait)}, status_code=status.HTTP_200_OK)


@traits_router.delete("/trait/{id}", tags=["Traits"], dependencies=[Depends(auth.discord.requires_authorization), Depends(auth.admin)])
async def delete_trait(id: int):
    return JSONResponse(content={"data": delete_trait(id)}, status_code=status.HTTP_200_OK)
