"""
Database Models
===============
These are our database tables defined as Python classes.
SQLAlchemy will create actual tables from these.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.db.database import Base


class Tenant(Base):
    """
    Tenants table - stores all registered businesses
    
    This is like:
    CREATE TABLE tenants (
        id SERIAL PRIMARY KEY,
        business_name VARCHAR(255),
        ...
    )
    """
    __tablename__ = "tenants"
    
    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    api_key = Column(String(255), unique=True, nullable=False, index=True)
    business_type = Column(String(50), default="general")
    plan = Column(String(50), default="free")
    monthly_quota = Column(Integer, default=1000)
    requests_used = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship: One tenant has many usage logs
    usage_logs = relationship("UsageLog", back_populates="tenant")


class UsageLog(Base):
    """
    Usage logs table - tracks every API request
    
    This helps us:
    - Bill customers accurately
    - Analyze usage patterns
    - Debug issues
    """
    __tablename__ = "usage_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    prompt = Column(Text)  # What they asked
    tokens_used = Column(Integer, default=0)
    model = Column(String(100))
    cost = Column(Float, default=0.0)  # Cost in rupees
    response_time_ms = Column(Integer)  # How long it took
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship: Each log belongs to a tenant
    tenant = relationship("Tenant", back_populates="usage_logs")
