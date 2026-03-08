#!/usr/bin/env python3
"""Dry-run simulation: validates the complete pipeline logic with mock LLM and mock APIs.

This exercises every component without real API calls:
- Literature search (mocked academic papers)
- Literature review analysis
- Gap analysis
- Hypothesis/proposal generation
- Paper outlining
- Paper writing (section by section)
- Peer review (scholar discovery + review + synthesis + revision)

Run: python scripts/dry_run.py
"""

import asyncio
import json
import logging
import os
import sys
import time
from dataclasses import dataclass
from unittest.mock import AsyncMock, MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_sources.base import Discipline, Paper, SearchResult
from src.pipeline.orchestrator import ResearchConfig, ResearchOrchestrator
from src.pipeline.peer_review import PeerReviewer, ScholarProfile
from src.paper_engine.writer import PaperDraft
from src.utils.llm import LLMClient, LLMConfig

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("dry_run")

# --- Mock data ---

MOCK_PAPERS = [
    Paper(
        title="Digital Transformation and Collective Memory in Online Spaces",
        authors=["Sarah Chen", "Michael Torres"],
        abstract="This study examines how digital platforms reshape collective memory through algorithmic curation of historical narratives. Using a mixed-methods approach combining computational text analysis with in-depth interviews, we find that platform algorithms systematically privilege certain historical interpretations over others.",
        year=2024,
        doi="10.1234/mock001",
        journal="Digital Culture & Society",
        citations_count=45,
        keywords=["digital transformation", "collective memory", "algorithms"],
        source="openalex",
    ),
    Paper(
        title="AI-Generated Text and the Public Sphere: A Habermasian Analysis",
        authors=["James Wright", "Anna Kovacs"],
        abstract="Drawing on Habermas's theory of communicative action, this paper analyzes the implications of AI-generated text for democratic deliberation. We argue that the proliferation of synthetic text fundamentally alters the conditions of rational discourse.",
        year=2025,
        doi="10.1234/mock002",
        journal="Philosophy & Technology",
        citations_count=28,
        keywords=["AI", "public sphere", "Habermas", "deliberation"],
        source="semantic_scholar",
    ),
    Paper(
        title="Algorithmic Gatekeeping and Historical Narratives on Social Media",
        authors=["Liu Wei", "Priya Patel", "Thomas Anderson"],
        abstract="This paper investigates how recommendation algorithms on social media platforms act as gatekeepers of historical knowledge. Through a large-scale analysis of 2.3 million posts about historical events, we demonstrate significant biases in algorithmic amplification.",
        year=2024,
        doi="10.1234/mock003",
        journal="New Media & Society",
        citations_count=72,
        keywords=["algorithms", "gatekeeping", "social media", "history"],
        source="crossref",
    ),
    Paper(
        title="The Epistemology of Machine-Generated Knowledge",
        authors=["Maria Gonzalez"],
        abstract="This philosophical investigation examines the epistemological status of knowledge claims produced by large language models. I argue for a novel framework that distinguishes between computational fluency and genuine understanding.",
        year=2025,
        doi="10.1234/mock004",
        journal="Episteme",
        citations_count=15,
        keywords=["epistemology", "AI", "knowledge", "LLM"],
        source="openalex",
    ),
    Paper(
        title="Cultural Heritage in the Age of Generative AI",
        authors=["Yuki Tanaka", "Robert Kim"],
        abstract="We examine the implications of generative AI for cultural heritage preservation and interpretation. Through case studies of museum exhibitions, we show both opportunities and risks of AI-mediated cultural experiences.",
        year=2024,
        doi="10.1234/mock005",
        journal="International Journal of Heritage Studies",
        citations_count=33,
        keywords=["cultural heritage", "generative AI", "museums"],
        source="semantic_scholar",
    ),
]

MOCK_SCHOLARS = [
    ScholarProfile(
        name="Shoshana Zuboff",
        affiliation="Harvard Business School",
        h_index=42,
        citation_count=35000,
        paper_count=85,
        top_papers=["The Age of Surveillance Capitalism", "Big Other: Surveillance Capitalism and the Prospects of an Information Civilization"],
        research_interests=["surveillance capitalism", "digital economy", "information technology"],
        source_id="mock:zuboff",
    ),
    ScholarProfile(
        name="Safiya Umoja Noble",
        affiliation="UCLA",
        h_index=28,
        citation_count=12000,
        paper_count=45,
        top_papers=["Algorithms of Oppression", "The Intersectional Internet"],
        research_interests=["algorithmic bias", "digital culture", "race and technology"],
        source_id="mock:noble",
    ),
    ScholarProfile(
        name="Luciano Floridi",
        affiliation="Yale University",
        h_index=75,
        citation_count=55000,
        paper_count=300,
        top_papers=["The Ethics of Artificial Intelligence", "The Fourth Revolution"],
        research_interests=["philosophy of information", "AI ethics", "digital ethics"],
        source_id="mock:floridi",
    ),
]

# --- Mock LLM responses for each pipeline stage ---

MOCK_RESPONSES = {
    "review": json.dumps({
        "themes": [
            {"name": "Algorithmic mediation of knowledge", "description": "How algorithms shape what people know and believe", "paper_count": 3},
            {"name": "AI and democratic discourse", "description": "Impact of AI on public deliberation", "paper_count": 2},
            {"name": "Epistemological challenges of AI", "description": "Philosophical questions about AI knowledge", "paper_count": 2},
        ],
        "gaps": [
            "Limited empirical research on how LLM-generated historical narratives affect collective memory formation",
            "Insufficient cross-cultural comparison of AI's impact on different memory cultures",
            "No systematic framework connecting AI text generation to collective memory theory",
        ],
        "key_debates": [
            "Whether AI-generated text constitutes a genuine epistemic threat or merely amplifies existing biases",
            "The role of human agency in algorithmic memory formation",
        ],
        "methodology_trends": ["Mixed methods combining computational and qualitative approaches", "Case study methodology"],
        "timeline_narrative": "Research has evolved from early concerns about digital memory (2020-2022) to sophisticated analyses of AI-specific impacts (2023-2025).",
        "future_directions": ["Longitudinal studies of AI impact on memory", "Cross-cultural comparisons", "Policy frameworks"],
    }),

    "gaps": json.dumps({
        "gaps": [
            {
                "title": "LLMs as Active Agents in Collective Memory Formation",
                "description": "No study has systematically examined how LLM-generated historical narratives enter and reshape collective memory.",
                "severity": "high",
                "addressable": True,
            },
            {
                "title": "Cross-Cultural Variations in AI-Mediated Memory",
                "description": "Existing research is primarily Western-centric, ignoring how different cultural memory traditions interact with AI systems.",
                "severity": "high",
                "addressable": True,
            },
        ],
        "connections": ["The intersection of AI epistemology and memory studies remains largely unexplored."],
    }),

    "proposals": json.dumps([
        {
            "question": "How do LLMs reshape collective memory through the generation of historically-inflected text in the digital public sphere?",
            "hypothesis": "Exposure to LLM-generated historical narratives significantly alters recall accuracy and narrative framing of historical events.",
            "rationale": "As LLMs become primary generators of online text, their outputs increasingly shape shared historical understanding, yet no systematic study exists.",
            "methodology": "Mixed-methods: computational analysis of LLM outputs on historical topics combined with experimental studies of exposure effects on memory.",
            "data_sources": ["LLM-generated texts", "Survey data", "Interview transcripts"],
            "theoretical_framework": "Halbwachs collective memory theory extended with algorithmic mediation framework",
            "expected_contribution": "First systematic framework connecting LLM capabilities to collective memory theory with empirical evidence.",
            "feasibility": "high",
            "novelty": "high",
            "related_gaps": ["LLMs as Active Agents in Collective Memory Formation"],
        },
    ]),

    "outline": json.dumps({
        "title": "Large Language Models as Cultural Agents: How AI-Generated Text Reshapes Collective Memory and Historical Narratives in the Digital Public Sphere",
        "abstract_draft": "This paper investigates the role of large language models as cultural agents in the formation and transformation of collective memory.",
        "sections": [
            {
                "title": "Introduction",
                "description": "Frame the research problem",
                "key_points": ["Rise of LLMs in public discourse", "Gap in memory studies", "Research questions"],
                "estimated_words": 1500,
                "citations_needed": ["Chen2024", "Wright2025"],
                "subsections": [],
            },
            {
                "title": "Theoretical Framework",
                "description": "Connect collective memory theory with AI studies",
                "key_points": ["Halbwachs and collective memory", "Digital memory studies", "LLMs as cultural agents"],
                "estimated_words": 2000,
                "citations_needed": ["Wright2025", "Gonzalez2025"],
                "subsections": [
                    {"title": "Collective Memory in the Digital Age", "description": "Review of digital memory literature", "key_points": ["Platform mediation", "Algorithmic curation"], "estimated_words": 800, "citations_needed": ["Chen2024"], "subsections": []},
                ],
            },
            {
                "title": "Methodology",
                "description": "Research design and methods",
                "key_points": ["Mixed methods design", "Computational analysis", "Interview protocol"],
                "estimated_words": 1500,
                "citations_needed": ["Anderson2024"],
                "subsections": [],
            },
            {
                "title": "Analysis and Discussion",
                "description": "Findings and interpretation",
                "key_points": ["LLM output patterns", "Memory formation effects", "Cultural implications"],
                "estimated_words": 2500,
                "citations_needed": ["Chen2024", "Wright2025", "Gonzalez2025"],
                "subsections": [],
            },
            {
                "title": "Conclusion",
                "description": "Summary and implications",
                "key_points": ["Key findings", "Theoretical contribution", "Policy implications"],
                "estimated_words": 500,
                "citations_needed": [],
                "subsections": [],
            },
        ],
    }),

    "abstract": "This paper investigates the emerging role of large language models (LLMs) as cultural agents in the formation and transformation of collective memory within the digital public sphere. As AI-generated text becomes increasingly prevalent in online discourse, questions arise about how algorithmic production of historically-inflected narratives affects shared understandings of the past. Drawing on Halbwachs's framework of collective memory and extending it to account for non-human textual agents, we propose a novel theoretical model — the 'algorithmic memory loop' — that captures the feedback dynamics between LLM outputs and human memory formation. Through a mixed-methods approach combining computational analysis of LLM-generated historical narratives (n=50,000 texts) with qualitative interviews of 45 participants, we demonstrate that exposure to AI-generated historical content significantly alters recall accuracy, narrative framing, and emotional valence of historical memories. Our findings reveal three distinct mechanisms through which LLMs reshape collective memory: narrative smoothing, temporal compression, and perspective homogenization. These findings contribute to both memory studies and AI ethics by providing the first empirical framework for understanding AI's role as a cultural memory agent.",

    "section": """The proliferation of large language models marks a watershed moment in the history of public discourse. Unlike previous technologies of textual production — from the printing press to word processors — LLMs generate text that is not merely reproduced or edited by human authors but is produced through statistical patterns derived from vast corpora of human-generated text [Chen2024]. This fundamental shift raises urgent questions about the nature of textual agency and its implications for how societies remember and narrate their pasts.

Collective memory, as theorized by Maurice Halbwachs and subsequently developed by scholars such as Jan Assmann and Aleida Assmann, is inherently social and mediated. It depends on shared frameworks of interpretation, communal practices of remembrance, and — crucially — the technologies through which memories are stored, transmitted, and reconstructed [Wright2025]. The digital turn in memory studies has already demonstrated how platforms reshape memorial practices through algorithmic curation and viral dynamics.

Yet the emergence of generative AI introduces a qualitatively different challenge. When an LLM produces a historical narrative, it draws upon patterns in its training data that reflect — but also transform — existing collective memories. The resulting text may appear authoritative while subtly altering factual details, shifting emotional registers, or collapsing complex historical debates into simplified narratives. As these AI-generated texts circulate in the digital public sphere, they enter the same memorial ecosystem as human-authored accounts, potentially reshaping collective understanding without clear markers of their algorithmic origins.

This paper addresses three research questions: (1) How do LLMs transform historical narratives in their text generation process? (2) What effects does exposure to AI-generated historical content have on individual and collective memory? (3) What theoretical framework best captures the relationship between algorithmic text production and collective memory formation?""",

    "review_json": json.dumps({
        "scores": [
            {"criterion": "Originality", "score": 8, "comment": "Novel theoretical framework connecting LLMs to collective memory theory. The 'algorithmic memory loop' concept is innovative."},
            {"criterion": "Theoretical Framework", "score": 7, "comment": "Strong grounding in Halbwachs and digital memory studies, though the bridge to AI studies could be more rigorous."},
            {"criterion": "Methodology", "score": 7, "comment": "Mixed methods approach is appropriate. Sample size adequate but could benefit from longitudinal component."},
            {"criterion": "Literature Engagement", "score": 8, "comment": "Comprehensive engagement with memory studies, though some key AI ethics works are missing."},
            {"criterion": "Argumentation & Evidence", "score": 7, "comment": "Arguments are generally well-supported. The three mechanisms need more empirical backing."},
            {"criterion": "Clarity & Writing", "score": 8, "comment": "Well-written and clearly organized. Technical concepts are made accessible."},
            {"criterion": "Significance", "score": 8, "comment": "Timely and important contribution to an emerging field."},
        ],
        "strengths": [
            "Original theoretical contribution with the 'algorithmic memory loop' framework",
            "Timely topic addressing a genuine gap in the literature",
            "Clear writing style that bridges technical and humanistic audiences",
        ],
        "weaknesses": [
            "The causal mechanisms linking LLM exposure to memory change need stronger empirical support",
            "Limited attention to non-Western memory cultures and AI systems",
            "The policy implications section is underdeveloped",
        ],
        "detailed_comments": "This paper makes a valuable contribution to the nascent field of AI and collective memory studies. The theoretical innovation of framing LLMs as 'cultural agents' rather than mere tools is compelling and opens productive avenues for future research. However, several issues need attention. First, the empirical evidence for the three mechanisms (narrative smoothing, temporal compression, perspective homogenization) relies heavily on the experimental setup, which may not capture the complexity of real-world memory formation. Second, the paper would benefit from engaging with non-Western perspectives on collective memory, particularly given that different cultural traditions may interact with AI systems in fundamentally different ways.",
        "suggestions": [
            "Add a longitudinal dimension to capture memory formation over time",
            "Include cross-cultural comparison, even if preliminary",
            "Strengthen the policy implications with concrete recommendations",
            "Engage more deeply with the AI alignment and safety literature",
        ],
        "decision": "minor_revision",
    }),

    "synthesis": json.dumps({
        "meta_review": "The three reviewers are in broad agreement that this paper makes a significant and timely contribution to the intersection of AI studies and collective memory theory. The proposed 'algorithmic memory loop' framework is recognized as an original theoretical contribution. However, all reviewers note the need for stronger empirical grounding of the proposed mechanisms and greater attention to cross-cultural perspectives. The consensus recommendation is minor revision, with particular attention to strengthening the empirical evidence and expanding the policy discussion.",
        "key_strengths": [
            "Original theoretical framework bridging AI and memory studies",
            "Clear, accessible writing that serves an interdisciplinary audience",
            "Timely topic with significant implications for multiple fields",
        ],
        "critical_issues": [
            "Empirical evidence for the three mechanisms needs strengthening",
            "Cross-cultural perspectives are largely absent",
            "Policy implications are underdeveloped",
        ],
        "revision_instructions": "Please revise the manuscript addressing the following: (1) Provide additional empirical support for the three mechanisms of memory reshaping, ideally through supplementary data analysis or more detailed case studies. (2) Add a section discussing how non-Western memory cultures may interact differently with AI systems, even if this is framed as a limitation and future direction. (3) Expand the policy implications section with 2-3 concrete, actionable recommendations for platform governance and AI regulation. (4) Engage more substantively with the AI safety literature, particularly work on truthfulness and alignment.",
    }),
}


class MockLLMClient:
    """Mock LLM that returns pre-scripted responses based on prompt content."""

    def __init__(self):
        self.call_count = 0
        self.calls = []
        from src.utils.llm import UsageTracker
        self.usage = UsageTracker()

    async def generate(self, prompt, *, system="", temperature=None, max_tokens=None):
        self.call_count += 1
        self.calls.append({"prompt": prompt[:100], "system": system[:50]})
        # Simulate token usage
        input_tokens = len(prompt.split()) + len(system.split())
        output_tokens = 500
        self.usage.record(input_tokens, output_tokens)

        # Route to appropriate mock response
        if "abstract" in prompt.lower() and "200-300 words" in prompt:
            return MOCK_RESPONSES["abstract"]
        elif "section" in prompt.lower() and "write this section" in prompt.lower():
            return MOCK_RESPONSES["section"]
        elif "write this subsection" in prompt.lower():
            return MOCK_RESPONSES["section"][:600]
        elif "revise" in prompt.lower() and "peer review" in prompt.lower():
            return "# Revised: " + MOCK_RESPONSES["abstract"] + "\n\n## Introduction\n\n" + MOCK_RESPONSES["section"]
        elif "revise" in prompt.lower():
            return "# Revised: " + MOCK_RESPONSES["abstract"] + "\n\n## Introduction\n\n" + MOCK_RESPONSES["section"]
        return MOCK_RESPONSES["section"]

    async def generate_structured(self, prompt, *, system="", temperature=None):
        self.call_count += 1
        self.calls.append({"prompt": prompt[:100], "system": system[:50]})
        input_tokens = len(prompt.split()) + len(system.split())
        self.usage.record(input_tokens, 300)

        p = prompt.lower()
        if "themes" in p and "gaps" in p:
            return MOCK_RESPONSES["review"]
        elif "severity" in p or ("gap" in p and "significance" in p):
            return MOCK_RESPONSES["gaps"]
        elif "recommend the best proposal" in p or ("recommended" in p and "evaluate" in p):
            return json.dumps({"recommended": 0, "evaluation": "Strong proposal with high novelty."})
        elif "research proposals" in p and "methodology" in p and "generate" in p:
            return MOCK_RESPONSES["proposals"]
        elif "sections" in p and "outline" in p:
            return MOCK_RESPONSES["outline"]
        elif "scores" in p and "criterion" in p:
            return MOCK_RESPONSES["review_json"]
        elif "meta_review" in p:
            return MOCK_RESPONSES["synthesis"]
        elif "real" in p and "scholar" in p:
            return json.dumps([
                {"name": "Shoshana Zuboff", "affiliation": "Harvard", "research_interests": ["AI", "capitalism"], "notable_works": ["Surveillance Capitalism"]},
            ])
        return MOCK_RESPONSES["review"]

    async def close(self):
        pass


async def mock_search(query, *, discipline=None, year_from=None, year_to=None,
                       limit=20, page=1, language=None):
    """Mock academic search that returns pre-built papers."""
    return SearchResult(
        papers=MOCK_PAPERS[:limit],
        total_count=len(MOCK_PAPERS),
        query=query,
        source_name="mock",
        page=1,
        has_more=False,
    )


async def run_dry_run():
    """Execute the full pipeline with mock components."""
    logger.info("=" * 60)
    logger.info("DRY RUN: Full Pipeline Simulation")
    logger.info("=" * 60)

    topic = PAPERS[0]["topic"] if "PAPERS" in dir() else (
        "Large Language Models as Cultural Agents: How AI-Generated Text "
        "Reshapes Collective Memory and Historical Narratives in the Digital Public Sphere"
    )

    config = ResearchConfig(
        topic=topic,
        discipline=Discipline.SOCIOLOGY,
        discipline_type="social_science",
        language="en",
        target_word_count=8000,
        paper_type="research_article",
        depth="standard",
        max_papers=30,
        output_dir="output/dry_run",
        output_format="markdown",
        llm_provider="openai",
        llm_model="mock",
        enabled_sources=["openalex"],
        enable_peer_review=True,
        num_reviewers=3,
        review_rounds=1,
    )

    orchestrator = ResearchOrchestrator(config)

    # Replace real components with mocks
    mock_llm = MockLLMClient()
    orchestrator.llm = mock_llm
    orchestrator.reviewer.llm = mock_llm
    orchestrator.gap_analyzer.llm = mock_llm
    orchestrator.hypothesis_gen.llm = mock_llm
    orchestrator.outliner.llm = mock_llm
    orchestrator.writer.llm = mock_llm
    orchestrator.peer_reviewer.llm = mock_llm

    # Mock data sources
    for src in orchestrator.sources.sources:
        src.search = mock_search

    # Mock peer reviewer's scholar finder to return our mock scholars
    original_find = orchestrator.peer_reviewer.find_scholars
    async def mock_find_scholars(topic, discipline, *, count=3):
        return MOCK_SCHOLARS[:count]
    orchestrator.peer_reviewer.find_scholars = mock_find_scholars

    stages_seen = []
    async def progress(stage, msg):
        stages_seen.append(stage)
        logger.info(f"  Stage: {stage} — {msg}")

    start = time.time()

    try:
        session = await orchestrator.run_full_pipeline(progress)
        elapsed = time.time() - start

        logger.info(f"\n{'='*60}")
        logger.info("RESULTS")
        logger.info(f"{'='*60}")

        # Validate each stage produced output
        checks = [
            ("Literature Review", session.review_result is not None),
            ("Gap Analysis", session.gap_result is not None),
            ("Proposals", session.proposals is not None),
            ("Outline", session.outline is not None),
            ("Draft", session.draft is not None),
            ("Peer Review", session.peer_review_result is not None),
        ]

        all_ok = True
        for name, ok in checks:
            status = "PASS" if ok else "FAIL"
            logger.info(f"  [{status}] {name}")
            if not ok:
                all_ok = False

        logger.info(f"\n  Pipeline stages: {' → '.join(stages_seen)}")
        logger.info(f"  LLM calls: {mock_llm.call_count}")
        logger.info(f"  Simulated usage: {mock_llm.usage.summary()}")
        logger.info(f"  Elapsed: {elapsed:.1f}s")

        if session.draft:
            logger.info(f"  Draft word count: ~{session.draft.word_count}")
            # Check output files exist
            out_dir = config.output_dir
            if os.path.exists(out_dir):
                files = os.listdir(out_dir)
                logger.info(f"  Output files: {', '.join(sorted(files))}")

        if session.peer_review_result:
            pr = session.peer_review_result
            logger.info(f"  Peer review score: {pr.average_score:.1f}/10")
            logger.info(f"  Decision: {pr.consensus_decision}")
            for r in pr.reviews:
                logger.info(f"    - {r.reviewer.name}: {r.overall_score:.1f}/10 ({r.decision})")

        if session.errors:
            logger.warning(f"  Errors: {session.errors}")

        logger.info(f"\n  {'ALL CHECKS PASSED' if all_ok else 'SOME CHECKS FAILED'}")

        # Cost estimation for real run
        logger.info(f"\n{'='*60}")
        logger.info("COST ESTIMATION (for real OpenRouter run)")
        logger.info(f"{'='*60}")
        # Estimate based on mock call patterns
        est_input = mock_llm.call_count * 3000  # ~3k tokens avg input
        est_output = mock_llm.call_count * 1500  # ~1.5k tokens avg output
        models = {
            "deepseek/deepseek-chat-v3-0324": (0.27, 1.10),
            "google/gemini-2.0-flash-001": (0.10, 0.40),
            "anthropic/claude-sonnet-4": (3.00, 15.00),
        }
        for model, (pin, pout) in models.items():
            cost = est_input * pin / 1e6 + est_output * pout / 1e6
            logger.info(f"  {model}: ~${cost:.3f}/paper (${cost*3:.2f} for 3 papers)")

        return all_ok

    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    success = asyncio.run(run_dry_run())
    sys.exit(0 if success else 1)
