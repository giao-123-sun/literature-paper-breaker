"""Data source connectors for academic databases and archives."""

from .base import DataSource, Paper, SearchResult
from .openalex import OpenAlexSource
from .semantic_scholar import SemanticScholarSource
from .crossref import CrossRefSource
from .ctext import CTextSource
from .core_ac import CoreSource

__all__ = [
    "DataSource",
    "Paper",
    "SearchResult",
    "OpenAlexSource",
    "SemanticScholarSource",
    "CrossRefSource",
    "CTextSource",
    "CoreSource",
]
