from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.api_dependency import APIDependency, SupplyChainNode, QualityIncident
from app.schemas.api_dependency import (
    APIDependency as APIDependencySchema,
    APIDependencyCreate,
    SupplyChainNode as SupplyChainNodeSchema,
    SupplyChainNodeCreate,
    QualityIncident as QualityIncidentSchema,
    QualityIncidentCreate
)

router = APIRouter()

@router.post("/", response_model=APIDependencySchema)
def create_api_dependency(
    api_dependency: APIDependencyCreate,
    db: Session = Depends(get_db)
):
    db_api_dependency = APIDependency(**api_dependency.dict())
    db.add(db_api_dependency)
    db.commit()
    db.refresh(db_api_dependency)
    return db_api_dependency

@router.get("/", response_model=List[APIDependencySchema])
def read_api_dependencies(
    skip: int = 0,
    limit: int = 100,
    country: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(APIDependency)
    if country:
        query = query.filter(APIDependency.country_of_origin == country)
    return query.offset(skip).limit(limit).all()

@router.get("/{api_dependency_id}", response_model=APIDependencySchema)
def read_api_dependency(
    api_dependency_id: int,
    db: Session = Depends(get_db)
):
    db_api_dependency = db.query(APIDependency).filter(APIDependency.id == api_dependency_id).first()
    if db_api_dependency is None:
        raise HTTPException(status_code=404, detail="API dependency not found")
    return db_api_dependency

@router.post("/{api_dependency_id}/supply-chain-nodes", response_model=SupplyChainNodeSchema)
def create_supply_chain_node(
    api_dependency_id: int,
    supply_chain_node: SupplyChainNodeCreate,
    db: Session = Depends(get_db)
):
    db_api_dependency = db.query(APIDependency).filter(APIDependency.id == api_dependency_id).first()
    if db_api_dependency is None:
        raise HTTPException(status_code=404, detail="API dependency not found")
    
    db_supply_chain_node = SupplyChainNode(
        api_dependency_id=api_dependency_id,
        **supply_chain_node.dict()
    )
    db.add(db_supply_chain_node)
    db.commit()
    db.refresh(db_supply_chain_node)
    return db_supply_chain_node

@router.post("/{api_dependency_id}/quality-incidents", response_model=QualityIncidentSchema)
def create_quality_incident(
    api_dependency_id: int,
    quality_incident: QualityIncidentCreate,
    db: Session = Depends(get_db)
):
    db_api_dependency = db.query(APIDependency).filter(APIDependency.id == api_dependency_id).first()
    if db_api_dependency is None:
        raise HTTPException(status_code=404, detail="API dependency not found")
    
    db_quality_incident = QualityIncident(
        api_dependency_id=api_dependency_id,
        **quality_incident.dict()
    )
    db.add(db_quality_incident)
    db.commit()
    db.refresh(db_quality_incident)
    return db_quality_incident

@router.get("/risk-assessment/summary")
def get_risk_assessment_summary(
    db: Session = Depends(get_db)
):
    # Calculate risk metrics
    high_risk_dependencies = db.query(APIDependency).filter(
        APIDependency.us_import_dependency > 70,
        APIDependency.quality_rating < 7
    ).count()
    
    total_dependencies = db.query(APIDependency).count()
    
    return {
        "total_dependencies": total_dependencies,
        "high_risk_dependencies": high_risk_dependencies,
        "risk_percentage": (high_risk_dependencies / total_dependencies * 100) if total_dependencies > 0 else 0
    } 