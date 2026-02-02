import datetime as dt
from typing import Union, Optional

from pydantic import BaseModel, Field


# ========== Nested Models ==========

class VirtualMemory(BaseModel):
    """RAM (Virtual Memory) statistics"""
    total: int = Field(..., description="Total physical memory in bytes")
    total_gb: float = Field(..., description="Total physical memory in GB")
    available: int = Field(..., description="Available memory in bytes")
    available_gb: float = Field(..., description="Available memory in GB")
    used: int = Field(..., description="Used memory in bytes")
    used_gb: float = Field(..., description="Used memory in GB")
    free: int = Field(..., description="Free memory in bytes")
    free_gb: float = Field(..., description="Free memory in GB")
    percent: float = Field(..., ge=0, le=100, description="Memory usage percentage")

    # Optional attributes (may not exist on all systems)
    active: Optional[int] = Field(None, description="Active memory in bytes")
    inactive: Optional[int] = Field(None, description="Inactive memory in bytes")
    buffers: Optional[int] = Field(None, description="Buffers in bytes")
    cached: Optional[int] = Field(None, description="Cached memory in bytes")
    shared: Optional[int] = Field(None, description="Shared memory in bytes")


class SwapMemory(BaseModel):
    """Swap space statistics"""
    total: int = Field(..., description="Total swap memory in bytes")
    total_gb: float = Field(..., description="Total swap memory in GB")
    used: int = Field(..., description="Used swap in bytes")
    used_gb: float = Field(..., description="Used swap in GB")
    free: int = Field(..., description="Free swap in bytes")
    free_gb: float = Field(..., description="Free swap in GB")
    percent: float = Field(..., ge=0, le=100, description="Swap usage percentage")

    # Optional swap activity
    sin: Optional[int] = Field(None, description="Bytes swapped in from disk")
    sout: Optional[int] = Field(None, description="Bytes swapped out to disk")


class MemorySummary(BaseModel):
    """Summary analysis of memory status"""
    ram_usage_percent: float = Field(..., ge=0, le=100, description="RAM usage percentage")
    swap_usage_percent: float = Field(..., ge=0, le=100, description="Swap usage percentage")
    total_memory_gb: float = Field(..., description="Total RAM + Swap in GB")
    available_memory_gb: float = Field(..., description="Available RAM in GB")
    status: str = Field(..., description="Memory health status")


# ========== Main Response Models ==========

class MemorySuccessResponse(BaseModel):
    """Successful memory API response"""
    timestamp: dt.datetime = Field(..., description="Response timestamp in UTC")
    virtual_memory: VirtualMemory
    swap_memory: SwapMemory
    summary: MemorySummary


class MemoryErrorResponse(BaseModel):
    """Error response for memory API"""
    error: str = Field(..., description="Error message")
    timestamp: dt.datetime = Field(..., description="Error timestamp in UTC")


# ========== Union Type for FastAPI ==========

MemoryAPIResponse = Union[MemorySuccessResponse, MemoryErrorResponse]