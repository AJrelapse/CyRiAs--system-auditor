from pydantic import BaseModel

from typing import List


class RiskRecommendation(BaseModel):

    priority: int

    recommendation: str


class AssetRiskAssessment(BaseModel):

    asset_id: str

    overall_score: float

    risk_level: str

    predictive_score: float

    attack_path_score: float

    criticality_score: float

    behavioral_score: float

    recommendations: List[RiskRecommendation]


class RiskAssessmentResponse(BaseModel):

    total_assets: int

    average_risk_score: float

    highest_risk_asset: str | None

    assessments: List[AssetRiskAssessment]