from pydantic import BaseModel
from typing import List


class PredictionReason(BaseModel):
    category: str
    description: str
    score: float


class AssetPrediction(BaseModel):
    asset_id: str
    current_score: float
    predicted_score: float
    confidence: float
    prediction_window: str
    risk_level: str
    reasons: List[PredictionReason]


class PredictiveRiskResponse(BaseModel):
    total_assets: int
    predictions: List[AssetPrediction]