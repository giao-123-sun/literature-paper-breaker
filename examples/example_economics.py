"""Example: Research on digital economy and rural development.

This example demonstrates how to use the Literature Paper Breaker
to conduct automated research on an economics topic.
"""

import asyncio

from src.data_sources.base import Discipline
from src.pipeline.orchestrator import ResearchConfig, ResearchOrchestrator


async def main():
    config = ResearchConfig(
        topic="数字经济对中国乡村治理现代化的影响机制研究",
        discipline=Discipline.ECONOMICS,
        year_from=2018,
        year_to=2026,
        max_papers=40,
        language="zh",
        depth="standard",
        paper_type="research_article",
        target_word_count=10000,
        discipline_type="social_science",
        output_dir="output/digital_economy_rural",
        output_format="markdown",
        enabled_sources=["openalex", "semantic_scholar", "crossref"],
    )

    orchestrator = ResearchOrchestrator(config)

    async def on_progress(stage: str, message: str):
        print(f"[{stage}] {message}")

    session = await orchestrator.run_full_pipeline(on_progress)

    print(f"\nDone! Papers analyzed: {len(session.review_result.papers)}")
    print(f"Proposals generated: {len(session.proposals.proposals)}")
    print(f"Paper word count: {session.draft.word_count}")


if __name__ == "__main__":
    asyncio.run(main())
