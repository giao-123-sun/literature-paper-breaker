"""Paper outline generator.

Creates structured outlines for academic papers based on
research findings and the target journal/format.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field

from ..data_sources.base import Paper
from ..pipeline.hypothesis_generator import ResearchProposal
from ..utils.llm import LLMClient

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """\
You are an experienced academic who has published extensively in top humanities
and social science journals. You know how to structure papers for maximum impact
and clarity. You understand the conventions of different disciplines and can
adapt your approach accordingly.

Key principles:
- Every section must serve the argument
- The introduction must hook readers and clearly state the contribution
- Literature review should position the paper, not just summarize
- Methodology must be transparent and defensible
- Analysis should build toward clear conclusions
- Conclusions should address "so what?" and "what next?"

CRITICAL — Primary Data Collection Awareness:
- If the methodology involves human subjects research (surveys, interviews, \
experiments, questionnaires, user studies, ethnography, etc.), you MUST mark \
those sections clearly in the outline.
- For each section, add a key_point entry: "[REQUIRES_HUMAN_DATA_COLLECTION]" \
if the section's content depends on data that must be collected from real \
human participants.
- Structure the paper so that sections requiring uncollected primary data are \
written as PROPOSED METHODOLOGY / RESEARCH PROTOCOL, NOT as completed research.
- Sections based on computational analysis of existing texts, literature \
review, or theoretical argument can be written as completed research.
- In the section description, explicitly state whether the section should be \
written as "completed research" or "proposed research protocol".

Respond in the same language as the research topic."""


@dataclass
class Section:
    """A section in a paper outline."""

    title: str
    description: str = ""
    subsections: list[Section] = field(default_factory=list)
    estimated_words: int = 0
    key_points: list[str] = field(default_factory=list)
    citations_needed: list[str] = field(default_factory=list)


@dataclass
class PaperOutline:
    """Complete paper outline."""

    title: str
    abstract_draft: str = ""
    keywords: list[str] = field(default_factory=list)
    sections: list[Section] = field(default_factory=list)
    total_estimated_words: int = 0
    paper_type: str = "research_article"  # research_article, review, essay, commentary
    target_journal: str = ""


class PaperOutliner:
    """Generates detailed paper outlines."""

    def __init__(self, llm: LLMClient):
        self.llm = llm

    async def create_outline(
        self,
        topic: str,
        proposal: ResearchProposal,
        papers: list[Paper],
        *,
        paper_type: str = "research_article",
        target_word_count: int = 8000,
        language: str = "en",
    ) -> PaperOutline:
        """Create a detailed paper outline.

        Args:
            topic: Research topic
            proposal: The research proposal to develop
            papers: Reference papers
            paper_type: Type of paper to write
            target_word_count: Target length
            language: Writing language
        """
        paper_refs = self._format_refs(papers)

        prompt = f"""Create a detailed academic paper outline.

Research topic: "{topic}"
Research question: {proposal.question}
Hypothesis: {proposal.hypothesis or "N/A (interpretive study)"}
Methodology: {proposal.methodology}
Theoretical framework: {proposal.theoretical_framework}
Paper type: {paper_type}
Target length: ~{target_word_count} words
Language: {language}

Available references:
{paper_refs}

Generate a complete outline with:
- title: compelling academic title
- abstract_draft: 150-250 word abstract draft
- keywords: 5-8 keywords
- sections: array of sections, each with:
  - title: section title
  - description: what this section covers
  - subsections: array of subsection objects (same structure)
  - estimated_words: word count for this section
  - key_points: main arguments/points to make
  - citations_needed: which references to cite [AuthorYear]

Return as JSON."""

        response = await self.llm.generate_structured(
            prompt, system=SYSTEM_PROMPT, temperature=0.3
        )

        try:
            data = json.loads(response)
            sections = [self._parse_section(s) for s in data.get("sections", [])]

            return PaperOutline(
                title=data.get("title", topic),
                abstract_draft=data.get("abstract_draft", ""),
                keywords=data.get("keywords", []),
                sections=sections,
                total_estimated_words=sum(s.estimated_words for s in sections),
                paper_type=paper_type,
            )
        except json.JSONDecodeError:
            logger.error("Failed to parse outline JSON")
            return PaperOutline(title=topic, paper_type=paper_type)

    def _parse_section(self, data: dict) -> Section:
        subsections = [
            self._parse_section(sub) for sub in data.get("subsections", [])
        ]
        return Section(
            title=data.get("title", ""),
            description=data.get("description", ""),
            subsections=subsections,
            estimated_words=data.get("estimated_words", 500),
            key_points=data.get("key_points", []),
            citations_needed=data.get("citations_needed", []),
        )

    @staticmethod
    def _format_refs(papers: list[Paper]) -> str:
        lines = []
        for p in papers[:40]:
            first_author = p.authors[0].split()[-1] if p.authors else "Unknown"
            key = f"[{first_author}{p.year or 'nd'}]"
            lines.append(f"{key} {', '.join(p.authors[:3])}. \"{p.title}\"")
        return "\n".join(lines)
