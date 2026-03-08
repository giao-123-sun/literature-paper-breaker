"""CORE (core.ac.uk) data source connector.

CORE aggregates open access research papers from repositories and journals worldwide.
It provides free API access with an API key.

API docs: https://core.ac.uk/documentation/api
"""

from __future__ import annotations

import os
from typing import Any

import httpx

from .base import DataSource, Discipline, Paper, SearchResult

BASE_URL = "https://api.core.ac.uk/v3"


class CoreSource(DataSource):
    """CORE open access aggregator.

    Provides access to millions of open access papers with full text.
    Free API key required from core.ac.uk.
    """

    name = "core"
    supports_full_text = True
    supports_citations = False
    requires_auth = True
    supported_languages = ["en", "fr", "de", "es", "zh"]

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("CORE_API_KEY", "")
        self._client = httpx.AsyncClient(
            base_url=BASE_URL,
            timeout=30.0,
            headers={"Authorization": f"Bearer {self.api_key}"} if self.api_key else {},
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
        if not self.api_key:
            return SearchResult(
                papers=[], total_count=0, query=query,
                source_name=self.name, page=page, has_more=False,
            )

        body: dict[str, Any] = {
            "q": query,
            "limit": min(limit, 100),
            "offset": (page - 1) * limit,
        }

        if year_from or year_to:
            body["q"] += f" AND yearPublished>={year_from or 1900}"
            if year_to:
                body["q"] += f" AND yearPublished<={year_to}"

        resp = await self._client.post("/search/works", json=body)
        resp.raise_for_status()
        data = resp.json()

        results = data.get("results", [])
        total = data.get("totalHits", 0)
        papers = [self._parse_work(w) for w in results]

        return SearchResult(
            papers=papers,
            total_count=total,
            query=query,
            source_name=self.name,
            page=page,
            has_more=(page * limit) < total,
        )

    async def get_paper(self, identifier: str) -> Paper | None:
        if not self.api_key:
            return None
        try:
            resp = await self._client.get(f"/works/{identifier}")
            resp.raise_for_status()
            return self._parse_work(resp.json())
        except httpx.HTTPStatusError:
            return None

    async def get_full_text(self, paper: Paper) -> str | None:
        core_id = paper.metadata.get("core_id")
        if not core_id or not self.api_key:
            return None
        try:
            resp = await self._client.get(f"/works/{core_id}")
            resp.raise_for_status()
            data = resp.json()
            return data.get("fullText")
        except httpx.HTTPStatusError:
            return None

    def _parse_work(self, work: dict[str, Any]) -> Paper:
        authors = []
        for author in work.get("authors", []):
            if isinstance(author, dict):
                authors.append(author.get("name", ""))
            elif isinstance(author, str):
                authors.append(author)

        doi = None
        for ident in work.get("identifiers", []):
            if isinstance(ident, str) and ident.startswith("10."):
                doi = ident
                break

        return Paper(
            title=work.get("title", ""),
            authors=authors,
            abstract=work.get("abstract", "") or "",
            year=work.get("yearPublished"),
            doi=doi,
            url=work.get("downloadUrl", "") or work.get("sourceFulltextUrls", [""])[0] if work.get("sourceFulltextUrls") else "",
            source=self.name,
            full_text=work.get("fullText"),
            journal=work.get("publisher", ""),
            language=work.get("language", {}).get("code", "en") if isinstance(work.get("language"), dict) else "en",
            metadata={"core_id": str(work.get("id", ""))},
        )

    async def close(self) -> None:
        await self._client.aclose()
