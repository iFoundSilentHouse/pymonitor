import datetime as dt
import psutil
from fastapi import APIRouter

from models.ram import (MemoryAPIResponse, MemorySuccessResponse, MemoryErrorResponse, VirtualMemory, SwapMemory,
                        MemorySummary)

router = APIRouter()

@router.get("/ram", response_model=MemoryAPIResponse)
async def get_memory_status() -> MemoryAPIResponse:
    """Get comprehensive RAM status information"""
    try:
        # Get virtual memory (RAM) statistics
        ram = psutil.virtual_memory()

        # Get swap memory statistics
        swap = psutil.swap_memory()

        return MemorySuccessResponse(
            timestamp=dt.datetime.now(dt.UTC),
            virtual_memory=VirtualMemory(
                total=ram.total,
                total_gb=round(ram.total / (1024 ** 3), 2),
                available=ram.available,
                available_gb=round(ram.available / (1024 ** 3), 2),
                used=ram.used,
                used_gb=round(ram.used / (1024 ** 3), 2),
                free=ram.free,
                free_gb=round(ram.free / (1024 ** 3), 2),
                percent=ram.percent,
                active=getattr(ram, 'active', None),
                inactive=getattr(ram, 'inactive', None),
                buffers=getattr(ram, 'buffers', None),
                cached=getattr(ram, 'cached', None),
                shared=getattr(ram, 'shared', None)
            ),
            swap_memory=SwapMemory(
                total=swap.total,
                total_gb=round(swap.total / (1024 ** 3), 2),
                used=swap.used,
                used_gb=round(swap.used / (1024 ** 3), 2),
                free=swap.free,
                free_gb=round(swap.free / (1024 ** 3), 2),
                percent=swap.percent,
                sin=getattr(swap, 'sin', None),
                sout=getattr(swap, 'sout', None)
            ),
            summary=MemorySummary(
                ram_usage_percent=ram.percent,
                swap_usage_percent=swap.percent,
                total_memory_gb=round((ram.total + swap.total) / (1024 ** 3), 2),
                available_memory_gb=round(ram.available / (1024 ** 3), 2),
                status="healthy" if ram.percent < 90 else "warning"
            )
        )

    except Exception as e:
        return MemoryErrorResponse(
            error=str(e),
            timestamp=dt.datetime.now(dt.UTC)
        )