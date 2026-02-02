import datetime as dt
from typing import Union

import psutil
from fastapi import APIRouter

from models.cpu import CPUStatusResponse, ErrorResponse, LoadAverage, CPUFrequency

router = APIRouter()

@router.get("/cpu", response_model=Union[CPUStatusResponse, ErrorResponse])
async def get_cpu_status() -> Union[CPUStatusResponse, ErrorResponse]:
    """Get basic CPU information and current usage"""
    try:
        # Get CPU usage percentages
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        cpu_load_tuple = psutil.getloadavg()  # Returns (1min, 5min, 15min)
        freq_info = psutil.cpu_freq()

        return CPUStatusResponse(
            timestamp=dt.datetime.now(dt.UTC),
            cpu_count=psutil.cpu_count(),
            cpu_percent_per_core=cpu_percent,
            cpu_percent_total=sum(cpu_percent) / len(cpu_percent),
            load_average= LoadAverage(
                # should use like this because aliases starting from numbers are forbidden
                **{
                    "1_min": cpu_load_tuple[0],   # Use the alias string as key
                    "5_min": cpu_load_tuple[1],
                    "15_min": cpu_load_tuple[2]
                }
            ),
            cpu_freq=CPUFrequency(
                current=freq_info.current if freq_info else None,
                max=freq_info.max if freq_info else None
            )
        )
    except Exception as e:
        return ErrorResponse(
            error=str(e),
            timestamp=dt.datetime.now(dt.UTC)
        )