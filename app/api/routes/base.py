from fastapi import APIRouter

from app.api.routes import book, health

api_router = APIRouter()

api_router.include_router(book.router, tags=["books"], prefix="/books")
api_router.include_router(health.router, tags=["health"], prefix="/health")
