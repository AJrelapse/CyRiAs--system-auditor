from pydantic import BaseModel


class AttackPath(BaseModel):

    path: list[str]

    risk_score: float

    techniques: list[str]


class AttackPathResponse(BaseModel):

    total_paths: int

    attack_paths: list[AttackPath]