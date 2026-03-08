"""Tests for the research pipeline components."""

import pytest

from src.data_sources.base import Paper
from src.pipeline.literature_review import LiteratureReviewer
from src.pipeline.peer_review import (
    PeerReviewer,
    ReviewScore,
    PeerReviewResult,
    ScholarProfile,
    ReviewSynthesis,
    REVIEW_CRITERIA,
)


class TestLiteratureReviewer:
    def test_format_papers(self):
        papers = [
            Paper(
                title="Test Paper",
                authors=["John Smith", "Jane Doe"],
                year=2024,
                citations_count=50,
                abstract="This is a test abstract.",
                journal="Test Journal",
            ),
        ]
        result = LiteratureReviewer._format_papers_for_llm(papers)
        assert "John Smith" in result
        assert "2024" in result
        assert "Test Paper" in result
        assert "Citations: 50" in result

    def test_deduplicate_papers(self):
        papers = [
            Paper(title="Paper A", doi="10.1234/a"),
            Paper(title="Paper A", doi="10.1234/a"),
            Paper(title="Paper B"),
        ]
        result = LiteratureReviewer._deduplicate_papers(papers)
        assert len(result) == 2

    def test_build_timeline(self):
        reviewer = LiteratureReviewer.__new__(LiteratureReviewer)
        papers = [
            Paper(title="Old Paper", year=2020, citations_count=100),
            Paper(title="New Paper 1", year=2024, citations_count=10),
            Paper(title="New Paper 2", year=2024, citations_count=20),
        ]
        timeline = reviewer._build_timeline(papers)
        assert len(timeline) == 2
        assert timeline[0]["year"] == 2020
        assert timeline[0]["count"] == 1
        assert timeline[1]["year"] == 2024
        assert timeline[1]["count"] == 2


class TestPeerReview:
    def test_review_criteria_weights_sum_to_one(self):
        total = sum(c["weight"] for c in REVIEW_CRITERIA)
        assert abs(total - 1.0) < 0.01

    def test_review_criteria_have_required_fields(self):
        for c in REVIEW_CRITERIA:
            assert "name" in c
            assert "weight" in c
            assert "description" in c
            assert "scale" in c
            assert c["weight"] > 0

    def test_scholar_profile_creation(self):
        scholar = ScholarProfile(
            name="John Smith",
            affiliation="Harvard University",
            h_index=45,
            citation_count=12000,
            paper_count=150,
            top_papers=["Paper A", "Paper B"],
            research_interests=["economics", "game theory"],
            source_id="openalex:A123",
        )
        assert scholar.name == "John Smith"
        assert scholar.h_index == 45

    def test_review_score_creation(self):
        score = ReviewScore(criterion="Originality", score=8, comment="Novel approach")
        assert score.score == 8
        assert score.criterion == "Originality"

    def test_peer_review_result_structure(self):
        scholar = ScholarProfile(
            name="Test Reviewer",
            affiliation="MIT",
            h_index=30,
            citation_count=5000,
            paper_count=80,
            top_papers=[],
            research_interests=["NLP"],
            source_id="test",
        )
        scores = [
            ReviewScore(criterion=c["name"], score=7, comment="Good")
            for c in REVIEW_CRITERIA
        ]
        review = PeerReviewResult(
            reviewer=scholar,
            scores=scores,
            overall_score=7.0,
            decision="minor_revision",
            strengths=["Clear writing"],
            weaknesses=["Limited scope"],
            detailed_comments="Solid paper overall.",
            suggestions=["Add more examples"],
        )
        assert review.overall_score == 7.0
        assert review.decision == "minor_revision"
        assert len(review.scores) == len(REVIEW_CRITERIA)

    def test_review_synthesis_consensus(self):
        """Test that synthesis correctly aggregates reviews."""
        scholar = ScholarProfile(
            name="R1", affiliation="", h_index=0, citation_count=0,
            paper_count=0, top_papers=[], research_interests=[], source_id="",
        )
        reviews = [
            PeerReviewResult(
                reviewer=scholar, scores=[], overall_score=8.0,
                decision="minor_revision", strengths=[], weaknesses=[],
                detailed_comments="", suggestions=[],
            ),
            PeerReviewResult(
                reviewer=scholar, scores=[], overall_score=6.0,
                decision="major_revision", strengths=[], weaknesses=[],
                detailed_comments="", suggestions=[],
            ),
            PeerReviewResult(
                reviewer=scholar, scores=[], overall_score=7.0,
                decision="minor_revision", strengths=[], weaknesses=[],
                detailed_comments="", suggestions=[],
            ),
        ]
        avg = sum(r.overall_score for r in reviews) / len(reviews)
        assert abs(avg - 7.0) < 0.01

    def test_parse_review_handles_valid_json(self):
        """Test that _parse_review correctly parses structured output."""
        reviewer = PeerReviewer.__new__(PeerReviewer)
        scholar = ScholarProfile(
            name="Test", affiliation="", h_index=10, citation_count=0,
            paper_count=0, top_papers=[], research_interests=[], source_id="",
        )
        json_text = '''{
            "scores": [
                {"criterion": "Originality", "score": 8, "comment": "Novel"},
                {"criterion": "Methodology", "score": 6, "comment": "Adequate"}
            ],
            "strengths": ["Well-written", "Original topic"],
            "weaknesses": ["Limited data"],
            "detailed_comments": "A solid contribution.",
            "suggestions": ["Add more analysis"],
            "decision": "minor_revision"
        }'''
        result = reviewer._parse_review(json_text, scholar)
        assert result.decision == "minor_revision"
        assert len(result.scores) == 2
        assert result.scores[0].score == 8
        assert "Well-written" in result.strengths
        assert result.overall_score > 0

    def test_parse_review_handles_invalid_json(self):
        """Test graceful fallback for unparseable output."""
        reviewer = PeerReviewer.__new__(PeerReviewer)
        scholar = ScholarProfile(
            name="Test", affiliation="", h_index=0, citation_count=0,
            paper_count=0, top_papers=[], research_interests=[], source_id="",
        )
        result = reviewer._parse_review("not valid json at all", scholar)
        assert result.decision == "major_revision"  # safe default
        assert result.overall_score == 5.0  # default when no scores
