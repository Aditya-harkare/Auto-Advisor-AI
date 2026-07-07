from langchain_core.prompts import ChatPromptTemplate

from schemas.candidate_selection_schema import CandidateSelectionSchema
from utils.llm import get_llm
from utils.car_repository import CarRepository
from utils.retry import invoke_with_retry
import pandas as pd

# Repository
repository = CarRepository()

# LLM
llm = get_llm().with_structured_output(CandidateSelectionSchema)

# Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert automobile consultant.

The candidate vehicles have already been filtered using the user's hard constraints.

Your task is ONLY to shortlist the best candidate models for further evaluation.

Do not infer maintenance costs,
service quality,
long-term reliability,
ownership experience,
or resale value unless they are directly supported by the provided specifications.

Those aspects will be evaluated by another specialist agent.

Select vehicles based only on:
- user constraints
- provided specifications
- overall suitability
- diversity of recommendations

Before selecting a variant, verify that it satisfies all explicit user constraints
such as budget, transmission, fuel type, seating capacity, and body type.
Do not select variants that violate these hard constraints.

Rules:

1. Select between 5 and 10 DISTINCT MODELS.
2. For each selected model, choose ONE specific variant that best matches the user's requirements.
3. Avoid selecting multiple variants of the same model unless absolutely necessary.
4. Use only the provided vehicle specifications.
5. Briefly explain why the model deserves further evaluation.
6. Assign a confidence score between 0 and 1.

Do NOT rank the models.
Do NOT recommend a final vehicle.
Do NOT compare shortlisted models in detail.
"""
        ),
        (
            "human",
            """
User Requirements:
{requirements}

Candidate Vehicles:
{candidate_cars}

{retry_instruction}
"""
        )
    ]
)


chain = prompt | llm


def candidate_selection_agent(state):

    candidates_df = pd.DataFrame(state["candidate_cars"])

    compact_candidates = repository.get_compact_candidates(candidates_df)

    response = invoke_with_retry(
    chain=chain,
    inputs={
        "requirements": state["requirements"],
        "candidate_cars": compact_candidates
    },
    agent_name="Candidate Selection Agent"
    )

    return {
    "selected_models": response.selected_models,

    "execution_log": [
        {
            "node": "Candidate Selection Agent",
            "message": f"Shortlisted {len(response.selected_models)} models."
        }
    ]
}