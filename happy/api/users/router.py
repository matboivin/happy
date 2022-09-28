"""User-related endpoints."""

from typing import List

from elastic_transport import ConnectionTimeout, ObjectApiResponse
from elasticsearch import BadRequestError
from fastapi import APIRouter

from happy.api.users.service import UsersService
from happy.core.database import elasticsearch
from happy.core.schemas import User

users_router: APIRouter = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

users_service: UsersService = UsersService(elasticsearch)


@users_router.get("/", response_model=List[User])
async def get_users() -> ObjectApiResponse:
    """Get all users."""
    try:
        return await users_service.fetch_users()
    except ConnectionTimeout as err:
        return err


@users_router.get("/{user_id}", response_model=User)
async def get_user(user_id: int) -> ObjectApiResponse:
    """Get a user using its ID.

    Parameters
    ----------
    - **user_id**: The user identifier.

    """
    try:
        return await users_service.fetch_user(user_id)
    except ConnectionTimeout as err:
        return err


@users_router.post("/{user_id}")
async def post_user(user_id: int, user: User) -> ObjectApiResponse:
    """Create or update a user.

    Parameters
    ----------
    - **user_id**: The user identifier.
    - **user**: The user data.

    """
    try:
        return await users_service.post_user(user_id, user)
    except (BadRequestError, ConnectionTimeout) as err:
        return err


@users_router.patch("/{user_id}")
async def update_user(user_id: int, user: User) -> ObjectApiResponse:
    """Update a user.

    Parameters
    ----------
    - **user_id**: The user identifier.
    - **user**: The user data.

    """
    try:
        return await users_service.post_user(user_id, user, True)
    except (BadRequestError, ConnectionTimeout) as err:
        return err
