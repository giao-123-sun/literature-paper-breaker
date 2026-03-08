"""Automated literature review pipeline.

This module handles:
1. Systematic literature search across multiple databases
2. Paper relevance scoring and filtering
3. Thematic clustering and research trajectory mapping
4. Automated literature review generation
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field

from ..data_sources.aggregator import AggregatedSource
from ..data_sources.base import Discipline, Paper
from ..utils.llm import LLMClient

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """\
You are a senior research scholar specializing in humanities and social sciences.
You have deep expertise in systematic literature reviews, research methodology,
and academic writing. You analyze papers with the rigor of a top-tier journal reviewer.

When analyzing literature, you:
- Identify key theoretical frameworks and their evolution
- Map debates, agreements, and disagreements between scholars
- Note methodological approaches and their strengths/limitations
- Identify gaps, contradictions, and under-explored areas
- Maintain academic objectivity while noting your analytical observations

Always cite papers using [AuthorYear] format.
Respond in the same language as the user's research topic."""


@dataclass
class ReviewResult:
    """Result of an automated literature review."""

    topic: str
    papers: list[Paper]
    review_text: str = ""
    themes: list[dict] = field(default_factory=list)
    timeline: list[dict] = field(default_factory=list)
    key_debates: list[dict] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    methodology_summary: str = ""


class LiteratureReviewer:
    """Conducts automated systematic literature reviews."""

    def __init__(self, sources: AggregatedSource, llm: LLMClient):
        self.sources = sources
        self.llm = llm

    async def review(
        self,
        topic: str,
        *,
        discipline: Discipline | None = None,
        year_from: int | None = None,
        year_to: int | None = None,
        max_papers: int = 50,
        language: str | None = None,
        depth: str = "standard",  # "quick", "standard", "deep"
    ) -> ReviewResult:
        """Conduct a systematic literature review on a topic.

        Args:
            topic: Research topic or question
            discipline: Academic discipline to focus on
            year_from: Start year for search
            year_to: End year for search
            max_papers: Maximum number of papers to analyze
            language: Preferred language
            depth: Review depth - quick (10 papers), standard (30), deep (50+)
        """
        # Step 1: Generate search queries
        queries = await self._generate_search_queries(topic, discipline)

        # Step 2: Search across all sources
        all_papers: list[Paper] = []
        for query in queries:
            result = await self.sources.search(
                query,
                discipline=discipline,
                year_from=year_from,
                year_to=year_to,
                limit=max_papers // len(queries) + 1,
                language=language,
            )
            all_papers.extend(result.papers)

        # Deduplicate
        papers = self._deduplicate_papers(all_papers)
        logger.info(f"Found {len(papers)} unique papers for topic: {topic}")

        # Step 3: Score and rank papers by relevance
        if len(papers) > max_papers:
            papers = await self._rank_papers(papers, topic, max_papers)

        # Step 4: Analyze papers and generate review
        result = ReviewResult(topic=topic, papers=papers)

        # Step 5: Identify themes
        result.themes = await self._identify_themes(papers, topic)

        # Step 6: Map research timeline
        result.timeline = self._build_timeline(papers)

        # Step 7: Identify key debates
        result.key_debates = await self._identify_debates(papers, topic)

        # Step 8: Generate the review text
        result.review_text = await self._generate_review(
            papers, topic, result.themes, result.key_debates, depth
        )

        # Step 9: Identify gaps
        result.gaps = await self._identify_gaps(papers, topic, result.themes)

        return result

    async def _generate_search_queries(
        self, topic: str, discipline: Discipline | None
    ) -> list[str]:
        """Use LLM to generate effective search queries for the topic."""
        disc_str = f" in the field of {discipline.value}" if discipline else ""
        prompt = f"""Given the research topic: "{topic}"{disc_str}

Generate 5 diverse academic search queries that would find relevant papers.
Include:
1. The main topic query
2. A broader theoretical framework query
3. A methodology-focused query
4. A query for seminal/foundational works
5. A query for recent developments or debates

Return as JSON array of strings. Example: ["query1", "query2", ...]"""

        response = await self.llm.generate_structured(prompt, system=SYSTEM_PROMPT)
        try:
            queries = json.loads(response)
            if isinstance(queries, list):
                return [str(q) for q in queries[:5]]
        except json.JSONDecodeError:
            pass
        return [topic]

    async def _rank_papers(
        self, papers: list[Paper], topic: str, limit: int
    ) -> list[Paper]:
        """Rank papers by relevance to the topic."""
        # Build paper summaries for LLM ranking
        paper_summaries = []
        for i, p in enumerate(papers[:100]):  # limit to avoid token overflow
            summary = f"[{i}] {p.title} ({p.year or 'n.d.'}) - Citations: {p.citations_count}"
            if p.abstract:
                summary += f"\n  Abstract: {p.abstract[:200]}"
            paper_summaries.append(summary)

        prompt = f"""Research topic: "{topic}"

Below are papers found. Select the {limit} most relevant paper indices.
Consider: topic relevance, citation impact, recency, and theoretical contribution.

Papers:
{chr(10).join(paper_summaries)}

Return JSON array of selected indices. Example: [0, 3, 7, ...]"""

        response = await self.llm.generate_structured(prompt, system=SYSTEM_PROMPT)
        try:
            indices = json.loads(response)
            if isinstance(indices, list):
                selected = []
                for idx in indices:
                    if isinstance(idx, int) and 0 <= idx < len(papers):
                        selected.append(papers[idx])
                if selected:
                    return selected[:limit]
        except json.JSONDecodeError:
            pass

        # Fallback: sort by citations
        papers.sort(key=lambda p: p.citations_count, reverse=True)
        return papers[:limit]

    async def _identify_themes(
        self, papers: list[Paper], topic: str
    ) -> list[dict]:
        """Identify major themes in the literature."""
        paper_info = self._format_papers_for_llm(papers)

        prompt = f"""Research topic: "{topic}"

Analyze these papers and identify the major themes/schools of thought:

{paper_info}

For each theme, provide:
- name: theme name
- description: brief description
- papers: list of paper indices [0, 1, ...]
- key_concepts: list of key concepts

Return as JSON array. Example:
[{{"name": "Theme 1", "description": "...", "papers": [0, 2, 5], "key_concepts": ["concept1"]}}]"""

        response = await self.llm.generate_structured(prompt, system=SYSTEM_PROMPT)
        try:
            themes = json.loads(response)
            if isinstance(themes, list):
                return themes
        except json.JSONDecodeError:
            pass
        return []

    async def _identify_debates(
        self, papers: list[Paper], topic: str
    ) -> list[dict]:
        """Identify key scholarly debates in the literature."""
        paper_info = self._format_papers_for_llm(papers)

        prompt = f"""Research topic: "{topic}"

Analyze these papers and identify the key scholarly debates/controversies:

{paper_info}

For each debate, provide:
- topic: debate topic
- positions: list of different scholarly positions
- key_scholars: notable scholars on each side
- status: "ongoing", "resolved", or "emerging"

Return as JSON array."""

        response = await self.llm.generate_structured(prompt, system=SYSTEM_PROMPT)
        try:
            debates = json.loads(response)
            if isinstance(debates, list):
                return debates
        except json.JSONDecodeError:
            pass
        return []

    async def _generate_review(
        self,
        papers: list[Paper],
        topic: str,
        themes: list[dict],
        debates: list[dict],
        depth: str,
    ) -> str:
        """Generate the full literature review text."""
        paper_info = self._format_papers_for_llm(papers)
        themes_info = json.dumps(themes, ensure_ascii=False, indent=2) if themes else "None identified"
        debates_info = json.dumps(debates, ensure_ascii=False, indent=2) if debates else "None identified"

        length_guide = {
            "quick": "Write a concise review of 800-1200 words.",
            "standard": "Write a comprehensive review of 2000-3000 words.",
            "deep": "Write a thorough, publication-ready review of 4000-6000 words.",
        }

        prompt = f"""Write a systematic literature review on: "{topic}"

{length_guide.get(depth, length_guide["standard"])}

Papers analyzed:
{paper_info}

Identified themes:
{themes_info}

Key debates:
{debates_info}

Structure your review with:
1. Introduction - scope and significance
2. Thematic analysis - organized by themes, not chronologically
3. Methodological considerations
4. Key debates and unresolved questions
5. Research gaps and future directions

Use academic tone. Cite papers as [AuthorYear]. Do NOT fabricate citations."""

        return await self.llm.generate(
            prompt,
            system=SYSTEM_PROMPT,
            max_tokens=16384 if depth == "deep" else 8192,
        )

    async def _identify_gaps(
        self, papers: list[Paper], topic: str, themes: list[dict]
    ) -> list[str]:
        """Identify research gaps from the literature."""
        paper_info = self._format_papers_for_llm(papers[:30])

        prompt = f"""Research topic: "{topic}"

Based on this literature review:
{paper_info}

Identify specific research gaps - areas that are under-explored, contradictory
findings that need resolution, methodological limitations, or emerging questions.

Return as JSON array of strings, each describing one gap."""

        response = await self.llm.generate_structured(prompt, system=SYSTEM_PROMPT)
        try:
            gaps = json.loads(response)
            if isinstance(gaps, list):
                return [str(g) for g in gaps]
        except json.JSONDecodeError:
            pass
        return []

    def _build_timeline(self, papers: list[Paper]) -> list[dict]:
        """Build a chronological timeline of research development."""
        year_groups: dict[int, list[Paper]] = {}
        for p in papers:
            if p.year:
                year_groups.setdefault(p.year, []).append(p)

        timeline = []
        for year in sorted(year_groups.keys()):
            group = year_groups[year]
            timeline.append({
                "year": year,
                "count": len(group),
                "key_papers": [
                    {"title": p.title, "authors": p.authors[:3], "citations": p.citations_count}
                    for p in sorted(group, key=lambda x: x.citations_count, reverse=True)[:3]
                ],
            })
        return timeline

    @staticmethod
    def _format_papers_for_llm(papers: list[Paper]) -> str:
        """Format papers into a compact string for LLM context."""
        lines = []
        for i, p in enumerate(papers):
            authors = ", ".join(p.authors[:3])
            if len(p.authors) > 3:
                authors += " et al."
            line = f"[{i}] {authors} ({p.year or 'n.d.'}). \"{p.title}\""
            if p.journal:
                line += f". {p.journal}"
            line += f". [Citations: {p.citations_count}]"
            if p.abstract:
                line += f"\n    Abstract: {p.abstract[:300]}"
            lines.append(line)
        return "\n".join(lines)

    @staticmethod
    def _deduplicate_papers(papers: list[Paper]) -> list[Paper]:
        seen: set[str] = set()
        unique: list[Paper] = []
        for p in papers:
            key = p.doi or p.title.lower().strip()
            if key not in seen:
                seen.add(key)
                unique.append(p)
        return unique
