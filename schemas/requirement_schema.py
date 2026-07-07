from typing import Optional

from pydantic import BaseModel


class RequirementSchema(BaseModel):

    budget: Optional[int] = None

    body_type: Optional[str] = None

    fuel_type: Optional[str] = None

    transmission: Optional[str] = None

    family_size: Optional[int] = None

    primary_usage: Optional[str] = None

    ownership_years: Optional[int] = None

    priority: Optional[str] = None