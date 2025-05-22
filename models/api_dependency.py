from sqlalchemy import Column, String, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class APIDependency(BaseModel):
    __tablename__ = "api_dependencies"

    name = Column(String, index=True, nullable=False)
    manufacturer = Column(String, nullable=False)
    country_of_origin = Column(String, nullable=False)
    global_market_share = Column(Float, nullable=False)
    us_import_dependency = Column(Float, nullable=False)
    quality_rating = Column(Float, nullable=False)
    regulatory_status = Column(String, nullable=False)
    alternative_sources = Column(JSON)
    risk_assessment = Column(JSON)
    
    # Relationships
    supply_chain_nodes = relationship("SupplyChainNode", back_populates="api_dependency")
    quality_incidents = relationship("QualityIncident", back_populates="api_dependency")

class SupplyChainNode(BaseModel):
    __tablename__ = "supply_chain_nodes"

    api_dependency_id = Column(Integer, ForeignKey("api_dependencies.id"))
    node_type = Column(String, nullable=False)  # e.g., "manufacturer", "distributor", "storage"
    location = Column(String, nullable=False)
    capacity = Column(Float)
    utilization = Column(Float)
    risk_factors = Column(JSON)

    # Relationships
    api_dependency = relationship("APIDependency", back_populates="supply_chain_nodes")

class QualityIncident(BaseModel):
    __tablename__ = "quality_incidents"

    api_dependency_id = Column(Integer, ForeignKey("api_dependencies.id"))
    incident_type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    description = Column(String)
    resolution_status = Column(String)
    impact_assessment = Column(JSON)

    # Relationships
    api_dependency = relationship("APIDependency", back_populates="quality_incidents") 