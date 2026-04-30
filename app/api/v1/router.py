from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.almacenes import router as almacenes_router
from app.api.v1.endpoints.categorias import router as categorias_router
from app.api.v1.endpoints.articulos import router as articulos_router
from app.api.v1.endpoints.inventarios import router as inventarios_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(almacenes_router)
api_router.include_router(categorias_router)
api_router.include_router(articulos_router)
api_router.include_router(inventarios_router)
