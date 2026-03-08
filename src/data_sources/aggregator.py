"""Aggregated data source that searches across multiple academic databases."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from .base import DataSource, Discipline, Paper, SearchResult

logger = logging.getLogger(__name__)


class AggregatedSource:
    """Searches multiple data sources in parallel and deduplicates results.

    This is the primary interface for the research pipeline to access
    academic literature across all configured sources.
    """

    def __init__(self, sources: list[DataSource] | None = None):
        self.sources: list[DataSource] = sources or []

    def add_source(self, source: DataSource) -> None:
        self.sources.append(source)

    async def search(
        self,
        query: str,
        *,
        discipline: Discipline | None = None,
        year_from: int | None = None,
        year_to: int | None = None,
        limit: int = 20,
        page: int = 1,
        language: str | None = None,
        sources: list[str] | None = None,
    ) -> SearchResult:
        """Search all configured sources in parallel."""
        active_sources = self.sources
        if sources:
            active_sources = [s for s in self.sources if s.name in sources]

        if not active_sources:
            return SearchResult(
                papers=[], total_count=0, query=query,
                source_name="aggregated", page=page, has_more=False,
            )

        tasks = [
            self._safe_search(
                source, query,
                discipline=discipline, year_from=year_from, year_to=year_to,
                limit=limit, page=page, language=language,
            )
            for source in active_sources
        ]

        results = await asyncio.gather(*tasks)

        all_papers: list[Paper] = []
        total_count = 0
        has_more = False

        for result in results:
            if result:
                all_papers.extend(result.papers)
                total_count += result.total_count
                has_more = has_more or result.has_more

        # Deduplicate by DOI, then by title similarity
        deduped = self._deduplicate(all_papers)

        # Sort by citation count (descending), then year (descending)
        deduped.sort(key=lambda p: (p.citations_count, p.year or 0), reverse=True)

        return SearchResult(
            papers=deduped[:limit * 2],  # return more since we aggregated
            total_count=total_count,
            query=query,
            source_name="aggregated",
            page=page,
            has_more=has_more,
        )

    async def get_paper(self, identifier: str) -> Paper | None:
        """Try to find a paper across all sources."""
        for source in self.sources:
            paper = await source.get_paper(identifier)
            if paper:
                return paper
        return None

    async def get_full_text(self, paper: Paper) -> str | None:
        """Try to get full text from any source that supports it."""
        for source in self.sources:
            if source.supports_full_text:
                text = await source.get_full_text(paper)
                if text:
                    return text
        return None

    async def get_citation_network(
        self, paper: Paper, depth: int = 1
    ) -> dict[str, list[Paper]]:
        """Build citation network around a paper."""
        network: dict[str, list[Paper]] = {"references": [], "citations": []}

        for source in self.sources:
            if source.supports_citations:
                try:
                    refs = await source.get_references(paper)
                    network["references"].extend(refs)
                    cites = await source.get_citations(paper)
                    network["citations"].extend(cites)
                except Exception as e:
                    logger.warning(f"Error getting citations from {source.name}: {e}")

        network["references"] = self._deduplicate(network["references"])
        network["citations"] = self._deduplicate(network["citations"])

        return network

    async def _safe_search(
        self, source: DataSource, query: str, **kwargs: Any
    ) -> SearchResult | None:
        try:
            return await source.search(query, **kwargs)
        except Exception as e:
            logger.warning(f"Search failed for {source.name}: {e}")
            return None

    @staticmethod
    def _deduplicate(papers: list[Paper]) -> list[Paper]:
        """Deduplicate papers by DOI, then by normalized title."""
        seen_dois: set[str] = set()
        seen_titles: set[str] = set()
        unique: list[Paper] = []

        for paper in papers:
            if paper.doi:
                doi_lower = paper.doi.lower()
                if doi_lower in seen_dois:
                    continue
                seen_dois.add(doi_lower)

            title_norm = paper.title.lower().strip()
            # Remove common punctuation for comparison
            title_key = "".join(c for c in title_norm if c.isalnum() or c == " ")
            if title_key in seen_titles:
                continue
            seen_titles.add(title_key)

            unique.append(paper)

        return unique

    async def close(self) -> None:
        await asyncio.gather(*[s.close() for s in self.sources])
