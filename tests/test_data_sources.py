"""Tests for data source connectors."""

import pytest

from src.data_sources.base import DataSource, Discipline, Paper, SearchResult
from src.data_sources.openalex import OpenAlexSource
from src.data_sources.semantic_scholar import SemanticScholarSource
from src.data_sources.crossref import CrossRefSource
from src.data_sources.aggregator import AggregatedSource


class TestPaper:
    def test_citation_key(self):
        paper = Paper(title="Test Paper", authors=["John Smith"], year=2024)
        assert paper.citation_key == "Smith2024"

    def test_citation_key_no_author(self):
        paper = Paper(title="Test Paper", year=2024)
        assert paper.citation_key == "Unknown2024"

    def test_apa_citation(self):
        paper = Paper(
            title="Test Paper",
            authors=["John Smith", "Jane Doe"],
            year=2024,
            journal="Journal of Testing",
            doi="10.1234/test",
        )
        citation = paper.to_citation("apa")
        assert "John Smith, Jane Doe" in citation
        assert "2024" in citation
        assert "Test Paper" in citation
        assert "Journal of Testing" in citation

    def test_chicago_citation(self):
        paper = Paper(
            title="Test Paper",
            authors=["John Smith"],
            year=2024,
        )
        citation = paper.to_citation("chicago")
        assert "John Smith" in citation
        assert "2024" in citation


class TestAggregatedSource:
    def test_deduplicate_by_doi(self):
        papers = [
            Paper(title="Paper A", doi="10.1234/a", authors=["Author1"]),
            Paper(title="Paper A duplicate", doi="10.1234/a", authors=["Author1"]),
            Paper(title="Paper B", doi="10.1234/b", authors=["Author2"]),
        ]
        result = AggregatedSource._deduplicate(papers)
        assert len(result) == 2

    def test_deduplicate_by_title(self):
        papers = [
            Paper(title="Same Title Here", authors=["Author1"]),
            Paper(title="Same Title Here", authors=["Author2"]),
            Paper(title="Different Title", authors=["Author3"]),
        ]
        result = AggregatedSource._deduplicate(papers)
        assert len(result) == 2

    def test_deduplicate_case_insensitive(self):
        papers = [
            Paper(title="A Study of Something", authors=["Author1"]),
            Paper(title="a study of something", authors=["Author2"]),
        ]
        result = AggregatedSource._deduplicate(papers)
        assert len(result) == 1


class TestOpenAlexSource:
    def test_reconstruct_abstract(self):
        inverted = {"Hello": [0], "world": [1], "this": [2], "is": [3], "a": [4], "test": [5]}
        result = OpenAlexSource._reconstruct_abstract(inverted)
        assert result == "Hello world this is a test"

    def test_reconstruct_empty_abstract(self):
        assert OpenAlexSource._reconstruct_abstract({}) == ""
        assert OpenAlexSource._reconstruct_abstract(None) == ""


@pytest.mark.asyncio
class TestOpenAlexIntegration:
    """Integration tests that hit the real OpenAlex API.

    These tests are marked to be skippable in CI.
    """

    @pytest.mark.skipif(True, reason="Integration test - run manually")
    async def test_search(self):
        source = OpenAlexSource()
        try:
            result = await source.search("digital humanities", limit=5)
            assert len(result.papers) > 0
            assert result.papers[0].title
        finally:
            await source.close()


@pytest.mark.asyncio
class TestSemanticScholarIntegration:
    @pytest.mark.skipif(True, reason="Integration test - run manually")
    async def test_search(self):
        source = SemanticScholarSource()
        try:
            result = await source.search("economic growth inequality", limit=5)
            assert len(result.papers) > 0
        finally:
            await source.close()
