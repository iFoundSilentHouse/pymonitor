# Model for nested CPU frequency
import datetime as dt
from typing import List

from pydantic import BaseModel, Field


class CPUFrequency(BaseModel):
    current: float = Field(None, description="Current CPU frequency in MHz")
    max: float = Field(None, description="Maximum CPU frequency in MHz")
# Model for nested load average
class LoadAverage(BaseModel):
    load_1_min: float = Field(..., alias="1_min", description="1-minute load average")
    load_5_min: float = Field(..., alias="5_min", description="5-minute load average")
    load_15_min: float = Field(..., alias="15_min", description="15-minute load average")
# Main response model (success case)
class CPUStatusResponse(BaseModel):
    timestamp: dt.datetime
    cpu_count: int
    cpu_percent_per_core: List[float]
    cpu_percent_total: float
    load_average: LoadAverage
    cpu_freq: CPUFrequency
# Error response model
class ErrorResponse(BaseModel):
    error: str
    timestamp: dt.datetime
