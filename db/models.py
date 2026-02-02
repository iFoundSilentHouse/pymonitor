from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean
from sqlalchemy.sql import func
from db.database import Base


class HealthCheck(Base):
    """Model for storing health check results"""
    __tablename__ = "health_checks"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True)


class CPUStat(Base):
    """Model for storing CPU statistics"""
    __tablename__ = "cpu_stats"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    cpu_percent_total = Column(Float, nullable=False)
    cpu_percent_per_core = Column(String, nullable=True)  # JSON string of list
    load_1min = Column(Float, nullable=True)
    load_5min = Column(Float, nullable=True)
    load_15min = Column(Float, nullable=True)
    cpu_freq_current = Column(Float, nullable=True)


class MemoryStat(Base):
    """Model for storing memory statistics"""
    __tablename__ = "memory_stats"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    ram_percent = Column(Float, nullable=False)
    ram_used_gb = Column(Float, nullable=False)
    ram_total_gb = Column(Float, nullable=False)
    swap_percent = Column(Float, nullable=True)
    swap_used_gb = Column(Float, nullable=True)
    swap_total_gb = Column(Float, nullable=True)


# Create all tables
def create_tables():
    from db.database import engine
    Base.metadata.create_all(bind=engine)