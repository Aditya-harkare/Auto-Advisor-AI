from typing import List

from pydantic import BaseModel


class PurchaseAdvisorySchema(BaseModel):

    insurance_advice: List[str]

    financing_advice: List[str]

    delivery_checklist: List[str]

    ownership_tips: List[str]

    optional_accessories: List[str]