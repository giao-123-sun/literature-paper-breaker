"""OpenAlex data source connector.

OpenAlex is a free, open catalog of the world's scholarly works, authors,
institutions, and more. It is the successor to Microsoft Academic Graph.

API docs: https://docs.openalex.org/
"""

from __future__ import annotations

import os
from typing import Any

import httpx

from .base import DataSource, Discipline, Paper, SearchResult

# OpenAlex concept IDs for humanities/social science disciplines
DISCIPLINE_CONCEPTS: dict[Discipline, str] = {
    Discipline.ECONOMICS: "C162324750",
    Discipline.HISTORY: "C95457728",
    Discipline.POLITICAL_SCIENCE: "C17744445",
    Discipline.SOCIOLOGY: "C144024400",
    Discipline.PHILOSOPHY: "C138885662",
    Discipline.LITERATURE: "C127313418",
    Discipline.LINGUISTICS: "C41008148",
    Discipline.ANTHROPOLOGY: "C15744967",
    Discipline.LAW: "C111472728",
    Discipline.EDUCATION: "C15744967",
    Discipline.PSYCHOLOGY: "C15744967",
    Discipline.ART_HISTORY: "C1862650",
}

BASE_URL = "https://api.openalex.org"


class OpenAlexSource(DataSource):
    """OpenAlex academic data source.

    Free, no API key required. Email recommended for polite pool (faster rate limits).
    """

    name = "openalex"
    supports_full_text = False
    supports_citations = True
    requires_auth = False
    supported_languages = ["en", "zh", "fr", "de", "es", "ja", "ko", "ar", "ru"]

    def __init__(self, email: str | None = None):
        self.email = email or os.environ.get("OPENALEX_EMAIL")
        self._client = httpx.AsyncClient(
            base_url=BASE_URL,
            timeout=30.0,
            headers={"User-Agent": f"LiteraturePaperBreaker/0.1 (mailto:{self.email})"}
            if self.email
            else {},
        )

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
            "search": query,
            "per_page": min(limit, 200),
            "page": page,
        }

        if self.email:
            params["mailto"] = self.email

        filters = []
        if discipline and discipline in DISCIPLINE_CONCEPTS:
            filters.append(f"concepts.id:{DISCIPLINE_CONCEPTS[discipline]}")
        if year_from:
            filters.append(f"publication_year:>{year_from - 1}")
        if year_to:
            filters.append(f"publication_year:<{year_to + 1}")
        if language:
            filters.append(f"language:{language}")
        if filters:
            params["filter"] = ",".join(filters)

        resp = await self._client.get("/works", params=params)
        resp.raise_for_status()
        data = resp.json()

        papers = [self._parse_work(w) for w in data.get("results", [])]
        total = data.get("meta", {}).get("count", 0)

        return SearchResult(
            papers=papers,
            total_count=total,
            query=query,
            source_name=self.name,
            page=page,
            has_more=page * limit < total,
        )

    async def get_paper(self, identifier: str) -> Paper | None:
        if identifier.startswith("10."):
            url = f"/works/doi:{identifier}"
        elif identifier.startswith("W"):
            url = f"/works/{identifier}"
        else:
            url = f"/works/{identifier}"

        try:
            resp = await self._client.get(url)
            resp.raise_for_status()
            return self._parse_work(resp.json())
        except httpx.HTTPStatusError:
            return None

    async def get_references(self, paper: Paper) -> list[Paper]:
        openalex_id = paper.metadata.get("openalex_id")
        if not openalex_id:
            return []
        resp = await self._client.get(
            "/works",
            params={"filter": f"cited_by:{openalex_id}", "per_page": 50},
        )
        resp.raise_for_status()
        return [self._parse_work(w) for w in resp.json().get("results", [])]

    async def get_citations(self, paper: Paper) -> list[Paper]:
        openalex_id = paper.metadata.get("openalex_id")
        if not openalex_id:
            return []
        resp = await self._client.get(
            "/works",
            params={"filter": f"cites:{openalex_id}", "per_page": 50},
        )
        resp.raise_for_status()
        return [self._parse_work(w) for w in resp.json().get("results", [])]

    def _parse_work(self, work: dict[str, Any]) -> Paper:
        authors = []
        for authorship in work.get("authorships", []):
            author = authorship.get("author", {})
            name = author.get("display_name", "")
            if name:
                authors.append(name)

        doi = work.get("doi", "")
        if doi and doi.startswith("https://doi.org/"):
            doi = doi[len("https://doi.org/"):]

        keywords = []
        for concept in work.get("concepts", []):
            if concept.get("score", 0) > 0.3:
                keywords.append(concept.get("display_name", ""))
        for kw in work.get("keywords", []):
            keywords.append(kw.get("keyword", "") if isinstance(kw, dict) else str(kw))

        abstract = ""
        inverted_abstract = work.get("abstract_inverted_index")
        if inverted_abstract:
            abstract = self._reconstruct_abstract(inverted_abstract)

        oa = work.get("open_access", {})
        url = oa.get("oa_url") or work.get("id", "")

        journal = ""
        primary_location = work.get("primary_location", {})
        if primary_location:
            source = primary_location.get("source", {})
            if source:
                journal = source.get("display_name", "")

        return Paper(
            title=work.get("display_name", work.get("title", "")),
            authors=authors,
            abstract=abstract,
            year=work.get("publication_year"),
            doi=doi,
            url=url,
            source=self.name,
            citations_count=work.get("cited_by_count", 0),
            keywords=keywords,
            journal=journal,
            language=work.get("language", "en"),
            metadata={"openalex_id": work.get("id", "")},
        )

    @staticmethod
    def _reconstruct_abstract(inverted_index: dict[str, list[int]]) -> str:
        if not inverted_index:
            return ""
        word_positions: list[tuple[int, str]] = []
        for word, positions in inverted_index.items():
            for pos in positions:
                word_positions.append((pos, word))
        word_positions.sort(key=lambda x: x[0])
        return " ".join(w for _, w in word_positions)

    async def close(self) -> None:
        await self._client.aclose()
