"""Command-line interface for Literature Paper Breaker."""

from __future__ import annotations

import asyncio
import sys

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from .data_sources.base import Discipline
from .pipeline.orchestrator import ResearchConfig, ResearchOrchestrator

console = Console()

DISCIPLINE_CHOICES = {d.value: d for d in Discipline}

BANNER = """
╔═══════════════════════════════════════════════════════════════╗
║         Literature Paper Breaker (LPB) v0.1.0                ║
║   AI-Powered Humanities & Social Science Research System      ║
╚═══════════════════════════════════════════════════════════════╝
"""


@click.group()
@click.version_option(version="0.1.0")
def main():
    """Literature Paper Breaker - AI-powered humanities research automation."""
    pass


@main.command()
@click.argument("topic")
@click.option(
    "--discipline", "-d",
    type=click.Choice(list(DISCIPLINE_CHOICES.keys())),
    default="general",
    help="Academic discipline",
)
@click.option("--year-from", "-yf", type=int, default=None, help="Start year")
@click.option("--year-to", "-yt", type=int, default=None, help="End year")
@click.option("--max-papers", "-n", type=int, default=50, help="Max papers to analyze")
@click.option("--language", "-l", default="en", help="Language (en, zh, etc.)")
@click.option(
    "--depth",
    type=click.Choice(["quick", "standard", "deep"]),
    default="standard",
    help="Review depth",
)
@click.option(
    "--paper-type",
    type=click.Choice(["research_article", "review", "essay", "commentary"]),
    default="research_article",
    help="Paper type",
)
@click.option("--target-words", "-w", type=int, default=8000, help="Target word count")
@click.option(
    "--discipline-type",
    type=click.Choice(["humanities", "social_science"]),
    default="social_science",
    help="Research approach",
)
@click.option("--output-dir", "-o", default="output", help="Output directory")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["markdown", "latex"]),
    default="markdown",
    help="Output format",
)
@click.option("--provider", default="anthropic", help="LLM provider (anthropic/openai)")
@click.option("--model", default=None, help="LLM model name")
@click.option(
    "--sources",
    default="openalex,semantic_scholar,crossref",
    help="Comma-separated data sources",
)
@click.option("--peer-review/--no-peer-review", default=False, help="Enable simulated peer review")
@click.option("--reviewers", type=int, default=3, help="Number of peer reviewers (default: 3)")
@click.option("--review-rounds", type=int, default=1, help="Rounds of review-revise cycles")
def research(
    topic: str,
    discipline: str,
    year_from: int | None,
    year_to: int | None,
    max_papers: int,
    language: str,
    depth: str,
    paper_type: str,
    target_words: int,
    discipline_type: str,
    output_dir: str,
    output_format: str,
    provider: str,
    model: str | None,
    sources: str,
    peer_review: bool,
    reviewers: int,
    review_rounds: int,
):
    """Run the full research pipeline on a topic.

    Example:
        lpb research "The impact of digital transformation on rural governance in China"
        lpb research "认知语言学中的隐喻理论演变" -d linguistics -l zh --depth deep
    """
    console.print(BANNER, style="bold cyan")

    if model is None:
        model = (
            "claude-sonnet-4-20250514" if provider == "anthropic"
            else "gpt-4o"
        )

    config = ResearchConfig(
        topic=topic,
        discipline=DISCIPLINE_CHOICES.get(discipline, Discipline.GENERAL),
        year_from=year_from,
        year_to=year_to,
        max_papers=max_papers,
        language=language,
        depth=depth,
        paper_type=paper_type,
        target_word_count=target_words,
        discipline_type=discipline_type,
        output_dir=output_dir,
        output_format=output_format,
        llm_provider=provider,
        llm_model=model,
        enabled_sources=sources.split(","),
        enable_peer_review=peer_review,
        num_reviewers=reviewers,
        review_rounds=review_rounds,
    )

    # Display config
    table = Table(title="Research Configuration", show_header=False)
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Topic", config.topic)
    table.add_row("Discipline", config.discipline.value)
    table.add_row("Depth", config.depth)
    table.add_row("Language", config.language)
    table.add_row("Max Papers", str(config.max_papers))
    table.add_row("LLM", f"{config.llm_provider}/{config.llm_model}")
    table.add_row("Sources", ", ".join(config.enabled_sources))
    if peer_review:
        table.add_row("Peer Review", f"{reviewers} reviewers, {review_rounds} round(s)")
    table.add_row("Output", f"{config.output_dir}/ ({config.output_format})")
    console.print(table)
    console.print()

    asyncio.run(_run_research(config))


async def _run_research(config: ResearchConfig):
    """Run the research pipeline with progress display."""
    orchestrator = ResearchOrchestrator(config)

    total = 6 if config.enable_peer_review else 5
    stage_messages = {
        "reviewing": f"[bold blue]Stage 1/{total}:[/] Conducting literature review...",
        "analyzing": f"[bold blue]Stage 2/{total}:[/] Analyzing research gaps...",
        "proposing": f"[bold blue]Stage 3/{total}:[/] Generating research proposals...",
        "outlining": f"[bold blue]Stage 4/{total}:[/] Creating paper outline...",
        "writing": f"[bold blue]Stage 5/{total}:[/] Writing paper draft...",
        "peer_reviewing": f"[bold blue]Stage 6/{total}:[/] Simulating peer review...",
        "complete": "[bold green]Pipeline complete![/]",
    }

    async def progress_callback(stage: str, message: str):
        display = stage_messages.get(stage, message)
        console.print(display)

    try:
        session = await orchestrator.run_full_pipeline(progress_callback)

        # Display results summary
        console.print()
        console.print(Panel("[bold green]Research Complete!", title="Status"))

        if session.review_result:
            console.print(f"  Papers analyzed: {len(session.review_result.papers)}")
            console.print(f"  Themes found: {len(session.review_result.themes)}")
            console.print(f"  Gaps identified: {len(session.review_result.gaps)}")

        if session.proposals:
            console.print(f"  Proposals generated: {len(session.proposals.proposals)}")

        if session.draft:
            console.print(f"  Paper word count: ~{session.draft.word_count}")

        if session.peer_review_result:
            pr = session.peer_review_result
            console.print(f"  Peer review score: {pr.average_score:.1f}/10")
            console.print(f"  Review decision: {pr.consensus_decision}")
            console.print(f"  Reviewers: {', '.join(r.reviewer.name for r in pr.reviews)}")

        console.print(f"\n  Output saved to: [cyan]{config.output_dir}/[/]")

        if session.errors:
            console.print("\n[yellow]Warnings:[/]")
            for err in session.errors:
                console.print(f"  - {err}")

    except Exception as e:
        console.print(f"\n[bold red]Error:[/] {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument("topic")
@click.option("--discipline", "-d", default="general", help="Discipline")
@click.option("--language", "-l", default="en", help="Language")
@click.option("--max-papers", "-n", type=int, default=30, help="Max papers")
@click.option("--output-dir", "-o", default="output", help="Output directory")
@click.option("--depth", default="standard", help="Review depth")
@click.option("--provider", default="anthropic", help="LLM provider")
@click.option("--model", default=None, help="LLM model")
@click.option(
    "--sources",
    default="openalex,semantic_scholar,crossref",
    help="Data sources",
)
def review(
    topic: str,
    discipline: str,
    language: str,
    max_papers: int,
    output_dir: str,
    depth: str,
    provider: str,
    model: str | None,
    sources: str,
):
    """Run only the literature review stage.

    Example:
        lpb review "Confucian ethics in modern corporate governance"
    """
    console.print(BANNER, style="bold cyan")

    if model is None:
        model = (
            "claude-sonnet-4-20250514" if provider == "anthropic"
            else "gpt-4o"
        )

    config = ResearchConfig(
        topic=topic,
        discipline=DISCIPLINE_CHOICES.get(discipline, Discipline.GENERAL),
        max_papers=max_papers,
        language=language,
        depth=depth,
        output_dir=output_dir,
        llm_provider=provider,
        llm_model=model,
        enabled_sources=sources.split(","),
    )

    asyncio.run(_run_review(config))


async def _run_review(config: ResearchConfig):
    orchestrator = ResearchOrchestrator(config)
    try:
        console.print("[bold blue]Conducting literature review...[/]")
        session = await orchestrator.run_review_only()
        if session.review_result:
            console.print(
                f"\n[green]Review complete![/] "
                f"Analyzed {len(session.review_result.papers)} papers."
            )
            console.print(f"Output saved to: [cyan]{config.output_dir}/[/]")
    except Exception as e:
        console.print(f"\n[bold red]Error:[/] {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument("query")
@click.option(
    "--source",
    "-s",
    multiple=True,
    default=["openalex"],
    help="Data sources to search",
)
@click.option("--limit", "-n", type=int, default=10, help="Number of results")
@click.option("--year-from", type=int, default=None, help="Start year")
@click.option("--year-to", type=int, default=None, help="End year")
def search(query: str, source: tuple, limit: int, year_from: int | None, year_to: int | None):
    """Search academic databases directly.

    Example:
        lpb search "digital humanities methodology" -s openalex -s semantic_scholar
    """
    asyncio.run(_run_search(query, list(source), limit, year_from, year_to))


async def _run_search(
    query: str, sources: list[str], limit: int, year_from: int | None, year_to: int | None
):
    from .data_sources.aggregator import AggregatedSource

    agg = AggregatedSource()
    if "openalex" in sources:
        agg.add_source(OpenAlexSource())
    if "semantic_scholar" in sources:
        agg.add_source(SemanticScholarSource())
    if "crossref" in sources:
        agg.add_source(CrossRefSource())

    console.print(f"Searching for: [cyan]{query}[/]")

    try:
        result = await agg.search(
            query, limit=limit, year_from=year_from, year_to=year_to
        )

        table = Table(title=f"Search Results ({result.total_count} total)")
        table.add_column("#", style="dim", width=3)
        table.add_column("Title", style="cyan", max_width=50)
        table.add_column("Authors", max_width=25)
        table.add_column("Year", width=5)
        table.add_column("Citations", width=8)
        table.add_column("Source", width=10)

        for i, paper in enumerate(result.papers[:limit], 1):
            authors = ", ".join(paper.authors[:2])
            if len(paper.authors) > 2:
                authors += " et al."
            table.add_row(
                str(i),
                paper.title[:50],
                authors[:25],
                str(paper.year or ""),
                str(paper.citations_count),
                paper.source,
            )

        console.print(table)
    finally:
        await agg.close()


@main.command()
def sources():
    """List available data sources and their status."""
    table = Table(title="Available Data Sources")
    table.add_column("Source", style="cyan")
    table.add_column("Type", width=12)
    table.add_column("Auth Required", width=13)
    table.add_column("Full Text", width=10)
    table.add_column("Citations", width=10)
    table.add_column("Status")

    import os

    source_info = [
        ("OpenAlex", "Open catalog", False, False, True, True),
        ("Semantic Scholar", "AI-powered", False, False, True, True),
        ("CrossRef", "DOI registry", False, False, False, True),
        ("CORE", "Open access", True, True, False, bool(os.environ.get("CORE_API_KEY"))),
        ("CText", "Chinese classics", False, True, False, True),
    ]

    for name, type_, auth, fulltext, citations, available in source_info:
        status = "[green]Available[/]" if available else "[yellow]Need API key[/]"
        table.add_row(
            name,
            type_,
            "Yes" if auth else "No",
            "Yes" if fulltext else "No",
            "Yes" if citations else "No",
            status,
        )

    console.print(table)

    console.print("\n[bold]Credential-based sources (bring your own login):[/]")
    console.print("  - CNKI (中国知网) - via institutional proxy")
    console.print("  - JSTOR - via institutional access")
    console.print("  - Web of Science / SSCI / A&HCI - via institutional access")
    console.print("\nSet credentials in .env file. See .env.example for details.")


if __name__ == "__main__":
    main()
