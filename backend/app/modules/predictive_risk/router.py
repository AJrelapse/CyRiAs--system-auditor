from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.modules.predictive_risk.models import PredictiveRiskResponse
from app.modules.predictive_risk.service import predictive_risk_service

router = APIRouter(
    prefix="/predictive-risk",
    tags=["Predictive Risk"]
)


@router.post(
    "/predict",
    response_model=PredictiveRiskResponse
)
def predict_risk(
    db: Session = Depends(get_db)
):

    return predictive_risk_service.predict(db)