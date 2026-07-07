from rich.prompt import Prompt

from graph.workflow import workflow
from utils.logger import section, success, info
from utils.report_renderer import render_report


section("AutoAdvisor AI")

while True:

    query = Prompt.ask(
        "[bold green]Enter your car requirements[/bold green]"
    )

    if query.strip().lower() in {"exit", "quit"}:
        success("Thank you for using AutoAdvisor AI!")
        break

    info(f"User Query:\n{query}")

    state = {
        "user_query": query,
        "execution_log": []
    }

    result = workflow.invoke(state)

    print("\n========== WORKFLOW EXECUTION ==========\n")

    for log in result["execution_log"]:
        print(f"✓ {log['node']}")
        print(f"  {log['message']}\n")

    success("Workflow completed successfully!")

    section("Consultation Report")

    render_report(
        result["consultation_report"]
    )

    print("\n" + "=" * 80 + "\n")