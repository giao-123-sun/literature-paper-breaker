"""Base classes for academic data source connectors."""

from __future__ import annotations

import abc
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class Discipline(str, Enum):
    """Humanities and social science disciplines."""

    ECONOMICS = "economics"
    HISTORY = "history"
    POLITICAL_SCIENCE = "political_science"
    SOCIOLOGY = "sociology"
    PHILOSOPHY = "philosophy"
    LITERATURE = "literature"
    LINGUISTICS = "linguistics"
    ANTHROPOLOGY = "anthropology"
    LAW = "law"
    EDUCATION = "education"
    PSYCHOLOGY = "psychology"
    ART_HISTORY = "art_history"
    RELIGIOUS_STUDIES = "religious_studies"
    AREA_STUDIES = "area_studies"
    GENERAL = "general"


@dataclass
class Paper:
    """Represents an academic paper or text."""

    title: str
    authors: list[str] = field(default_factory=list)
    abstract: str = ""
    year: int | None = None
    doi: str | None = None
    url: str | None = None
    source: str = ""
    full_text: str | None = None
    citations_count: int = 0
    references: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    journal: str = ""
    discipline: Discipline = Discipline.GENERAL
    language: str = "en"
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def citation_key(self) -> str:
        first_author = self.authors[0].split()[-1] if self.authors else "Unknown"
        return f"{first_author}{self.year or 'nd'}"

    def to_citation(self, style: str = "apa") -> str:
        authors_str = ", ".join(self.authors) if self.authors else "Unknown"
        year_str = str(self.year) if self.year else "n.d."
        if style == "apa":
            base = f"{authors_str} ({year_str}). {self.title}."
            if self.journal:
                base += f" *{self.journal}*."
            if self.doi:
                base += f" https://doi.org/{self.doi}"
            return base
        elif style == "chicago":
            base = f"{authors_str}. \"{self.title}.\""
            if self.journal:
                base += f" *{self.journal}*"
            if self.year:
                base += f" ({year_str})."
            if self.doi:
                base += f" https://doi.org/{self.doi}"
            return base
        return f"{authors_str} ({year_str}). {self.title}."


@dataclass
class SearchResult:
    """A collection of search results from a data source."""

    papers: list[Paper] = field(default_factory=list)
    total_count: int = 0
    query: str = ""
    source_name: str = ""
    page: int = 1
    has_more: bool = False


class DataSource(abc.ABC):
    """Abstract base class for academic data source connectors."""

    name: str = "base"
    supports_full_text: bool = False
    supports_citations: bool = False
    requires_auth: bool = False
    supported_languages: list[str] = ["en"]

    @abc.abstractmethod
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
        """Search for papers matching query."""
        ...

    @abc.abstractmethod
    async def get_paper(self, identifier: str) -> Paper | None:
        """Get a specific paper by DOI or other identifier."""
        ...

    async def get_references(self, paper: Paper) -> list[Paper]:
        """Get papers referenced by the given paper."""
        return []

    async def get_citations(self, paper: Paper) -> list[Paper]:
        """Get papers that cite the given paper."""
        return []

    async def get_full_text(self, paper: Paper) -> str | None:
        """Attempt to retrieve full text of a paper."""
        return None

    async def close(self) -> None:
        """Clean up resources."""
        pass
