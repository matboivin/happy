"""User-related endpoints."""

from typing import Any, List

from elasticsearch import NotFoundError
from fastapi import APIRouter

from happy.core.database import elasticsearch
from happy.core.models.user import User

router: APIRouter = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[User])
async def get_users() -> Any:
    """Get all users."""
    return await elasticsearch.search(index="users")


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int) -> Any:
    """Get a user using its ID."""
    try:
        return await elasticsearch.get(index="users", id=user_id)
    except NotFoundError as err:
        return err


@router.post("/{user_id}")
async def post_user(user: User) -> Any:
    """Update a user data."""
    return await elasticsearch.update(
        index="users",
        id=user.id,
        body={
            "doc": {"id": user.id, "username": user.username},
            "doc_as_upsert": True,
        },
    )
