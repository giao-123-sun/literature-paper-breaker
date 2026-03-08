#!/usr/bin/env python3
"""Production runner: Generate 2-3 academic papers using OpenRouter.

Usage:
    export OPENROUTER_API_KEY="sk-or-v1-..."
    python scripts/run_papers.py

Budget: $25 for 2-3 papers with peer review.
"""

import asyncio
import json
import logging
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pipeline.orchestrator import ResearchConfig, ResearchOrchestrator
from src.data_sources.base import Discipline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("paper_runner")

# Model strategy for $25 budget (updated from OpenRouter research):
# - deepseek/deepseek-chat (V3.2): $0.24/1M input, $0.38/1M output — BEST value
# - qwen/qwen-2.5-72b-instruct: $0.04/1M input, $0.10/1M output — cheapest
# - google/gemini-2.5-flash: $0.30/1M input, $2.50/1M output — avoid (expensive output)
# - anthropic/claude-sonnet-4: $3/1M input, $15/1M output — highest quality, expensive
#
# Strategy: DeepSeek V3.2 for everything — ~90% of frontier quality at <$0.15/paper
# Total 3 papers with peer review: well under $1 of the $25 budget

PAPERS = [
    {
        "topic": "Large Language Models as Cultural Agents: How AI-Generated Text Reshapes "
                 "Collective Memory and Historical Narratives in the Digital Public Sphere",
        "discipline": Discipline.SOCIOLOGY,
        "discipline_type": "social_science",
        "language": "en",
        "target_words": 8000,
        "paper_type": "research_article",
    },
    {
        "topic": "数字孪生与非物质文化遗产保护：人工智能时代传统手工艺知识图谱的构建与传承路径研究",
        "discipline": Discipline.ANTHROPOLOGY,
        "discipline_type": "humanities",
        "language": "zh",
        "target_words": 10000,
        "paper_type": "research_article",
    },
    {
        "topic": "The Algorithmic Flaneur: Psychogeography, Attention Economics, and the "
                 "Phenomenology of AI-Mediated Urban Experience",
        "discipline": Discipline.PHILOSOPHY,
        "discipline_type": "humanities",
        "language": "en",
        "target_words": 7000,
        "paper_type": "essay",
    },
]


async def run_single_paper(paper_config: dict, paper_num: int, total: int):
    """Run the full pipeline for one paper."""
    topic = paper_config["topic"]
    logger.info(f"\n{'='*60}")
    logger.info(f"Paper {paper_num}/{total}: {topic[:60]}...")
    logger.info(f"{'='*60}")

    config = ResearchConfig(
        topic=topic,
        discipline=paper_config["discipline"],
        discipline_type=paper_config["discipline_type"],
        language=paper_config["language"],
        target_word_count=paper_config["target_words"],
        paper_type=paper_config["paper_type"],
        depth="standard",
        max_papers=30,
        output_dir=f"output/paper_{paper_num}",
        output_format="markdown",
        # OpenRouter with cost-effective model
        llm_provider="openrouter",
        llm_model="deepseek/deepseek-chat",
        enabled_sources=["openalex", "semantic_scholar", "crossref"],
        enable_peer_review=True,
        num_reviewers=3,
        review_rounds=1,
    )

    start = time.time()
    orchestrator = ResearchOrchestrator(config)

    async def progress(stage, msg):
        elapsed = time.time() - start
        logger.info(f"  [{elapsed:.0f}s] Stage: {stage} — {msg}")

    try:
        session = await orchestrator.run_full_pipeline(progress)
        elapsed = time.time() - start

        logger.info(f"\n  Paper {paper_num} complete in {elapsed:.0f}s")
        if session.draft:
            logger.info(f"  Word count: ~{session.draft.word_count}")
        if session.peer_review_result:
            pr = session.peer_review_result
            logger.info(f"  Peer review score: {pr.average_score:.1f}/10")
            logger.info(f"  Decision: {pr.consensus_decision}")
            reviewers = [r.reviewer.name for r in pr.reviews]
            logger.info(f"  Reviewers: {', '.join(reviewers)}")
        logger.info(f"  API usage: {orchestrator.llm.usage.summary()}")

        return {
            "paper_num": paper_num,
            "topic": topic[:60],
            "word_count": session.draft.word_count if session.draft else 0,
            "review_score": session.peer_review_result.average_score if session.peer_review_result else 0,
            "api_calls": orchestrator.llm.usage.total_calls,
            "input_tokens": orchestrator.llm.usage.total_input_tokens,
            "output_tokens": orchestrator.llm.usage.total_output_tokens,
            "elapsed_s": elapsed,
            "errors": session.errors,
        }
    except Exception as e:
        logger.error(f"  Paper {paper_num} failed: {e}")
        return {"paper_num": paper_num, "topic": topic[:60], "error": str(e)}


async def main():
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        print("ERROR: Set OPENROUTER_API_KEY environment variable")
        sys.exit(1)

    logger.info("Literature Paper Breaker — Production Run")
    logger.info(f"Papers to generate: {len(PAPERS)}")
    logger.info(f"Model: deepseek/deepseek-chat (V3.2) via OpenRouter")
    logger.info(f"Budget: $25")

    results = []
    for i, paper in enumerate(PAPERS, 1):
        result = await run_single_paper(paper, i, len(PAPERS))
        results.append(result)
        logger.info(f"\n--- Cumulative progress: {i}/{len(PAPERS)} papers ---\n")

    # Final summary
    logger.info("\n" + "=" * 60)
    logger.info("FINAL SUMMARY")
    logger.info("=" * 60)

    total_input = sum(r.get("input_tokens", 0) for r in results)
    total_output = sum(r.get("output_tokens", 0) for r in results)
    total_calls = sum(r.get("api_calls", 0) for r in results)

    # DeepSeek V3.2 pricing on OpenRouter
    cost_input = total_input * 0.24 / 1_000_000
    cost_output = total_output * 0.38 / 1_000_000
    total_cost = cost_input + cost_output

    for r in results:
        status = f"OK ({r.get('word_count', 0)} words, score {r.get('review_score', 0):.1f})" \
                 if 'error' not in r else f"FAILED: {r['error']}"
        logger.info(f"  Paper {r['paper_num']}: {status}")

    logger.info(f"\n  Total API calls: {total_calls}")
    logger.info(f"  Total tokens: {total_input:,} in + {total_output:,} out")
    logger.info(f"  Estimated cost: ${total_cost:.2f}")
    logger.info(f"  Budget remaining: ~${25 - total_cost:.2f}")

    # Save summary
    os.makedirs("output", exist_ok=True)
    with open("output/run_summary.json", "w") as f:
        json.dump({
            "results": results,
            "total_cost_estimate": total_cost,
            "total_tokens": {"input": total_input, "output": total_output},
        }, f, indent=2, ensure_ascii=False)
    logger.info(f"\n  Summary saved to output/run_summary.json")


if __name__ == "__main__":
    asyncio.run(main())
