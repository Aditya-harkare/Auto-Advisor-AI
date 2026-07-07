from typing import List

from pydantic import BaseModel, Field



class SelectedCar(BaseModel):
    """
    Represents one shortlisted vehicle variant.
    """

    brand: str = Field(description="Vehicle manufacturer")

    model: str = Field(description="Vehicle model")

    variant: str = Field(
        description="Exact variant selected for evaluation."
    )

    reason: str = Field(
        description="Reason for selecting this model."
    )

    confidence: float = Field(
        ge=0,
        le=1,
        description="Confidence score between 0 and 1."
    )


class CandidateSelectionSchema(BaseModel):

    selected_models: List[SelectedCar]


class CandidateSelectionSchema(BaseModel):
    """
    Output of the Candidate Selection Agent.
    """

    selected_models: List[SelectedCar]