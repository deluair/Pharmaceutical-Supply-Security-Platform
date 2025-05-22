from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.base import Base

class ColdChainFacility(Base):
    __tablename__ = "cold_chain_facilities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    temperature_range = Column(JSON)  # {"min": float, "max": float}
    capacity = Column(Float)
    current_utilization = Column(Float)
    certification_status = Column(String)
    last_inspection_date = Column(DateTime)
    compliance_score = Column(Float)
    backup_systems = Column(Boolean)
    risk_factors = Column(JSON)

    temperature_logs = relationship("TemperatureLog", back_populates="facility")
    incidents = relationship("ColdChainIncident", back_populates="facility")

class TemperatureLog(Base):
    __tablename__ = "temperature_logs"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("cold_chain_facilities.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    temperature = Column(Float)
    humidity = Column(Float)
    status = Column(String)
    alert_threshold = Column(Float)
    notes = Column(String)

    facility = relationship("ColdChainFacility", back_populates="temperature_logs")

class ColdChainIncident(Base):
    __tablename__ = "cold_chain_incidents"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("cold_chain_facilities.id"))
    incident_type = Column(String)
    severity = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    affected_products = Column(JSON)
    root_cause = Column(String)
    corrective_actions = Column(JSON)
    preventive_measures = Column(JSON)
    financial_impact = Column(Float)
    regulatory_impact = Column(String)

    facility = relationship("ColdChainFacility", back_populates="incidents") 