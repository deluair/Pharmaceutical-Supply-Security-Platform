from sqlalchemy import Column, String, Float, ForeignKey, JSON, DateTime, Boolean, Integer
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class EconomicAnalysis(BaseModel):
    __tablename__ = "economic_analyses"

    name = Column(String, nullable=False)
    analysis_type = Column(String, nullable=False)  # e.g., "cost_benefit", "roi", "risk_assessment"
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    currency = Column(String, nullable=False, default="USD")
    discount_rate = Column(Float, nullable=False)
    assumptions = Column(JSON)
    results = Column(JSON)
    sensitivity_analysis = Column(JSON)
    
    # Relationships
    cost_items = relationship("CostItem", back_populates="analysis")
    benefit_items = relationship("BenefitItem", back_populates="analysis")
    risk_factors = relationship("EconomicRiskFactor", back_populates="analysis")

class CostItem(BaseModel):
    __tablename__ = "cost_items"

    analysis_id = Column(Integer, ForeignKey("economic_analyses.id"))
    category = Column(String, nullable=False)  # e.g., "capital", "operational", "regulatory"
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    frequency = Column(String, nullable=False)  # e.g., "one_time", "annual", "monthly"
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    assumptions = Column(JSON)
    
    # Relationships
    analysis = relationship("EconomicAnalysis", back_populates="cost_items")

class BenefitItem(BaseModel):
    __tablename__ = "benefit_items"

    analysis_id = Column(Integer, ForeignKey("economic_analyses.id"))
    category = Column(String, nullable=False)  # e.g., "revenue", "cost_savings", "risk_reduction"
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    frequency = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    assumptions = Column(JSON)
    
    # Relationships
    analysis = relationship("EconomicAnalysis", back_populates="benefit_items")

class EconomicRiskFactor(BaseModel):
    __tablename__ = "economic_risk_factors"

    analysis_id = Column(Integer, ForeignKey("economic_analyses.id"))
    factor_type = Column(String, nullable=False)  # e.g., "market", "regulatory", "operational"
    description = Column(String, nullable=False)
    probability = Column(Float, nullable=False)
    impact = Column(Float, nullable=False)
    mitigation_strategy = Column(String, nullable=True)
    contingency_plan = Column(String, nullable=True)
    
    # Relationships
    analysis = relationship("EconomicAnalysis", back_populates="risk_factors")

class SupplyChainCost(BaseModel):
    __tablename__ = "supply_chain_costs"

    analysis_id = Column(Integer, ForeignKey("economic_analyses.id"))
    category = Column(String, nullable=False)  # e.g., "transportation", "storage", "quality_control"
    description = Column(String, nullable=False)
    base_cost = Column(Float, nullable=False)
    variable_factors = Column(JSON)
    fixed_factors = Column(JSON)
    optimization_potential = Column(Float, nullable=True)
    
    # Relationships
    analysis = relationship("EconomicAnalysis") 