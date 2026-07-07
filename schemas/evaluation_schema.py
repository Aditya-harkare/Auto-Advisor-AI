from typing import List
from pydantic import BaseModel, Field


class CarEvaluation(BaseModel):

    brand: str

    model: str

    variant: str

    suitability_score: int = Field(
        ge=0,
        le=100
    )

    strengths: List[str]

    weaknesses: List[str]

    best_for: List[str]

    summary: str


class EvaluationSchema(BaseModel):

    evaluations: List[CarEvaluation]