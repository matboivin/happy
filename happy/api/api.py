"""API routes."""

from elastic_transport import ConnectionTimeout, ObjectApiResponse
from fastapi import APIRouter

from happy.api.users import users_router
from happy.core.database import elasticsearch

router: APIRouter = APIRouter()


@router.get("/")
async def get_cluster_health() -> ObjectApiResponse:
    """Return the health status of a cluster.

    Returns
    -------
    elastic_transport.ObjectApiResponse
        The health status of the ElasticSearch cluster.

    """
    try:
        return await elasticsearch.cluster.health()
    except ConnectionTimeout as err:
        return err


router.include_router(users_router)
