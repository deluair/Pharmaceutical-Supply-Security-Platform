from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class SupplyChainNodeBase(BaseModel):
    node_type: str
    location: str
    capacity: Optional[float] = None
    utilization: Optional[float] = None
    risk_factors: Optional[Dict[str, Any]] = None

class SupplyChainNodeCreate(SupplyChainNodeBase):
    pass

class SupplyChainNode(SupplyChainNodeBase):
    id: int
    api_dependency_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class QualityIncidentBase(BaseModel):
    incident_type: str
    severity: str
    description: Optional[str] = None
    resolution_status: Optional[str] = None
    impact_assessment: Optional[Dict[str, Any]] = None

class QualityIncidentCreate(QualityIncidentBase):
    pass

class QualityIncident(QualityIncidentBase):
    id: int
    api_dependency_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class APIDependencyBase(BaseModel):
    name: str
    manufacturer: str
    country_of_origin: str
    global_market_share: float = Field(..., ge=0, le=100)
    us_import_dependency: float = Field(..., ge=0, le=100)
    quality_rating: float = Field(..., ge=0, le=10)
    regulatory_status: str
    alternative_sources: Optional[Dict[str, Any]] = None
    risk_assessment: Optional[Dict[str, Any]] = None

class APIDependencyCreate(APIDependencyBase):
    pass

class APIDependency(APIDependencyBase):
    id: int
    created_at: datetime
    updated_at: datetime
    supply_chain_nodes: List[SupplyChainNode] = []
    quality_incidents: List[QualityIncident] = []

    class Config:
        from_attributes = True 