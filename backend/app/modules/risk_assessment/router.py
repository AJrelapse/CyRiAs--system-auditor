from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.modules.risk_assessment.service import (
    risk_assessment_service,
)

router = APIRouter(
    prefix="/risk-assessment",
    tags=["Risk Assessment"],
)


@router.post("/assess")
def assess_risk(
    db: Session = Depends(get_db),
):
    return risk_assessment_service.assess(db)