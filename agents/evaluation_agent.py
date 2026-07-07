from langchain_core.prompts import ChatPromptTemplate

from schemas.evaluation_schema import EvaluationSchema
from utils.car_repository import CarRepository
from utils.llm import get_llm
from utils.retry import invoke_with_retry


repository = CarRepository()

llm = get_llm().with_structured_output(
    EvaluationSchema
)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an experienced automobile consultant.

You are given:

1. User requirements.
2. Shortlisted vehicle variants.
3. Complete specifications.

Evaluate all shortlisted vehicles together.

Use the provided specifications as the primary source of truth.

You may use well-established general automotive knowledge
(e.g., reliability reputation, service network, ownership experience)
only when it is widely accepted and does not contradict
the provided specifications.

For each vehicle:

- Assign a suitability score (0–100)
- List strengths
- List weaknesses
- Mention what type of user or usage it is best suited for
- Write a concise summary

Do NOT recommend a final winner.

The Recommendation Agent will make the final decision.
"""
        ),
        (
            "human",
            """
User Requirements

{requirements}

Shortlisted Models

{models}

{retry_instruction}

"""
        )
    ]
)

chain = prompt | llm


def evaluation_agent(state):

    selected_models = state["selected_models"]

    model_specs = repository.get_selected_model_specs(
        selected_models
    )

    response = invoke_with_retry(
    chain=chain,
    inputs={
        "requirements": state["requirements"],
        "models": model_specs
    },
    agent_name="Evaluation Agent"
    )

    return {
    "evaluations": response.evaluations,

    "execution_log": [
        {
            "node": "Evaluation Agent",
            "message": f"Evaluated {len(response.evaluations)} vehicles."
        }
    ]
}