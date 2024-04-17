from fastapi import APIRouter

from api.v1.endpoints import star_wars
from api.v1.endpoints import star_warsWorld

api_router = APIRouter()

api_router.include_router(star_wars.router, prefix="/personagem", tags=["personagem"])
api_router.include_router(star_warsWorld.router, prefix="/mundo", tags=["mundo"])