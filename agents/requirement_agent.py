from langchain_core.prompts import ChatPromptTemplate

from schemas.requirement_schema import RequirementSchema
from utils.llm import get_llm
from utils.retry import invoke_with_retry

llm = get_llm().with_structured_output(RequirementSchema)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert automobile consultant.

Your task is to extract the user's automobile purchasing requirements.

Only extract information explicitly mentioned by the user.

If a field is not mentioned, leave it empty.

Do not make assumptions.
"""
        ),
        (
            "human",
            """
User Query:

{user_query}

{retry_instruction}
"""
        ),
    ]
)

chain = prompt | llm


def requirement_agent(state):

    response = invoke_with_retry(
        chain=chain,
        inputs={
            "user_query": state["user_query"]
        },
        agent_name="Requirement Agent"
    )

    return {
        "requirements": response.model_dump(),
        "execution_log": [
            {
                "node": "Requirement Agent",
                "message": "Requirements extracted successfully."
            }
        ]
    }