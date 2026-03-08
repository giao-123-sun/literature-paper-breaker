"""Semantic Scholar data source connector.

Semantic Scholar is a free AI-powered research tool by the Allen Institute for AI.
Provides rich citation graph and paper metadata.

API docs: https://api.semanticscholar.org/
"""

from __future__ import annotations

import os
from typing import Any

import httpx

from .base import DataSource, Discipline, Paper, SearchResult

BASE_URL = "https://api.semanticscholar.org/graph/v1"
SEARCH_URL = "https://api.semanticscholar.org"

# Semantic Scholar field of study mappings
DISCIPLINE_FIELDS: dict[Discipline, str] = {
    Discipline.ECONOMICS: "Economics",
    Discipline.HISTORY: "History",
    Discipline.POLITICAL_SCIENCE: "Political Science",
    Discipline.SOCIOLOGY: "Sociology",
    Discipline.PHILOSOPHY: "Philosophy",
    Discipline.LINGUISTICS: "Linguistics",
    Discipline.ANTHROPOLOGY: "Sociology",  # closest match
    Discipline.LAW: "Law",
    Discipline.EDUCATION: "Education",
    Discipline.PSYCHOLOGY: "Psychology",
    Discipline.ART_HISTORY: "Art",
}

PAPER_FIELDS = (
    "paperId,title,abstract,year,authors,citationCount,referenceCount,"
    "journal,fieldsOfStudy,url,externalIds,publicationTypes,tldr"
)


class SemanticScholarSource(DataSource):
    """Semantic Scholar academic data source.

    Free tier: 1 request/second without API key, 10 requests/second with key.
    """

    name = "semantic_scholar"
    supports_full_text = False
    supports_citations = True
    requires_auth = False
    supported_languages = ["en"]

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
        headers = {}
        if self.api_key:
            headers["x-api-key"] = self.api_key
        self._client = httpx.AsyncClient(timeout=30.0, headers=headers)

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
    ) -> SearchResult:
        params: dict[str, Any] = {
            "query": query,
            "limit": min(limit, 100),
            "offset": (page - 1) * limit,
            "fields": PAPER_FIELDS,
        }

        if year_from or year_to:
            year_range = f"{year_from or ''}-{year_to or ''}"
            params["year"] = year_range

        if discipline and discipline in DISCIPLINE_FIELDS:
            params["fieldsOfStudy"] = DISCIPLINE_FIELDS[discipline]

        resp = await self._client.get(
            f"{SEARCH_URL}/graph/v1/paper/search", params=params
        )
        resp.raise_for_status()
        data = resp.json()

        papers = [self._parse_paper(p) for p in data.get("data", [])]
        total = data.get("total", 0)

        return SearchResult(
            papers=papers,
            total_count=total,
            query=query,
            source_name=self.name,
            page=page,
            has_more=(page * limit) < total,
        )

    async def get_paper(self, identifier: str) -> Paper | None:
        if identifier.startswith("10."):
            url = f"{BASE_URL}/paper/DOI:{identifier}"
        else:
            url = f"{BASE_URL}/paper/{identifier}"

        try:
            resp = await self._client.get(url, params={"fields": PAPER_FIELDS})
            resp.raise_for_status()
            return self._parse_paper(resp.json())
        except httpx.HTTPStatusError:
            return None

    async def get_references(self, paper: Paper) -> list[Paper]:
        paper_id = paper.metadata.get("s2_paper_id")
        if not paper_id:
            return []
        resp = await self._client.get(
            f"{BASE_URL}/paper/{paper_id}/references",
            params={"fields": PAPER_FIELDS, "limit": 100},
        )
        resp.raise_for_status()
        data = resp.json()
        return [
            self._parse_paper(ref["citedPaper"])
            for ref in data.get("data", [])
            if ref.get("citedPaper", {}).get("paperId")
        ]

    async def get_citations(self, paper: Paper) -> list[Paper]:
        paper_id = paper.metadata.get("s2_paper_id")
        if not paper_id:
            return []
        resp = await self._client.get(
            f"{BASE_URL}/paper/{paper_id}/citations",
            params={"fields": PAPER_FIELDS, "limit": 100},
        )
        resp.raise_for_status()
        data = resp.json()
        return [
            self._parse_paper(cit["citingPaper"])
            for cit in data.get("data", [])
            if cit.get("citingPaper", {}).get("paperId")
        ]

    def _parse_paper(self, data: dict[str, Any]) -> Paper:
        authors = [a.get("name", "") for a in data.get("authors", []) if a.get("name")]

        doi = None
        external_ids = data.get("externalIds", {})
        if external_ids:
            doi = external_ids.get("DOI")

        journal_info = data.get("journal")
        journal = ""
        if journal_info:
            journal = journal_info.get("name", "") if isinstance(journal_info, dict) else str(journal_info)

        keywords = data.get("fieldsOfStudy", []) or []

        abstract = data.get("abstract", "") or ""
        tldr = data.get("tldr")
        if not abstract and tldr:
            abstract = tldr.get("text", "") if isinstance(tldr, dict) else ""

        return Paper(
            title=data.get("title", ""),
            authors=authors,
            abstract=abstract,
            year=data.get("year"),
            doi=doi,
            url=data.get("url", ""),
            source=self.name,
            citations_count=data.get("citationCount", 0),
            keywords=keywords,
            journal=journal,
            metadata={"s2_paper_id": data.get("paperId", "")},
        )

    async def close(self) -> None:
        await self._client.aclose()
