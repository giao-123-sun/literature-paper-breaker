"""Research gap analyzer.

Identifies under-explored areas, contradictions, and opportunities
in a body of literature.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field

from ..data_sources.base import Paper
from ..utils.llm import LLMClient

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """\
You are an expert research methodologist specializing in identifying research gaps
in humanities and social sciences. You have a keen eye for:
- Theoretical blind spots and under-theorized phenomena
- Methodological limitations in existing studies
- Geographic, temporal, or demographic gaps in coverage
- Contradictory findings that demand resolution
- Emerging phenomena that existing theories cannot explain
- Cross-disciplinary connections that haven't been made

You think critically and challenge assumptions. You prioritize gaps that are
both significant and feasible to address.
Respond in the same language as the research topic."""


@dataclass
class ResearchGap:
    """A specific research gap identified in the literature."""

    title: str
    description: str
    gap_type: str  # theoretical, methodological, empirical, geographic, temporal
    significance: str  # high, medium, low
    feasibility: str  # high, medium, low
    related_papers: list[int] = field(default_factory=list)
    suggested_approaches: list[str] = field(default_factory=list)


@dataclass
class GapAnalysisResult:
    """Result of a gap analysis."""

    topic: str
    gaps: list[ResearchGap] = field(default_factory=list)
    contradictions: list[dict] = field(default_factory=list)
    emerging_trends: list[dict] = field(default_factory=list)
    cross_disciplinary_opportunities: list[dict] = field(default_factory=list)
    summary: str = ""


class GapAnalyzer:
    """Analyzes literature to identify research gaps and opportunities."""

    def __init__(self, llm: LLMClient):
        self.llm = llm

    async def analyze(
        self,
        papers: list[Paper],
        topic: str,
        themes: list[dict] | None = None,
    ) -> GapAnalysisResult:
        """Perform comprehensive gap analysis on a body of literature.

        Args:
            papers: Papers from the literature review
            topic: Research topic
            themes: Previously identified themes (optional)
        """
        result = GapAnalysisResult(topic=topic)

        paper_info = self._format_papers(papers)

        # Run analyses in sequence (each builds on context)
        result.gaps = await self._find_gaps(paper_info, topic, themes)
        result.contradictions = await self._find_contradictions(paper_info, topic)
        result.emerging_trends = await self._find_trends(paper_info, topic)
        result.cross_disciplinary_opportunities = await self._find_cross_disciplinary(
            paper_info, topic
        )
        result.summary = await self._generate_summary(result)

        return result

    async def _find_gaps(
        self, paper_info: str, topic: str, themes: list[dict] | None
    ) -> list[ResearchGap]:
        themes_str = json.dumps(themes, ensure_ascii=False) if themes else "Not provided"

        prompt = f"""Topic: "{topic}"
Identified themes: {themes_str}

Literature:
{paper_info}

Identify 5-10 specific research gaps. For each gap provide:
- title: concise name
- description: what is missing and why it matters
- gap_type: one of [theoretical, methodological, empirical, geographic, temporal]
- significance: high/medium/low
- feasibility: high/medium/low (how feasible to address)
- related_papers: indices of papers that reveal this gap
- suggested_approaches: 2-3 ways to address this gap

Return as JSON array of objects."""

        response = await self.llm.generate_structured(prompt, system=SYSTEM_PROMPT)
        try:
            gaps_data = json.loads(response)
            if isinstance(gaps_data, list):
                return [
                    ResearchGap(
                        title=g.get("title", ""),
                        description=g.get("description", ""),
                        gap_type=g.get("gap_type", "theoretical"),
                        significance=g.get("significance", "medium"),
                        feasibility=g.get("feasibility", "medium"),
                        related_papers=g.get("related_papers", []),
                        suggested_approaches=g.get("suggested_approaches", []),
                    )
                    for g in gaps_data
                ]
        except json.JSONDecodeError:
            pass
        return []

    async def _find_contradictions(
        self, paper_info: str, topic: str
    ) -> list[dict]:
        prompt = f"""Topic: "{topic}"

Literature:
{paper_info}

Identify contradictory findings, conflicting theoretical claims, or
inconsistent evidence across these papers. For each contradiction:
- claim_a: one position/finding
- claim_b: the contradicting position/finding
- papers_a: paper indices supporting claim A
- papers_b: paper indices supporting claim B
- possible_resolution: how this might be resolved

Return as JSON array."""

        response = await self.llm.generate_structured(prompt, system=SYSTEM_PROMPT)
        try:
            data = json.loads(response)
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []

    async def _find_trends(self, paper_info: str, topic: str) -> list[dict]:
        prompt = f"""Topic: "{topic}"

Literature:
{paper_info}

Identify emerging trends and new directions in this field:
- trend: name of the trend
- evidence: what papers/findings suggest this trend
- potential_impact: how significant this could become
- stage: "nascent", "growing", "established"

Return as JSON array."""

        response = await self.llm.generate_structured(prompt, system=SYSTEM_PROMPT)
        try:
            data = json.loads(response)
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []

    async def _find_cross_disciplinary(
        self, paper_info: str, topic: str
    ) -> list[dict]:
        prompt = f"""Topic: "{topic}"

Literature:
{paper_info}

Identify opportunities for cross-disciplinary research:
- disciplines: which fields could be connected
- connection: what links them
- potential: what new insights could emerge
- examples: any existing work at this intersection

Return as JSON array."""

        response = await self.llm.generate_structured(prompt, system=SYSTEM_PROMPT)
        try:
            data = json.loads(response)
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []

    async def _generate_summary(self, result: GapAnalysisResult) -> str:
        gaps_str = "\n".join(
            f"- [{g.significance}] {g.title}: {g.description}" for g in result.gaps
        )
        contradictions_str = json.dumps(result.contradictions, ensure_ascii=False)[:1000]
        trends_str = json.dumps(result.emerging_trends, ensure_ascii=False)[:1000]

        prompt = f"""Summarize the gap analysis for topic: "{result.topic}"

Research Gaps:
{gaps_str}

Contradictions:
{contradictions_str}

Emerging Trends:
{trends_str}

Write a concise 300-500 word summary that:
1. Highlights the most significant gaps
2. Recommends priority areas for new research
3. Suggests the most promising research questions"""

        return await self.llm.generate(prompt, system=SYSTEM_PROMPT)

    @staticmethod
    def _format_papers(papers: list[Paper]) -> str:
        lines = []
        for i, p in enumerate(papers):
            authors = ", ".join(p.authors[:3])
            if len(p.authors) > 3:
                authors += " et al."
            line = f"[{i}] {authors} ({p.year or 'n.d.'}). \"{p.title}\""
            if p.abstract:
                line += f"\n    {p.abstract[:250]}"
            lines.append(line)
        return "\n".join(lines)
