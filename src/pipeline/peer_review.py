"""Simulated peer review system.

Finds real scholars in the paper's field via academic APIs,
then creates reviewer agents that role-play as those scholars
to provide expert critique. Includes both subjective expert
feedback and objective journal-standard metrics.

Design: find scholars → build personas → parallel review → synthesize → revise
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from typing import Any

import httpx

from ..data_sources.base import Discipline, Paper
from ..utils.llm import LLMClient

logger = logging.getLogger(__name__)

# Standard review criteria used by major humanities/social science journals
# (adapted from SSCI journals, AHCI journals, and top conferences)
REVIEW_CRITERIA = [
    {
        "name": "Originality",
        "weight": 0.20,
        "description": "Does the paper make a novel contribution? Are the research questions original?",
        "scale": "1-10 (1=no novelty, 10=groundbreaking)",
    },
    {
        "name": "Theoretical Framework",
        "weight": 0.15,
        "description": "Is the theoretical grounding appropriate and well-articulated?",
        "scale": "1-10",
    },
    {
        "name": "Methodology",
        "weight": 0.15,
        "description": "Is the methodology sound and appropriate for the research questions?",
        "scale": "1-10",
    },
    {
        "name": "Literature Engagement",
        "weight": 0.15,
        "description": "Does the paper adequately engage with existing scholarship?",
        "scale": "1-10",
    },
    {
        "name": "Argumentation & Evidence",
        "weight": 0.15,
        "description": "Are arguments logically structured and well-supported by evidence?",
        "scale": "1-10",
    },
    {
        "name": "Clarity & Writing",
        "weight": 0.10,
        "description": "Is the paper well-written, clearly organized, and accessible?",
        "scale": "1-10",
    },
    {
        "name": "Significance",
        "weight": 0.10,
        "description": "What is the potential impact on the field? Does it advance understanding?",
        "scale": "1-10",
    },
]


@dataclass
class ScholarProfile:
    """A real scholar found via academic APIs."""

    name: str
    affiliation: str
    h_index: int
    citation_count: int
    paper_count: int
    top_papers: list[str]  # titles of most-cited papers
    research_interests: list[str]
    source_id: str  # API identifier for lookups


@dataclass
class ReviewScore:
    """Score on a single review criterion."""

    criterion: str
    score: int  # 1-10
    comment: str


@dataclass
class PeerReviewResult:
    """A single reviewer's evaluation."""

    reviewer: ScholarProfile
    scores: list[ReviewScore]
    overall_score: float  # weighted average
    decision: str  # accept, minor_revision, major_revision, reject
    strengths: list[str]
    weaknesses: list[str]
    detailed_comments: str
    suggestions: list[str]


@dataclass
class ReviewSynthesis:
    """Editor's synthesis of all reviews."""

    reviews: list[PeerReviewResult]
    average_score: float
    consensus_decision: str
    key_strengths: list[str]
    critical_issues: list[str]
    revision_instructions: str  # actionable feedback for revision
    meta_review: str  # editor's narrative summary


class PeerReviewer:
    """Simulates academic peer review using real scholar personas.

    Pipeline:
    1. Search OpenAlex/Semantic Scholar for leading scholars in the field
    2. Build reviewer personas from their real profiles
    3. Each reviewer evaluates the paper from their expert perspective
    4. An editor synthesizes reviews into actionable revision guidance
    """

    def __init__(self, llm: LLMClient):
        self.llm = llm
        self._http = httpx.AsyncClient(timeout=30.0)

    async def review_and_revise(
        self,
        draft_text: str,
        topic: str,
        discipline: Discipline,
        papers: list[Paper],
        *,
        num_reviewers: int = 3,
        max_rounds: int = 1,
    ) -> tuple[ReviewSynthesis, str]:
        """Full review cycle: find reviewers → review → synthesize → revise.

        Returns (synthesis, revised_text).
        """
        # Find real scholars to serve as reviewer personas
        scholars = await self.find_scholars(topic, discipline, count=num_reviewers)

        revised = draft_text
        synthesis = None

        for round_num in range(max_rounds):
            logger.info(f"Review round {round_num + 1}/{max_rounds}")

            # Each scholar reviews the paper
            reviews = []
            for scholar in scholars:
                review = await self._single_review(revised, topic, scholar, papers)
                reviews.append(review)

            # Editor synthesizes all reviews
            synthesis = await self._synthesize_reviews(reviews, topic)

            # If accepted or only minor issues, stop
            if synthesis.consensus_decision == "accept":
                logger.info("Paper accepted — no revision needed")
                break

            # Revise based on feedback
            revised = await self._revise_draft(revised, synthesis, papers)
            logger.info(
                f"Round {round_num + 1} complete — score: {synthesis.average_score:.1f}/10, "
                f"decision: {synthesis.consensus_decision}"
            )

        return synthesis, revised

    async def find_scholars(
        self,
        topic: str,
        discipline: Discipline,
        *,
        count: int = 3,
    ) -> list[ScholarProfile]:
        """Find real scholars in the field using OpenAlex authors API.

        Strategy: search for top-cited papers on the topic, then extract
        their most prolific/cited authors as reviewer candidates.
        """
        scholars = []

        # Try OpenAlex first (largest free index)
        try:
            scholars = await self._find_via_openalex(topic, discipline, count * 2)
        except Exception as e:
            logger.warning(f"OpenAlex author search failed: {e}")

        # Supplement with Semantic Scholar if needed
        if len(scholars) < count:
            try:
                extra = await self._find_via_semantic_scholar(
                    topic, count * 2 - len(scholars)
                )
                scholars.extend(extra)
            except Exception as e:
                logger.warning(f"Semantic Scholar author search failed: {e}")

        # Deduplicate by name (rough)
        seen = set()
        unique = []
        for s in scholars:
            key = s.name.lower().strip()
            if key not in seen:
                seen.add(key)
                unique.append(s)

        # Sort by h-index (most authoritative first) and take top N
        unique.sort(key=lambda s: s.h_index, reverse=True)
        selected = unique[:count]

        # If we couldn't find real scholars, create synthetic profiles
        if len(selected) < count:
            synthetic = await self._generate_synthetic_reviewers(
                topic, discipline, count - len(selected)
            )
            selected.extend(synthetic)

        logger.info(
            f"Selected {len(selected)} reviewers: "
            + ", ".join(f"{s.name} (h={s.h_index})" for s in selected)
        )
        return selected

    async def _find_via_openalex(
        self, topic: str, discipline: Discipline, count: int
    ) -> list[ScholarProfile]:
        """Find scholars via OpenAlex works → authors pipeline."""
        # Search for highly-cited papers on the topic
        params: dict[str, Any] = {
            "search": topic,
            "per_page": 20,
            "sort": "cited_by_count:desc",
        }

        resp = await self._http.get("https://api.openalex.org/works", params=params)
        resp.raise_for_status()
        works = resp.json().get("results", [])

        # Extract unique author IDs from top papers
        author_ids: dict[str, list[str]] = {}  # id → [paper_titles]
        for work in works:
            title = work.get("display_name", "")
            for authorship in work.get("authorships", []):
                author = authorship.get("author", {})
                aid = author.get("id", "")
                if aid:
                    author_ids.setdefault(aid, []).append(title)

        # Fetch author details for the most-appearing authors
        sorted_authors = sorted(author_ids.items(), key=lambda x: len(x[1]), reverse=True)
        scholars = []
        for aid, paper_titles in sorted_authors[:count]:
            try:
                resp = await self._http.get(f"https://api.openalex.org/authors/{aid.split('/')[-1]}")
                if resp.status_code != 200:
                    continue
                data = resp.json()

                # Extract research interests from top concepts
                interests = [
                    c.get("display_name", "")
                    for c in (data.get("x_concepts", []) or [])[:5]
                    if c.get("display_name")
                ]

                scholars.append(ScholarProfile(
                    name=data.get("display_name", "Unknown"),
                    affiliation=_extract_affiliation(data),
                    h_index=data.get("summary_stats", {}).get("h_index", 0),
                    citation_count=data.get("cited_by_count", 0),
                    paper_count=data.get("works_count", 0),
                    top_papers=paper_titles[:3],
                    research_interests=interests,
                    source_id=aid,
                ))
            except Exception:
                continue

        return scholars

    async def _find_via_semantic_scholar(
        self, topic: str, count: int
    ) -> list[ScholarProfile]:
        """Find scholars via Semantic Scholar paper search → authors."""
        resp = await self._http.get(
            "https://api.semanticscholar.org/graph/v1/paper/search",
            params={
                "query": topic,
                "limit": 10,
                "fields": "title,authors,citationCount",
            },
        )
        resp.raise_for_status()
        papers = resp.json().get("data", [])

        # Collect author IDs
        author_ids: dict[str, list[str]] = {}
        for paper in papers:
            title = paper.get("title", "")
            for author in paper.get("authors", []):
                aid = author.get("authorId", "")
                if aid:
                    author_ids.setdefault(aid, []).append(title)

        scholars = []
        sorted_authors = sorted(author_ids.items(), key=lambda x: len(x[1]), reverse=True)
        for aid, paper_titles in sorted_authors[:count]:
            try:
                resp = await self._http.get(
                    f"https://api.semanticscholar.org/graph/v1/author/{aid}",
                    params={"fields": "name,affiliations,hIndex,citationCount,paperCount"},
                )
                if resp.status_code != 200:
                    continue
                data = resp.json()

                scholars.append(ScholarProfile(
                    name=data.get("name", "Unknown"),
                    affiliation=(data.get("affiliations", []) or [""])[0],
                    h_index=data.get("hIndex", 0) or 0,
                    citation_count=data.get("citationCount", 0) or 0,
                    paper_count=data.get("paperCount", 0) or 0,
                    top_papers=paper_titles[:3],
                    research_interests=[],
                    source_id=f"s2:{aid}",
                ))
            except Exception:
                continue

        return scholars

    async def _generate_synthetic_reviewers(
        self, topic: str, discipline: Discipline, count: int
    ) -> list[ScholarProfile]:
        """Fallback: ask LLM to suggest plausible real scholar profiles."""
        prompt = f"""For the research topic "{topic}" in {discipline.value}, suggest {count} real,
well-known scholars who would be appropriate peer reviewers. For each scholar, provide:
- name (a real, well-known scholar in this field)
- affiliation
- research_interests (list of 3-5 areas)
- notable_works (2-3 titles of their real, well-known publications)

Respond in JSON: [{{"name": "...", "affiliation": "...", "research_interests": [...], "notable_works": [...]}}]"""

        text = await self.llm.generate_structured(prompt)
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            data = []

        return [
            ScholarProfile(
                name=d.get("name", f"Reviewer {i+1}"),
                affiliation=d.get("affiliation", ""),
                h_index=0,
                citation_count=0,
                paper_count=0,
                top_papers=d.get("notable_works", []),
                research_interests=d.get("research_interests", []),
                source_id="synthetic",
            )
            for i, d in enumerate(data[:count])
        ]

    async def _single_review(
        self,
        draft_text: str,
        topic: str,
        scholar: ScholarProfile,
        papers: list[Paper],
    ) -> PeerReviewResult:
        """One scholar reviews the paper."""
        criteria_text = "\n".join(
            f"- **{c['name']}** ({c['weight']*100:.0f}%): {c['description']} Scale: {c['scale']}"
            for c in REVIEW_CRITERIA
        )

        system = f"""You are Professor {scholar.name}, {scholar.affiliation}.
Your research focuses on: {', '.join(scholar.research_interests) or topic}.
Notable publications: {'; '.join(scholar.top_papers[:3]) or 'various works in this field'}.
H-index: {scholar.h_index}, Total citations: {scholar.citation_count}.

You have been invited to review a manuscript for a top-tier journal in this field.
Review from YOUR scholarly perspective — your specific expertise, theoretical commitments,
and methodological preferences should shape your evaluation.

Be rigorous but constructive. Identify both strengths and genuine weaknesses.
Do not be sycophantic — a good review helps authors improve their work."""

        prompt = f"""Review this manuscript on "{topic}".

EVALUATION CRITERIA (score each 1-10):
{criteria_text}

MANUSCRIPT:
{draft_text[:12000]}

Provide your review as JSON:
{{
  "scores": [{{"criterion": "Originality", "score": N, "comment": "..."}}, ...],
  "strengths": ["...", "..."],
  "weaknesses": ["...", "..."],
  "detailed_comments": "Your detailed narrative review (2-3 paragraphs)",
  "suggestions": ["specific actionable suggestion 1", "..."],
  "decision": "accept|minor_revision|major_revision|reject"
}}"""

        text = await self.llm.generate_structured(prompt, system=system)
        return self._parse_review(text, scholar)

    def _parse_review(self, text: str, scholar: ScholarProfile) -> PeerReviewResult:
        """Parse LLM review output into structured result."""
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            # Fallback: extract what we can
            data = {
                "scores": [],
                "strengths": ["Unable to parse structured review"],
                "weaknesses": ["Review parsing failed"],
                "detailed_comments": text[:2000],
                "suggestions": [],
                "decision": "major_revision",
            }

        scores = [
            ReviewScore(
                criterion=s.get("criterion", ""),
                score=max(1, min(10, int(s.get("score", 5)))),
                comment=s.get("comment", ""),
            )
            for s in data.get("scores", [])
        ]

        # Calculate weighted average
        criteria_weights = {c["name"]: c["weight"] for c in REVIEW_CRITERIA}
        weighted_sum = 0.0
        total_weight = 0.0
        for s in scores:
            w = criteria_weights.get(s.criterion, 0.1)
            weighted_sum += s.score * w
            total_weight += w
        overall = weighted_sum / total_weight if total_weight > 0 else 5.0

        return PeerReviewResult(
            reviewer=scholar,
            scores=scores,
            overall_score=overall,
            decision=data.get("decision", "major_revision"),
            strengths=data.get("strengths", []),
            weaknesses=data.get("weaknesses", []),
            detailed_comments=data.get("detailed_comments", ""),
            suggestions=data.get("suggestions", []),
        )

    async def _synthesize_reviews(
        self, reviews: list[PeerReviewResult], topic: str
    ) -> ReviewSynthesis:
        """Editor synthesizes all reviews into a coherent assessment."""
        avg_score = sum(r.overall_score for r in reviews) / len(reviews) if reviews else 0

        # Determine consensus decision by majority
        decisions = [r.decision for r in reviews]
        decision_priority = {"reject": 0, "major_revision": 1, "minor_revision": 2, "accept": 3}
        sorted_decisions = sorted(decisions, key=lambda d: decision_priority.get(d, 1))
        consensus = sorted_decisions[len(sorted_decisions) // 2]  # median

        # Build review summary for editor
        review_summaries = []
        for i, r in enumerate(reviews, 1):
            summary = (
                f"Reviewer {i} ({r.reviewer.name}, {r.reviewer.affiliation}):\n"
                f"  Score: {r.overall_score:.1f}/10 | Decision: {r.decision}\n"
                f"  Strengths: {'; '.join(r.strengths[:3])}\n"
                f"  Weaknesses: {'; '.join(r.weaknesses[:3])}\n"
                f"  Key suggestions: {'; '.join(r.suggestions[:3])}\n"
            )
            review_summaries.append(summary)

        editor_prompt = f"""As the editor-in-chief, synthesize these peer reviews for a manuscript on "{topic}".

REVIEWS:
{''.join(review_summaries)}

Average score: {avg_score:.1f}/10
Consensus decision: {consensus}

Write:
1. A meta-review (2-3 paragraphs) summarizing the reviewers' assessments
2. Key strengths agreed upon by reviewers
3. Critical issues that MUST be addressed
4. Concrete, prioritized revision instructions for the authors

Respond in JSON:
{{
  "meta_review": "...",
  "key_strengths": ["...", "..."],
  "critical_issues": ["...", "..."],
  "revision_instructions": "Detailed, actionable revision guidance..."
}}"""

        text = await self.llm.generate_structured(
            editor_prompt,
            system="You are the editor-in-chief of a leading academic journal. "
            "Synthesize reviewer feedback into clear, actionable guidance.",
        )

        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            data = {
                "meta_review": text[:2000],
                "key_strengths": [],
                "critical_issues": [],
                "revision_instructions": "Please address reviewer comments.",
            }

        return ReviewSynthesis(
            reviews=reviews,
            average_score=avg_score,
            consensus_decision=consensus,
            key_strengths=data.get("key_strengths", []),
            critical_issues=data.get("critical_issues", []),
            revision_instructions=data.get("revision_instructions", ""),
            meta_review=data.get("meta_review", ""),
        )

    async def _revise_draft(
        self,
        draft_text: str,
        synthesis: ReviewSynthesis,
        papers: list[Paper],
    ) -> str:
        """Revise the draft based on review synthesis."""
        refs = "\n".join(
            f"- {p.to_citation()}" for p in papers[:30]
        )

        prompt = f"""Revise this academic manuscript based on peer review feedback.

REVISION INSTRUCTIONS FROM EDITOR:
{synthesis.revision_instructions}

CRITICAL ISSUES TO ADDRESS:
{chr(10).join(f'- {issue}' for issue in synthesis.critical_issues)}

REVIEWER COMMENTS:
{chr(10).join(r.detailed_comments[:500] for r in synthesis.reviews)}

AVAILABLE REFERENCES:
{refs}

CURRENT MANUSCRIPT:
{draft_text[:15000]}

Revise the manuscript addressing ALL issues raised. Maintain the overall structure
but strengthen weak areas. Only cite papers from the provided references.
Output the complete revised manuscript."""

        return await self.llm.generate(
            prompt,
            system="You are a world-class academic writer revising a manuscript based on "
            "peer review feedback. Address every substantive criticism while maintaining "
            "the paper's original contribution and voice.",
            max_tokens=16384,
        )

    async def close(self):
        await self._http.aclose()


def _extract_affiliation(author_data: dict) -> str:
    """Extract affiliation from OpenAlex author data."""
    affiliations = author_data.get("affiliations", [])
    if affiliations:
        inst = affiliations[0].get("institution", {})
        return inst.get("display_name", "")
    last_known = author_data.get("last_known_institution", {})
    if last_known:
        return last_known.get("display_name", "")
    return ""
