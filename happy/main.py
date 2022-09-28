"""API initialization."""

from typing import Any, List

from elastic_transport import ConnectionTimeout
from fastapi import FastAPI

from happy.api.api import router as api_router
from happy.core.config import tags_metadata
from happy.core.database import elasticsearch
from happy.core.logger import api_logger as logger

app: FastAPI = FastAPI(
    title="happy",
    description="ᕕ( ՞ ᗜ ՞ )ᕗ",
    version="1.0.0",
    openapi_tags=tags_metadata,
)
app.include_router(api_router)


@app.on_event("startup")
async def app_startup() -> None:
    """Create indices on startup."""
    indices: List[str] = ["users"]

    try:
        for index in indices:
            if not await elasticsearch.indices.exists(index=index):
                await elasticsearch.indices.create(index=index)
    except ConnectionTimeout as err:
        logger.error(err)


@app.on_event("shutdown")
async def app_shutdown() -> None:
    """Close cluster connections on shutdown."""
    try:
        await elasticsearch.close()
    except ConnectionTimeout as err:
        logger.error(err)


@app.get("/")
async def get_cluster_health() -> Any:
    """Returns the cluster health."""
    return await elasticsearch.cluster.health()
