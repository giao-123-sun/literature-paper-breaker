"""Chinese Text Project (CText) data source connector.

CText (ctext.org) is an open-access digital library of pre-modern Chinese texts.
It provides API access to classical Chinese texts with translations.

API docs: https://ctext.org/tools/api
"""

from __future__ import annotations

from typing import Any

import httpx

from .base import DataSource, Discipline, Paper, SearchResult

BASE_URL = "https://api.ctext.org"


class CTextSource(DataSource):
    """Chinese Text Project data source.

    Provides access to pre-modern Chinese texts (classics, philosophy, history).
    Free API access with rate limits.
    """

    name = "ctext"
    supports_full_text = True
    supports_citations = False
    requires_auth = False
    supported_languages = ["zh", "en"]

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key
        self._client = httpx.AsyncClient(base_url=BASE_URL, timeout=30.0)

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
        """Search Chinese classical texts.

        Note: CText search is primarily text-based (searching within texts),
        not paper-based like academic databases.
        """
        params: dict[str, Any] = {
            "if": "en",  # interface language
            "remap": "gb",
        }

        if self.api_key:
            params["apikey"] = self.api_key

        # CText uses a different search paradigm - search within texts
        resp = await self._client.get(
            "/searchtexts",
            params={**params, "title": query},
        )

        if resp.status_code != 200:
            return SearchResult(
                papers=[], total_count=0, query=query,
                source_name=self.name, page=page, has_more=False,
            )

        data = resp.json()
        papers = []

        for item in data if isinstance(data, list) else [data]:
            if isinstance(item, dict):
                paper = Paper(
                    title=item.get("title", query),
                    authors=[item.get("author", "Unknown")],
                    abstract=item.get("introduction", ""),
                    source=self.name,
                    url=item.get("url", f"https://ctext.org/{query}"),
                    language="zh",
                    discipline=Discipline.HISTORY,
                    full_text=item.get("fulltext", None),
                    metadata={
                        "ctext_urn": item.get("urn", ""),
                        "dynasty": item.get("dynasty", ""),
                        "category": item.get("category", ""),
                    },
                )
                papers.append(paper)

        return SearchResult(
            papers=papers[:limit],
            total_count=len(papers),
            query=query,
            source_name=self.name,
            page=page,
            has_more=False,
        )

    async def get_paper(self, identifier: str) -> Paper | None:
        """Get a text by its CText URN."""
        params: dict[str, Any] = {"if": "en", "remap": "gb"}
        if self.api_key:
            params["apikey"] = self.api_key

        try:
            resp = await self._client.get(
                "/gettext", params={**params, "urn": identifier}
            )
            resp.raise_for_status()
            data = resp.json()

            fulltext = ""
            if isinstance(data, list):
                fulltext = "\n".join(
                    item.get("text", "") for item in data if isinstance(item, dict)
                )

            return Paper(
                title=identifier,
                source=self.name,
                language="zh",
                full_text=fulltext,
                metadata={"ctext_urn": identifier},
            )
        except httpx.HTTPStatusError:
            return None

    async def get_full_text(self, paper: Paper) -> str | None:
        urn = paper.metadata.get("ctext_urn")
        if not urn:
            return None
        result = await self.get_paper(urn)
        return result.full_text if result else None

    async def close(self) -> None:
        await self._client.aclose()
