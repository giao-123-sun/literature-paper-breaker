"""Research orchestrator - coordinates the full research pipeline.

This is the main entry point that ties together:
1. Literature search and review
2. Gap analysis
3. Hypothesis generation
4. Paper outlining and writing
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..data_sources.aggregator import AggregatedSource
from ..data_sources.base import Discipline
from ..data_sources.openalex import OpenAlexSource
from ..data_sources.semantic_scholar import SemanticScholarSource
from ..data_sources.crossref import CrossRefSource
from ..data_sources.core_ac import CoreSource
from ..data_sources.ctext import CTextSource
from ..paper_engine.outliner import PaperOutliner
from ..paper_engine.writer import PaperWriter
from ..utils.llm import LLMClient, LLMConfig
from .gap_analyzer import GapAnalyzer
from .hypothesis_generator import HypothesisGenerator
from .literature_review import LiteratureReviewer

logger = logging.getLogger(__name__)


@dataclass
class ResearchConfig:
    """Configuration for a research session."""

    topic: str
    discipline: Discipline = Discipline.GENERAL
    year_from: int | None = None
    year_to: int | None = None
    max_papers: int = 50
    language: str = "en"
    depth: str = "standard"  # quick, standard, deep
    paper_type: str = "research_article"
    target_word_count: int = 8000
    discipline_type: str = "social_science"  # humanities or social_science
    output_dir: str = "output"
    output_format: str = "markdown"  # markdown or latex
    llm_provider: str = "anthropic"
    llm_model: str = "claude-sonnet-4-20250514"
    enabled_sources: list[str] = field(
        default_factory=lambda: ["openalex", "semantic_scholar", "crossref"]
    )


@dataclass
class ResearchSession:
    """Tracks the state of a research session."""

    config: ResearchConfig
    stage: str = "initialized"  # initialized, reviewing, analyzing, proposing, outlining, writing, complete
    review_result: Any = None
    gap_result: Any = None
    proposals: Any = None
    outline: Any = None
    draft: Any = None
    errors: list[str] = field(default_factory=list)


class ResearchOrchestrator:
    """Orchestrates the full research pipeline."""

    def __init__(self, config: ResearchConfig):
        self.config = config
        self.session = ResearchSession(config=config)

        # Initialize LLM
        self.llm = LLMClient(LLMConfig(
            provider=config.llm_provider,
            model=config.llm_model,
        ))

        # Initialize data sources
        self.sources = self._init_sources()

        # Initialize pipeline components
        self.reviewer = LiteratureReviewer(self.sources, self.llm)
        self.gap_analyzer = GapAnalyzer(self.llm)
        self.hypothesis_gen = HypothesisGenerator(self.llm)
        self.outliner = PaperOutliner(self.llm)
        self.writer = PaperWriter(self.llm)

    def _init_sources(self) -> AggregatedSource:
        """Initialize configured data sources."""
        agg = AggregatedSource()
        enabled = self.config.enabled_sources

        if "openalex" in enabled:
            agg.add_source(OpenAlexSource())
        if "semantic_scholar" in enabled:
            agg.add_source(SemanticScholarSource())
        if "crossref" in enabled:
            agg.add_source(CrossRefSource())
        if "core" in enabled:
            api_key = os.environ.get("CORE_API_KEY")
            if api_key:
                agg.add_source(CoreSource(api_key))
        if "ctext" in enabled:
            agg.add_source(CTextSource())

        return agg

    async def run_full_pipeline(
        self, progress_callback: Any = None
    ) -> ResearchSession:
        """Run the complete research pipeline.

        Args:
            progress_callback: Optional async callback(stage, message) for progress updates
        """
        try:
            await self._run_stage(
                "reviewing",
                "Conducting literature review...",
                self._do_review,
                progress_callback,
            )

            await self._run_stage(
                "analyzing",
                "Analyzing research gaps...",
                self._do_gap_analysis,
                progress_callback,
            )

            await self._run_stage(
                "proposing",
                "Generating research proposals...",
                self._do_hypothesis_generation,
                progress_callback,
            )

            await self._run_stage(
                "outlining",
                "Creating paper outline...",
                self._do_outline,
                progress_callback,
            )

            await self._run_stage(
                "writing",
                "Writing paper draft...",
                self._do_writing,
                progress_callback,
            )

            self.session.stage = "complete"
            if progress_callback:
                await progress_callback("complete", "Research pipeline complete!")

            # Save outputs
            await self._save_outputs()

        except Exception as e:
            logger.error(f"Pipeline error at stage {self.session.stage}: {e}")
            self.session.errors.append(f"[{self.session.stage}] {str(e)}")
            raise
        finally:
            await self.sources.close()
            await self.llm.close()

        return self.session

    async def run_review_only(self) -> ResearchSession:
        """Run only the literature review stage."""
        try:
            await self._do_review()
            await self._save_outputs()
        finally:
            await self.sources.close()
            await self.llm.close()
        return self.session

    async def _run_stage(self, stage, message, func, callback=None):
        self.session.stage = stage
        if callback:
            await callback(stage, message)
        logger.info(message)
        await func()

    async def _do_review(self):
        self.session.review_result = await self.reviewer.review(
            self.config.topic,
            discipline=self.config.discipline,
            year_from=self.config.year_from,
            year_to=self.config.year_to,
            max_papers=self.config.max_papers,
            language=self.config.language,
            depth=self.config.depth,
        )

    async def _do_gap_analysis(self):
        review = self.session.review_result
        self.session.gap_result = await self.gap_analyzer.analyze(
            review.papers, self.config.topic, review.themes
        )

    async def _do_hypothesis_generation(self):
        review = self.session.review_result
        self.session.proposals = await self.hypothesis_gen.generate(
            self.config.topic,
            review.papers,
            self.session.gap_result,
            discipline_type=self.config.discipline_type,
        )

    async def _do_outline(self):
        proposals = self.session.proposals
        if not proposals.proposals:
            raise ValueError("No research proposals generated")

        best = proposals.proposals[proposals.recommended]
        self.session.outline = await self.outliner.create_outline(
            self.config.topic,
            best,
            self.session.review_result.papers,
            paper_type=self.config.paper_type,
            target_word_count=self.config.target_word_count,
            language=self.config.language,
        )

    async def _do_writing(self):
        self.session.draft = await self.writer.write(
            self.session.outline,
            self.session.review_result.papers,
        )

    async def _save_outputs(self):
        """Save all outputs to the output directory."""
        out_dir = Path(self.config.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        # Save literature review
        if self.session.review_result:
            review = self.session.review_result
            with open(out_dir / "literature_review.md", "w", encoding="utf-8") as f:
                f.write(f"# Literature Review: {review.topic}\n\n")
                f.write(review.review_text)
                f.write(f"\n\n## Papers Analyzed ({len(review.papers)})\n\n")
                for p in review.papers:
                    f.write(f"- {p.to_citation()}\n")

            # Save timeline
            if review.timeline:
                with open(out_dir / "timeline.json", "w", encoding="utf-8") as f:
                    json.dump(review.timeline, f, ensure_ascii=False, indent=2)

        # Save gap analysis
        if self.session.gap_result:
            gap = self.session.gap_result
            with open(out_dir / "gap_analysis.md", "w", encoding="utf-8") as f:
                f.write(f"# Gap Analysis: {gap.topic}\n\n")
                f.write(gap.summary)
                f.write("\n\n## Research Gaps\n\n")
                for g in gap.gaps:
                    f.write(f"### {g.title}\n")
                    f.write(f"- **Type:** {g.gap_type}\n")
                    f.write(f"- **Significance:** {g.significance}\n")
                    f.write(f"- **Feasibility:** {g.feasibility}\n")
                    f.write(f"- {g.description}\n\n")

        # Save proposals
        if self.session.proposals:
            props = self.session.proposals
            with open(out_dir / "proposals.md", "w", encoding="utf-8") as f:
                f.write(f"# Research Proposals: {props.topic}\n\n")
                f.write(f"**Recommended:** Proposal {props.recommended + 1}\n\n")
                f.write(f"{props.evaluation}\n\n")
                for i, p in enumerate(props.proposals):
                    marker = " (RECOMMENDED)" if i == props.recommended else ""
                    f.write(f"## Proposal {i + 1}{marker}\n\n")
                    f.write(f"**Question:** {p.question}\n\n")
                    if p.hypothesis:
                        f.write(f"**Hypothesis:** {p.hypothesis}\n\n")
                    f.write(f"**Rationale:** {p.rationale}\n\n")
                    f.write(f"**Methodology:** {p.methodology}\n\n")
                    f.write(f"**Theoretical Framework:** {p.theoretical_framework}\n\n")
                    f.write(f"**Expected Contribution:** {p.expected_contribution}\n\n")
                    f.write(f"**Feasibility:** {p.feasibility} | **Novelty:** {p.novelty}\n\n")

        # Save paper draft
        if self.session.draft:
            draft = self.session.draft
            if self.config.output_format == "latex":
                with open(out_dir / "paper.tex", "w", encoding="utf-8") as f:
                    f.write(draft.to_latex())
            else:
                with open(out_dir / "paper.md", "w", encoding="utf-8") as f:
                    f.write(draft.to_markdown())

            with open(out_dir / "references.json", "w", encoding="utf-8") as f:
                json.dump(draft.references, f, ensure_ascii=False, indent=2)

        logger.info(f"Outputs saved to {out_dir}")
