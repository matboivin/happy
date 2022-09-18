"""API routes."""

from fastapi import APIRouter

from happy.v1.endpoints import users

router: APIRouter = APIRouter()

router.include_router(users.router)
