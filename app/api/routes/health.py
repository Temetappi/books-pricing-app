from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["health"])


class HealthCheck(BaseModel):
    status: str = "ok"


@router.get("/")
async def health_check() -> HealthCheck:
    return HealthCheck(status="ok")
