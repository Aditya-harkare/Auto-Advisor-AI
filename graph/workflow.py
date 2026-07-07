from langgraph.graph import StateGraph, START, END

from graph.state import AutoAdvisorState

from agents.requirement_agent import requirement_agent
from agents.candidate_selection_agent import candidate_selection_agent
from agents.evaluation_agent import evaluation_agent
from agents.recommendation_agent import recommendation_agent
from agents.purchase_advisory_agent import purchase_advisory_agent
from graph.response_composer import response_composer

from utils.car_repository import CarRepository

repository = CarRepository()


def repository_node(state):

    candidates = repository.get_candidate_cars(
        state["requirements"]
    )

    return {
        "candidate_cars": candidates.to_dict(
            orient="records"
        ),

        "execution_log": [
            {
                "node": "Repository",
                "message": f"Retrieved {len(candidates)} candidate vehicles."
            }
        ]
    }


builder = StateGraph(AutoAdvisorState)

builder.add_node(
    "Requirement Agent",
    requirement_agent
)

builder.add_node(
    "Repository",
    repository_node
)

builder.add_node(
    "Candidate Selection Agent",
    candidate_selection_agent
)

builder.add_node(
    "Evaluation Agent",
    evaluation_agent
)

builder.add_node(
    "Recommendation Agent",
    recommendation_agent
)

builder.add_node(
    "Purchase Advisory Agent",
    purchase_advisory_agent
)

builder.add_node(
    "Response Composer",
    response_composer
)

builder.add_edge(
    START,
    "Requirement Agent"
)

builder.add_edge(
    "Requirement Agent",
    "Repository"
)

builder.add_edge(
    "Repository",
    "Candidate Selection Agent"
)

builder.add_edge(
    "Candidate Selection Agent",
    "Evaluation Agent"
)

builder.add_edge(
    "Evaluation Agent",
    "Recommendation Agent"
)

builder.add_edge(
    "Evaluation Agent",
    "Purchase Advisory Agent"
)

builder.add_edge(
    "Recommendation Agent",
    "Response Composer"
)

builder.add_edge(
    "Purchase Advisory Agent",
    "Response Composer"
)

builder.add_edge(
    "Response Composer",
    END
)



workflow = builder.compile()