from sqlalchemy import Column, String, Float, ForeignKey, JSON, DateTime, Boolean, Integer
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class SterilizationFacility(BaseModel):
    __tablename__ = "sterilization_facilities"

    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    sterilization_method = Column(String, nullable=False)  # e.g., "ethylene_oxide", "gamma_radiation", "steam"
    capacity = Column(Float, nullable=False)  # units per day
    current_utilization = Column(Float, nullable=False)
    certification_status = Column(String, nullable=False)
    last_inspection_date = Column(DateTime, nullable=True)
    compliance_score = Column(Float, nullable=False)
    emission_controls = Column(JSON)
    backup_systems = Column(Boolean, default=True)
    risk_factors = Column(JSON)
    
    # Relationships
    batches = relationship("SterilizationBatch", back_populates="facility")
    incidents = relationship("SterilizationIncident", back_populates="facility")

class SterilizationBatch(BaseModel):
    __tablename__ = "sterilization_batches"

    facility_id = Column(Integer, ForeignKey("sterilization_facilities.id"))
    batch_number = Column(String, nullable=False)
    device_type = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    parameters = Column(JSON)  # e.g., temperature, pressure, duration
    quality_metrics = Column(JSON)
    status = Column(String, nullable=False)  # e.g., "in_progress", "completed", "failed"
    release_status = Column(String, nullable=True)
    
    # Relationships
    facility = relationship("SterilizationFacility", back_populates="batches")
    quality_checks = relationship("SterilizationQualityCheck", back_populates="batch")

class SterilizationQualityCheck(BaseModel):
    __tablename__ = "sterilization_quality_checks"

    batch_id = Column(Integer, ForeignKey("sterilization_batches.id"))
    check_type = Column(String, nullable=False)  # e.g., "biological", "chemical", "physical"
    timestamp = Column(DateTime, nullable=False)
    parameters = Column(JSON)
    results = Column(JSON)
    status = Column(String, nullable=False)  # e.g., "pass", "fail", "pending"
    reviewer = Column(String, nullable=True)
    comments = Column(String, nullable=True)
    
    # Relationships
    batch = relationship("SterilizationBatch", back_populates="quality_checks")

class SterilizationIncident(BaseModel):
    __tablename__ = "sterilization_incidents"

    facility_id = Column(Integer, ForeignKey("sterilization_facilities.id"))
    incident_type = Column(String, nullable=False)  # e.g., "equipment_failure", "parameter_deviation", "quality_failure"
    severity = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    affected_batches = Column(JSON)
    root_cause = Column(String, nullable=True)
    corrective_actions = Column(JSON)
    preventive_measures = Column(JSON)
    financial_impact = Column(Float, nullable=True)
    regulatory_impact = Column(JSON)
    
    # Relationships
    facility = relationship("SterilizationFacility", back_populates="incidents") 