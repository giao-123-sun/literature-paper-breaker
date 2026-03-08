"""Example: Historical research on Silk Road trade networks.

This example demonstrates humanities-style research with
interpretive research questions rather than testable hypotheses.
"""

import asyncio

from src.data_sources.base import Discipline
from src.pipeline.orchestrator import ResearchConfig, ResearchOrchestrator


async def main():
    config = ResearchConfig(
        topic="Maritime Silk Road and cross-cultural exchange in Southeast Asia (15th-17th century)",
        discipline=Discipline.HISTORY,
        year_from=2010,
        year_to=2026,
        max_papers=60,
        language="en",
        depth="deep",
        paper_type="research_article",
        target_word_count=12000,
        discipline_type="humanities",  # Use interpretive questions
        output_dir="output/silk_road",
        output_format="markdown",
        enabled_sources=["openalex", "semantic_scholar", "crossref", "ctext"],
    )

    orchestrator = ResearchOrchestrator(config)

    async def on_progress(stage: str, message: str):
        print(f"[{stage}] {message}")

    session = await orchestrator.run_full_pipeline(on_progress)

    print(f"\nDone! Papers analyzed: {len(session.review_result.papers)}")
    print(f"Output saved to: {config.output_dir}/")


if __name__ == "__main__":
    asyncio.run(main())
