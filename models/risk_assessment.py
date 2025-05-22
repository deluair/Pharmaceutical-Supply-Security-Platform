from sqlalchemy import Column, String, Float, ForeignKey, JSON, DateTime, Boolean, Integer
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from pydantic import BaseModel as PydanticBaseModel, Field
import numpy as np
from scipy import stats
import pandas as pd
from enum import Enum

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class RiskCategory(str, Enum):
    QUALITY = "quality"
    SAFETY = "safety"
    COMPLIANCE = "compliance"
    SUPPLY_CHAIN = "supply_chain"
    FINANCIAL = "financial"

class RiskFactorSchema(PydanticBaseModel):
    name: str
    category: RiskCategory
    description: str
    probability: float = Field(ge=0.0, le=1.0)
    impact: float = Field(ge=0.0, le=1.0)
    controls: List[str] = Field(default_factory=list)
    mitigation_actions: List[str] = Field(default_factory=list)

class RiskAssessmentSchema(PydanticBaseModel):
    timestamp: datetime
    factors: List[RiskFactorSchema]
    overall_risk_score: float = Field(ge=0.0, le=1.0)
    risk_level: RiskLevel
    recommendations: List[str] = Field(default_factory=list)

class RiskAssessmentModel:
    def __init__(self):
        self.risk_factors: Dict[str, RiskFactorSchema] = {}
        self.assessments: List[RiskAssessmentSchema] = []
        self.risk_thresholds = {
            RiskLevel.LOW: 0.3,
            RiskLevel.MEDIUM: 0.6,
            RiskLevel.HIGH: 0.8,
            RiskLevel.CRITICAL: 1.0
        }

    def add_risk_factor(self, factor: RiskFactorSchema) -> None:
        """Add a new risk factor to the assessment model."""
        self.risk_factors[factor.name] = factor

    def calculate_risk_score(self, factor: RiskFactorSchema) -> float:
        """Calculate risk score for a single factor."""
        return factor.probability * factor.impact

    def assess_risk_level(self, score: float) -> RiskLevel:
        """Determine risk level based on score."""
        for level, threshold in self.risk_thresholds.items():
            if score <= threshold:
                return level
        return RiskLevel.CRITICAL

    def perform_assessment(self) -> RiskAssessmentSchema:
        """Perform a comprehensive risk assessment."""
        if not self.risk_factors:
            raise ValueError("No risk factors defined for assessment")

        # Calculate individual risk scores
        risk_scores: List[float] = []
        for factor in self.risk_factors.values():
            score = self.calculate_risk_score(factor)
            risk_scores.append(score)

        # Calculate overall risk score (weighted average)
        overall_score = np.mean(risk_scores)
        risk_level = self.assess_risk_level(overall_score)

        # Generate recommendations
        recommendations = self._generate_recommendations(risk_level, list(self.risk_factors.values()))

        assessment = RiskAssessmentSchema(
            timestamp=datetime.utcnow(),
            factors=list(self.risk_factors.values()),
            overall_risk_score=overall_score,
            risk_level=risk_level,
            recommendations=recommendations
        )

        self.assessments.append(assessment)
        return assessment

    def _generate_recommendations(self, risk_level: RiskLevel, factors: List[RiskFactorSchema]) -> List[str]:
        """Generate recommendations based on risk level and factors."""
        recommendations = []
        
        if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            recommendations.append("Immediate action required to address high-risk factors")
            
        for factor in factors:
            if factor.probability > 0.7 or factor.impact > 0.7:
                recommendations.append(
                    f"Review and strengthen controls for {factor.name} "
                    f"({factor.category.value})"
                )
                
        return recommendations

    def get_risk_trends(self, days: int = 30) -> Dict[str, Any]:
        """Analyze risk trends over time."""
        if not self.assessments:
            return {"error": "No assessment data available"}

        # Filter assessments within the specified time range
        cutoff_date = datetime.utcnow() - pd.Timedelta(days=days)
        recent_assessments = [
            a for a in self.assessments 
            if a.timestamp >= cutoff_date
        ]

        if not recent_assessments:
            return {"error": "No assessments in the specified time range"}

        # Calculate trend metrics
        scores = [a.overall_risk_score for a in recent_assessments]
        trend_data = {
            "mean_score": np.mean(scores),
            "std_score": np.std(scores),
            "trend_direction": "increasing" if scores[-1] > scores[0] else "decreasing",
            "risk_level_distribution": self._calculate_risk_distribution(recent_assessments)
        }

        return trend_data

    def _calculate_risk_distribution(self, assessments: List[RiskAssessmentSchema]) -> Dict[RiskLevel, float]:
        """Calculate distribution of risk levels in assessments."""
        total = len(assessments)
        if total == 0:
            return {level: 0.0 for level in RiskLevel}

        distribution = {}
        for level in RiskLevel:
            count = sum(1 for a in assessments if a.risk_level == level)
            distribution[level] = count / total

        return distribution

    def get_risk_report(self) -> Dict[str, Any]:
        """Generate a comprehensive risk report."""
        if not self.assessments:
            return {"error": "No assessment data available"}

        latest_assessment = self.assessments[-1]
        trends = self.get_risk_trends()

        report = {
            "timestamp": latest_assessment.timestamp,
            "current_risk_level": latest_assessment.risk_level,
            "overall_risk_score": latest_assessment.overall_risk_score,
            "high_risk_factors": [
                factor for factor in latest_assessment.factors
                if self.calculate_risk_score(factor) > 0.7
            ],
            "recommendations": latest_assessment.recommendations,
            "trend_analysis": trends
        }

        return report

class RiskAssessment(BaseModel):
    __tablename__ = "risk_assessments"

    name = Column(String, nullable=False)
    assessment_type = Column(String, nullable=False)  # e.g., "supply_chain", "quality", "regulatory"
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    status = Column(String, nullable=False)  # e.g., "draft", "in_progress", "completed"
    overall_risk_score = Column(Float, nullable=False)
    methodology = Column(String, nullable=False)
    assumptions = Column(JSON)
    findings = Column(JSON)
    recommendations = Column(JSON)
    
    # Relationships
    risk_factors = relationship("RiskFactor", back_populates="assessment")
    mitigation_strategies = relationship("MitigationStrategy", back_populates="assessment")
    monitoring_metrics = relationship("RiskMonitoringMetric", back_populates="assessment")

class RiskFactor(BaseModel):
    __tablename__ = "risk_factors"

    assessment_id = Column(Integer, ForeignKey("risk_assessments.id"))
    category = Column(String, nullable=False)  # e.g., "geopolitical", "operational", "regulatory"
    description = Column(String, nullable=False)
    probability = Column(Float, nullable=False)
    impact = Column(Float, nullable=False)
    risk_score = Column(Float, nullable=False)
    detection_difficulty = Column(Float, nullable=False)
    time_to_impact = Column(String, nullable=False)  # e.g., "immediate", "short_term", "long_term"
    dependencies = Column(JSON)
    
    # Relationships
    assessment = relationship("RiskAssessment", back_populates="risk_factors")
    mitigations = relationship("MitigationStrategy", secondary="risk_factor_mitigations")

class MitigationStrategy(BaseModel):
    __tablename__ = "mitigation_strategies"

    assessment_id = Column(Integer, ForeignKey("risk_assessments.id"))
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    strategy_type = Column(String, nullable=False)  # e.g., "preventive", "detective", "corrective"
    effectiveness = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)
    implementation_time = Column(String, nullable=False)
    status = Column(String, nullable=False)  # e.g., "planned", "in_progress", "completed"
    metrics = Column(JSON)
    
    # Relationships
    assessment = relationship("RiskAssessment", back_populates="mitigation_strategies")
    risk_factors = relationship("RiskFactor", secondary="risk_factor_mitigations")

class RiskMonitoringMetric(BaseModel):
    __tablename__ = "risk_monitoring_metrics"

    assessment_id = Column(Integer, ForeignKey("risk_assessments.id"))
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    metric_type = Column(String, nullable=False)  # e.g., "leading", "lagging"
    target_value = Column(Float, nullable=False)
    current_value = Column(Float, nullable=False)
    threshold = Column(Float, nullable=False)
    frequency = Column(String, nullable=False)  # e.g., "daily", "weekly", "monthly"
    data_source = Column(String, nullable=False)
    
    # Relationships
    assessment = relationship("RiskAssessment", back_populates="monitoring_metrics")

# Association table for many-to-many relationship between RiskFactor and MitigationStrategy
class RiskFactorMitigation(BaseModel):
    __tablename__ = "risk_factor_mitigations"

    risk_factor_id = Column(Integer, ForeignKey("risk_factors.id"), primary_key=True)
    mitigation_strategy_id = Column(Integer, ForeignKey("mitigation_strategies.id"), primary_key=True)
    effectiveness = Column(Float, nullable=False)
    implementation_status = Column(String, nullable=False)
    last_review_date = Column(DateTime, nullable=True)
    review_notes = Column(String, nullable=True) 