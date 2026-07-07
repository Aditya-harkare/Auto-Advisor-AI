from langchain_core.prompts import ChatPromptTemplate

from schemas.purchase_advisory_schema import PurchaseAdvisorySchema
from utils.llm import get_llm
from utils.retry import invoke_with_retry


llm = get_llm().with_structured_output(
    PurchaseAdvisorySchema
)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an experienced automobile ownership consultant.

The vehicle recommendation has NOT yet been finalized.

You are given:
• User requirements
• Evaluations of shortlisted vehicles

Identify the highest suitability scoring vehicle from the evaluation results
and generate personalized purchase and ownership guidance for that vehicle.

Your advice must be tailored to BOTH:

1. The selected vehicle
2. The user's intended usage

Consider factors such as:

• Fuel type
• Body type
• Transmission
• Family size
• Primary usage
• Ownership duration
• User priority

Before generating advice, identify the three most important ownership concerns
based on the user requirements and the selected vehicle.

Prioritize your advice around these concerns.

Generate advice under these sections:

1. Insurance Advice
2. Financing Advice
3. Delivery Checklist
4. Ownership Tips
5. Recommended Accessories

Rules:

• Keep advice concise.
• Avoid generic filler.
• Tailor every recommendation to the user's scenario.
• Avoid expensive unnecessary accessories.
• Do NOT recommend another vehicle.
"""
        ),
        (
            "human",
            """
User Requirements

{requirements}

Recommended Vehicle

{recommended_vehicle}

Vehicle Evaluations

{evaluations}

{retry_instruction}

"""
        )
    ]
)

chain = prompt | llm


def purchase_advisory_agent(state):
    """
    Generate ownership guidance independently of the
    Recommendation Agent.
    """

    evaluations = state["evaluations"]

    best_vehicle = max(
        evaluations,
        key=lambda car: car.suitability_score
    )

    response = invoke_with_retry(
    chain=chain,
    inputs={
        "requirements": state["requirements"],
        "recommended_vehicle": best_vehicle,
        "evaluations": evaluations
    },
    agent_name="Purchase Advisory Agent"
    )

    return {
    "purchase_advisory": response.model_dump(),

    "execution_log": [
        {
            "node": "Purchase Advisory Agent",
            "message": "Generated ownership advisory."
        }
    ]
}