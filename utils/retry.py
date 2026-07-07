import time
from typing import Any

from pydantic import ValidationError


class AgentExecutionError(Exception):
    """Raised when an agent fails after all retry attempts."""
    pass


# Errors that are worth retrying
RETRYABLE_ERRORS = (
    "DeadlineExceeded",
    "ServiceUnavailable",
    "InternalServerError",
    "ConnectionError",
    "ReadTimeout",
    "Timeout",
    "503",
    "500",
)


# Errors that should immediately fail
NON_RETRYABLE_ERRORS = (
    "RESOURCE_EXHAUSTED",
    "429",
    "API_KEY_INVALID",
    "401",
    "403",
    "PERMISSION_DENIED",
    "INVALID_ARGUMENT",
)


def invoke_with_retry(
    chain,
    inputs: dict,
    agent_name: str,
    max_attempts: int = 3,
    base_delay: float = 2,
) -> Any:

    retry_instruction = ""

    last_exception = None

    for attempt in range(max_attempts):

        try:

            current_inputs = dict(inputs)
            current_inputs.setdefault(
                "retry_instruction",
                retry_instruction,
            )

            response = chain.invoke(current_inputs)

            if response is None:
                raise ValueError("LLM returned None.")

            return response

        except ValidationError as e:

            last_exception = e

            retry_instruction = (
                "The previous response could not be parsed.\n"
                "Return ONLY valid structured output.\n"
                "Do not include markdown or explanations."
            )

        except Exception as e:

            last_exception = e

            error = str(e)

            # Permanent failures
            if any(code in error for code in NON_RETRYABLE_ERRORS):
                raise AgentExecutionError(
                    f"{agent_name} failed.\n\n{error}"
                )

            # Unknown error?
            if not any(code in error for code in RETRYABLE_ERRORS):

                raise AgentExecutionError(
                    f"{agent_name} failed.\n\n{error}"
                )

            retry_instruction = (
                "The previous response failed.\n"
                "Please strictly follow the required schema."
            )

        if attempt < max_attempts - 1:

            wait = base_delay * (2 ** attempt)

            print(
                f"[Retry] {agent_name}: "
                f"Retry {attempt + 2}/{max_attempts} "
                f"in {wait}s..."
            )

            time.sleep(wait)

    raise AgentExecutionError(
        f"{agent_name} failed after {max_attempts} attempts.\n\n"
        f"{last_exception}"
    )