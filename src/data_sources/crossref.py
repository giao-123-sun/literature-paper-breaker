"""CrossRef data source connector.

CrossRef is a DOI registration agency providing metadata for scholarly works.
Free API, no key required. Polite pool available with email.

API docs: https://api.crossref.org/swagger-ui/index.html
"""

from __future__ import annotations

import os
from typing import Any

import httpx

from .base import DataSource, Discipline, Paper, SearchResult

BASE_URL = "https://api.crossref.org"


class CrossRefSource(DataSource):
    """CrossRef metadata source.

    Excellent for DOI resolution and journal article metadata.
    Free, polite pool with email for better rate limits.
    """

    name = "crossref"
    supports_full_text = False
    supports_citations = False
    requires_auth = False
    supported_languages = ["en", "zh", "fr", "de", "es", "ja"]

    def __init__(self, email: str | None = None):
        self.email = email or os.environ.get("OPENALEX_EMAIL", "")
        headers = {"User-Agent": f"LiteraturePaperBreaker/0.1 (mailto:{self.email})"}
        self._client = httpx.AsyncClient(
            base_url=BASE_URL, timeout=30.0, headers=headers
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
            "query": query,
            "rows": min(limit, 100),
            "offset": (page - 1) * limit,
            "sort": "relevance",
            "order": "desc",
        }

        filters = []
        if year_from:
            filters.append(f"from-pub-date:{year_from}")
        if year_to:
            filters.append(f"until-pub-date:{year_to}")
        if filters:
            params["filter"] = ",".join(filters)

        resp = await self._client.get("/works", params=params)
        resp.raise_for_status()
        data = resp.json()

        message = data.get("message", {})
        items = message.get("items", [])
        total = message.get("total-results", 0)

        papers = [self._parse_item(item) for item in items]

        return SearchResult(
            papers=papers,
            total_count=total,
            query=query,
            source_name=self.name,
            page=page,
            has_more=(page * limit) < total,
        )

    async def get_paper(self, identifier: str) -> Paper | None:
        try:
            resp = await self._client.get(f"/works/{identifier}")
            resp.raise_for_status()
            data = resp.json()
            return self._parse_item(data.get("message", {}))
        except httpx.HTTPStatusError:
            return None

    def _parse_item(self, item: dict[str, Any]) -> Paper:
        authors = []
        for author in item.get("author", []):
            given = author.get("given", "")
            family = author.get("family", "")
            if given and family:
                authors.append(f"{given} {family}")
            elif family:
                authors.append(family)

        title_list = item.get("title", [])
        title = title_list[0] if title_list else ""

        abstract = item.get("abstract", "")
        if abstract:
            # CrossRef abstracts often have JATS XML tags
            import re
            abstract = re.sub(r"<[^>]+>", "", abstract).strip()

        year = None
        published = item.get("published", {}) or item.get("published-print", {})
        if published:
            date_parts = published.get("date-parts", [[]])
            if date_parts and date_parts[0]:
                year = date_parts[0][0]

        journal_list = item.get("container-title", [])
        journal = journal_list[0] if journal_list else ""

        doi = item.get("DOI", "")

        return Paper(
            title=title,
            authors=authors,
            abstract=abstract,
            year=year,
            doi=doi,
            url=f"https://doi.org/{doi}" if doi else "",
            source=self.name,
            citations_count=item.get("is-referenced-by-count", 0),
            journal=journal,
            language=item.get("language", "en"),
            metadata={"crossref_type": item.get("type", "")},
        )

    async def close(self) -> None:
        await self._client.aclose()
