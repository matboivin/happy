"""The API initialization."""

from typing import Any, Dict, List

from fastapi import FastAPI

from .core.models.database import elasticsearch
from .v1.api import router as api_router

tags_metadata: List[Dict[str, str]] = [
    {
        "name": "users",
        "description": "Operations with users.",
    },
]

app: FastAPI = FastAPI(
    title="happy",
    description="ᕕ( ՞ ᗜ ՞ )ᕗ",
    version="1.0.0",
    openapi_tags=tags_metadata,
)
app.include_router(api_router)


@app.on_event("startup")
async def app_startup() -> None:
    indices: List[str] = ["users"]

    for index in indices:
        if not (await elasticsearch.indices.exists(index=index)):
            await elasticsearch.indices.create(index=index)


@app.on_event("shutdown")
async def app_shutdown() -> None:
    await elasticsearch.close()


@app.get("/")
async def index() -> Any:
    return await elasticsearch.cluster.health()
