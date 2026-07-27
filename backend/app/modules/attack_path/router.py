from fastapi import APIRouter

from app.modules.attack_path.service import (
    attack_path_service,
)

router = APIRouter(
    prefix="/attack-path",
    tags=["Attack Path"],
)


@router.post("/generate")
def generate_attack_paths():

    return attack_path_service.generate_attack_paths()