from fastapi import status, Response, APIRouter, Path
from fastapi.responses import JSONResponse

from typing import Annotated

from crud import object_search as search, get_object

objects_router = APIRouter(tags=["Objects"])


@objects_router.get("/object/", tags=["Objects"])
async def object_search(name: str):
    '''This method will eventually support filtering all values. Not just name.'''
    return JSONResponse(content={"data": search(name)}, status_code=status.HTTP_200_OK)


# api.example.com/object/5
#
@objects_router.get("/object/{id}", tags=["Objects"])
async def get_object_by_id(id: Annotated[int, Path(title="The ID of the object to get")]):
    return JSONResponse(content={"data": get_object(id)}, status_code=status.HTTP_200_OK)
