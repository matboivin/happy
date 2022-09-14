"""API routes."""

from fastapi import APIRouter

from .endpoints import users

router: APIRouter = APIRouter()

router.include_router(users.router)
