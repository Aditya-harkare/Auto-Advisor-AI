from typing import Annotated, TypedDict
import operator


class AutoAdvisorState(TypedDict):

    # Initial Input
    user_query: str

    # Produced by Requirement Agent
    requirements: dict

    # Produced by Repository
    candidate_cars: list

    # Produced by Candidate Selection Agent
    selected_models: list

    # Produced by Evaluation Agent
    evaluations: list

    # Produced by Recommendation Agent
    recommendation: dict

    # Produced by Purchase Advisory Agent
    purchase_advisory: dict

    # Produced by Response Composer
    consultation_report: dict

    # Parallel-safe log
    execution_log: Annotated[list, operator.add]