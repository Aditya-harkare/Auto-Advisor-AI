from typing import List

from pydantic import BaseModel, Field


class AlternativeCar(BaseModel):
    brand: str
    model: str
    variant: str
    reason: str


class RecommendationSchema(BaseModel):

    recommended_brand: str

    recommended_model: str

    recommended_variant: str

    recommendation_summary: str = Field(
        description="Overall recommendation for the user."
    )

    key_reasons: List[str] = Field(
        description="Top reasons for recommending this vehicle."
    )

    tradeoffs: List[str] = Field(
        description="Trade-offs the user should know."
    )

    alternatives: List[AlternativeCar]