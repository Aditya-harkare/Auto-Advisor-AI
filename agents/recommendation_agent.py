from langchain_core.prompts import ChatPromptTemplate

from schemas.recommendation_schema import RecommendationSchema
from utils.llm import get_llm
from utils.retry import invoke_with_retry

llm = get_llm().with_structured_output(
    RecommendationSchema
)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an experienced automobile consultant.

You are given:

1. User requirements.
2. Evaluations of shortlisted vehicles.

Your responsibility is to recommend ONE vehicle.

Instructions:

1. Select the single best vehicle.
2. Explain why it is the best fit.
3. Mention important trade-offs.
4. Suggest up to 3 alternatives with brief reasons.
5. Base your recommendation on:
   - User priorities
   - Evaluation results
   - Overall suitability

Do not invent specifications.
Use the evaluation summaries as the primary source.
"""
        ),
        (
            "human",
            """
User Requirements

{requirements}

Vehicle Evaluations

{evaluations}

{retry_instruction}

"""
        )
    ]
)

chain = prompt | llm


def recommendation_agent(state):
    """
    Generate the final recommendation.
    """

    response = invoke_with_retry(
    chain=chain,
    inputs={
        "requirements": state["requirements"],
        "evaluations": state["evaluations"]
    },
    agent_name="Recommendation Agent"
    )

    return {
    "recommendation": response.model_dump(),

    "execution_log": [
        {
            "node": "Recommendation Agent",
            "message": "Generated recommendation."
        }
    ]
}