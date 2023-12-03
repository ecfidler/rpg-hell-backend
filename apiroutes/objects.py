from fastapi import status, Response, APIRouter, Path
from fastapi.responses import JSONResponse

from typing import Annotated

from crud import object_search as search, get_object

from models import Trait, Item

objects_router = APIRouter(tags=["Objects"])


@objects_router.get("/object/", response_model=Trait | Item)
async def object_search(name: str):
    # return JSONResponse(content={"data": search(name)}, status_code=status.HTTP_200_OK)
    return search(name)


# api.example.com/object/5
#
@objects_router.get("/object/{id}", response_model=Trait | Item)
async def get_object_by_id(id: Annotated[int, Path(title="The ID of the object to get")]):
    # return JSONResponse(content={"data": get_object(id)}, status_code=status.HTTP_200_OK)
    return get_object(id)
