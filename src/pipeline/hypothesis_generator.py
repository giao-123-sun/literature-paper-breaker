"""Research hypothesis and question generator.

Takes literature review results and gap analysis to propose
novel research questions and hypotheses.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field

from ..data_sources.base import Paper
from ..utils.llm import LLMClient
from .gap_analyzer import GapAnalysisResult

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """\
You are a brilliant humanities and social science researcher known for asking
penetrating questions that open new avenues of inquiry. You combine theoretical
sophistication with empirical rigor. You understand that the best research
questions in humanities are not just about what happened, but WHY, HOW, and
WHAT IT MEANS.

You excel at:
- Formulating falsifiable hypotheses for social science
- Crafting interpretive research questions for humanities
- Identifying causal mechanisms and mediating variables
- Proposing innovative methodological approaches
- Connecting micro-level phenomena to macro-level theories

Always ground your proposals in existing literature.
Respond in the same language as the research topic."""


@dataclass
class ResearchProposal:
    """A proposed research question or hypothesis with methodology."""

    question: str
    hypothesis: str = ""  # For social science; empty for pure humanities
    rationale: str = ""
    methodology: str = ""
    data_sources: list[str] = field(default_factory=list)
    theoretical_framework: str = ""
    expected_contribution: str = ""
    feasibility: str = "medium"  # high, medium, low
    novelty: str = "medium"  # high, medium, low
    related_gaps: list[str] = field(default_factory=list)


@dataclass
class ProposalSet:
    """A set of research proposals generated for a topic."""

    topic: str
    proposals: list[ResearchProposal] = field(default_factory=list)
    recommended: int = 0  # index of most recommended proposal
    evaluation: str = ""


class HypothesisGenerator:
    """Generates research hypotheses and questions from literature analysis."""

    def __init__(self, llm: LLMClient):
        self.llm = llm

    async def generate(
        self,
        topic: str,
        papers: list[Paper],
        gap_analysis: GapAnalysisResult | None = None,
        *,
        num_proposals: int = 5,
        discipline_type: str = "social_science",  # "humanities" or "social_science"
    ) -> ProposalSet:
        """Generate research proposals based on literature and gap analysis.

        Args:
            topic: Research topic
            papers: Papers from literature review
            gap_analysis: Results from gap analysis
            num_proposals: Number of proposals to generate
            discipline_type: "humanities" for interpretive questions,
                           "social_science" for testable hypotheses
        """
        paper_info = self._format_papers(papers)
        gaps_info = self._format_gaps(gap_analysis) if gap_analysis else "Not available"

        proposals = await self._generate_proposals(
            topic, paper_info, gaps_info, num_proposals, discipline_type
        )

        result = ProposalSet(topic=topic, proposals=proposals)

        # Evaluate and rank proposals
        if proposals:
            result.recommended, result.evaluation = await self._evaluate_proposals(
                topic, proposals
            )

        return result

    async def _generate_proposals(
        self,
        topic: str,
        paper_info: str,
        gaps_info: str,
        num: int,
        discipline_type: str,
    ) -> list[ResearchProposal]:
        if discipline_type == "humanities":
            question_guidance = """For each proposal, formulate an interpretive research question
that explores meaning, significance, or cultural/historical understanding.
These need not be falsifiable but should be answerable through rigorous analysis."""
        else:
            question_guidance = """For each proposal, formulate both a research question AND
a testable hypothesis with clear variables. Ensure hypotheses are falsifiable
and specify the expected relationship between variables."""

        prompt = f"""Research topic: "{topic}"

Literature reviewed:
{paper_info}

Research gaps identified:
{gaps_info}

Generate {num} original research proposals. {question_guidance}

For each proposal provide:
- question: the central research question
- hypothesis: testable hypothesis (empty string for purely interpretive work)
- rationale: why this question matters and how it builds on existing work
- methodology: specific methods to address this question
- data_sources: what data/sources would be needed
- theoretical_framework: which theories guide this inquiry
- expected_contribution: what this would add to the field
- feasibility: high/medium/low
- novelty: high/medium/low
- related_gaps: which identified gaps this addresses

Return as JSON array of objects."""

        response = await self.llm.generate_structured(
            prompt, system=SYSTEM_PROMPT, temperature=0.5
        )

        try:
            data = json.loads(response)
            if isinstance(data, list):
                return [
                    ResearchProposal(
                        question=p.get("question", ""),
                        hypothesis=p.get("hypothesis", ""),
                        rationale=p.get("rationale", ""),
                        methodology=p.get("methodology", ""),
                        data_sources=p.get("data_sources", []),
                        theoretical_framework=p.get("theoretical_framework", ""),
                        expected_contribution=p.get("expected_contribution", ""),
                        feasibility=p.get("feasibility", "medium"),
                        novelty=p.get("novelty", "medium"),
                        related_gaps=p.get("related_gaps", []),
                    )
                    for p in data
                ]
        except json.JSONDecodeError:
            pass
        return []

    async def _evaluate_proposals(
        self, topic: str, proposals: list[ResearchProposal]
    ) -> tuple[int, str]:
        proposals_text = "\n\n".join(
            f"Proposal {i}:\n"
            f"  Question: {p.question}\n"
            f"  Hypothesis: {p.hypothesis}\n"
            f"  Methodology: {p.methodology}\n"
            f"  Novelty: {p.novelty}, Feasibility: {p.feasibility}"
            for i, p in enumerate(proposals)
        )

        prompt = f"""Evaluate these research proposals for topic: "{topic}"

{proposals_text}

Assess each proposal on:
1. Originality and novelty
2. Theoretical significance
3. Methodological rigor
4. Feasibility
5. Potential impact

Then recommend the BEST proposal (by index) and explain why.

Return JSON: {{"recommended": 0, "evaluation": "detailed evaluation text..."}}"""

        response = await self.llm.generate_structured(prompt, system=SYSTEM_PROMPT)
        try:
            data = json.loads(response)
            return (
                int(data.get("recommended", 0)),
                data.get("evaluation", ""),
            )
        except (json.JSONDecodeError, ValueError):
            return 0, ""

    @staticmethod
    def _format_papers(papers: list[Paper]) -> str:
        lines = []
        for i, p in enumerate(papers[:30]):
            authors = ", ".join(p.authors[:2])
            line = f"[{i}] {authors} ({p.year}). \"{p.title}\""
            if p.abstract:
                line += f" - {p.abstract[:150]}"
            lines.append(line)
        return "\n".join(lines)

    @staticmethod
    def _format_gaps(gap_analysis: GapAnalysisResult) -> str:
        lines = []
        for g in gap_analysis.gaps:
            lines.append(f"- [{g.gap_type}/{g.significance}] {g.title}: {g.description}")
        if gap_analysis.contradictions:
            lines.append("\nContradictions found:")
            for c in gap_analysis.contradictions[:5]:
                lines.append(f"- {c.get('claim_a', '')} vs {c.get('claim_b', '')}")
        return "\n".join(lines)
