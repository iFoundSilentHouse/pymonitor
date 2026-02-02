import datetime as dt

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from db.database import get_db
from db.models import HealthCheck

router = APIRouter()

# GET endpoint - returns current health status
@router.get("/health")
async def health_check() -> JSONResponse:
    """Endpoint for health checks and load balancers."""
    return JSONResponse(content={"timestamp": dt.datetime.now(dt.UTC).isoformat(), "is_active": "true"}, status_code=200)


# POST endpoint - stores health check in database
@router.post("/health")
async def store_health_check(db: Session = Depends(get_db)) -> JSONResponse:
    """Store a simple health check in the database."""
    try:
        # Create database record - just timestamp and is_active
        db_check = HealthCheck(
            # id: auto-incremented by database
            # timestamp: automatically set by func.now()
            is_active=True  # Default is already True, but explicit is clear
        )

        # Save to database
        db.add(db_check)
        db.commit()
        db.refresh(db_check)  # Refresh to get the generated id and timestamp

        return JSONResponse(
            content={
                "message": "Health check stored successfully",
                "id": db_check.id,
                "timestamp": db_check.timestamp.isoformat(),
                "is_active": db_check.is_active
            },
            status_code=201  # 201 Created
        )

    except Exception as e:
        db.rollback()  # Rollback on error
        return JSONResponse(
            content={
                "timestamp": dt.datetime.now(dt.UTC).isoformat(),
                "error": str(e),
                "status": "failed"
            },
            status_code=500
        )