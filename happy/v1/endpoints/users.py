"""User-related endpoints."""

from typing import Any

from fastapi import APIRouter

from happy.core.models.database import elasticsearch
from happy.core.models.user import User

router: APIRouter = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_root() -> Any:
    return await elasticsearch.search(index="users")


@router.get("/{user_id}")
async def read_user(user_id: int) -> Any:
    return await elasticsearch.get(index="users", id=user_id)


@router.post("/{user_id}")
async def post_user(user: User) -> Any:
    await elasticsearch.update(
        index="users",
        id=user.id,
        body={
            "doc": {"id": user.id, "username": user.username},
            "doc_as_upsert": True,
        },
    )
