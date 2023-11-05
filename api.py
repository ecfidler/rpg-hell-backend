from fastapi import FastAPI, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware

tags = [
    {
        "name": "Traits",
        "description": "Files stored in storage on the printer."
    },
    {
        "name": "Spells",
        "description": "Physical data collected by the printer."
    },
    {
        "name": "Items",
        "description": "Control for the printing processes."
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


@app.get("/")
async def root():
    return {"message": "Hello, World!"}