from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

console = Console()


def render_report(report):

    recommendation = report["recommendation"]
    advisory = report["purchase_advisory"]

    console.print()

    console.print(
        Panel.fit(
            "[bold cyan]🚗 AutoAdvisor AI[/bold cyan]\n"
            "[white]Personalized Vehicle Purchase Report[/white]",
            border_style="cyan",
        )
    )

    console.print()

    # --------------------------------------------------
    # Recommended Vehicle
    # --------------------------------------------------

    vehicle = (
        f"[bold green]{recommendation['recommended_brand']} "
        f"{recommendation['recommended_model']}[/bold green]\n"
        f"[white]Variant:[/white] {recommendation['recommended_variant']}"
    )

    console.print(
        Panel(
            vehicle,
            title="🏆 Recommended Vehicle",
            border_style="green",
        )
    )

    console.print()

    console.print("[bold]Why this vehicle?[/bold]\n")

    for reason in recommendation["key_reasons"]:
        console.print(f"✅ {reason}")

    console.print()

    console.print("[bold]Trade-offs[/bold]\n")

    for tradeoff in recommendation["tradeoffs"]:
        console.print(f"⚠ {tradeoff}")

    console.print()

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    console.print(
        Panel(
            recommendation["recommendation_summary"],
            title="Recommendation Summary",
            border_style="blue",
        )
    )

    console.print()

    # --------------------------------------------------
    # Alternatives
    # --------------------------------------------------

    table = Table(
        title="🥈 Alternative Vehicles",
        box=box.ROUNDED,
        show_lines=True,
    )

    table.add_column("Brand", style="cyan")
    table.add_column("Model")
    table.add_column("Variant")
    table.add_column("Why Consider")

    for alt in recommendation["alternatives"]:

        table.add_row(
            alt["brand"],
            alt["model"],
            alt["variant"],
            alt["reason"],
        )

    console.print(table)

    console.print()

    # --------------------------------------------------
    # Insurance
    # --------------------------------------------------

    console.print(
        Panel.fit(
            "[bold]🛡 Insurance Advice[/bold]",
            border_style="yellow",
        )
    )

    for item in advisory["insurance_advice"]:
        console.print(f"• {item}")

    console.print()

    # --------------------------------------------------
    # Financing
    # --------------------------------------------------

    console.print(
        Panel.fit(
            "[bold]💰 Financing Advice[/bold]",
            border_style="yellow",
        )
    )

    for item in advisory["financing_advice"]:
        console.print(f"• {item}")

    console.print()

    # --------------------------------------------------
    # Delivery Checklist
    # --------------------------------------------------

    console.print(
        Panel.fit(
            "[bold]🚙 Delivery Checklist[/bold]",
            border_style="yellow",
        )
    )

    for item in advisory["delivery_checklist"]:
        console.print(f"☐ {item}")

    console.print()

    # --------------------------------------------------
    # Ownership Tips
    # --------------------------------------------------

    console.print(
        Panel.fit(
            "[bold]🛠 Ownership Tips[/bold]",
            border_style="yellow",
        )
    )

    for item in advisory["ownership_tips"]:
        console.print(f"• {item}")

    console.print()

    # --------------------------------------------------
    # Accessories
    # --------------------------------------------------

    console.print(
        Panel.fit(
            "[bold]🧰 Recommended Accessories[/bold]",
            border_style="yellow",
        )
    )

    for item in advisory["optional_accessories"]:
        console.print(f"• {item}")

    console.print()

    console.rule("[bold green]End of Report[/bold green]")