from fastapi import APIRouter
from api.endpoints import (
    health, cpu, ram
)

# Create main router for v1
api_router = APIRouter()

# Include all endpoint routers with their prefixes
api_router.include_router(health.router, tags=["Simple connection check"])
api_router.include_router(cpu.router, tags=["CPU Monitoring"])
api_router.include_router(ram.router, tags=["Memory Monitoring"])