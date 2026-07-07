from rich.console import Console

console = Console()


def section(title: str):
    console.rule(f"[bold cyan]{title}")


def success(message: str):
    console.print(f"[green]✓[/green] {message}")


def info(message: str):
    console.print(f"[cyan]{message}[/cyan]")