"""Tests for the research pipeline components."""

import pytest

from src.data_sources.base import Paper
from src.pipeline.literature_review import LiteratureReviewer


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
