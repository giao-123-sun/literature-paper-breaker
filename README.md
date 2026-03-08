# Literature Paper Breaker (LPB)

AI-powered humanities & social science research automation system.

LPB automates the full academic research pipeline — from literature search and systematic review, through gap analysis and hypothesis generation, to paper drafting — specifically designed for humanities and social sciences (economics, history, political science, sociology, philosophy, linguistics, etc.).

## What It Does

```
Research Topic → Literature Search → Systematic Review → Gap Analysis → Research Proposals → Paper Draft
```

### Pipeline Stages

1. **Literature Search** — Parallel search across OpenAlex, Semantic Scholar, CrossRef, CORE, and CText (Chinese classics). Results are deduplicated and ranked by relevance.

2. **Systematic Literature Review** — LLM-powered analysis that identifies themes, maps research trajectories, and generates a structured review with proper citations.

3. **Gap Analysis** — Identifies theoretical blind spots, methodological limitations, contradictory findings, and under-explored areas.

4. **Hypothesis/Question Generation** — Proposes original research questions (humanities) or testable hypotheses (social science) grounded in the literature.

5. **Paper Drafting** — Generates a structured academic paper with sections written sequentially for coherence, proper citations, and export to Markdown or LaTeX.

## Quick Start

```bash
# Install
pip install -e ".[llm]"

# Set your API key
export ANTHROPIC_API_KEY=sk-ant-...
# or
export OPENAI_API_KEY=sk-...

# Run full pipeline
lpb research "The impact of digital transformation on rural governance in China" \
  --discipline economics \
  --language zh \
  --depth standard

# Run literature review only
lpb review "Confucian ethics in modern corporate governance" \
  --discipline philosophy

# Search academic databases
lpb search "digital humanities methodology" -n 20

# List available data sources
lpb sources
```

## Data Sources

| Source | Type | Auth | Full Text | Citations | Cost |
|--------|------|------|-----------|-----------|------|
| OpenAlex | Open catalog (240M+ works) | No | No | Yes | Free |
| Semantic Scholar | AI-powered search | No* | No | Yes | Free |
| CrossRef | DOI metadata | No | No | No | Free |
| CORE | Open access aggregator | API key | Yes | No | Free |
| CText | Chinese classical texts | No | Yes | No | Free |

\* API key available for higher rate limits

### Bring Your Own Credentials

For institutional databases (CNKI, JSTOR, Web of Science), set credentials in `.env`:

```bash
cp .env.example .env
# Edit .env with your institutional credentials
```

## Configuration

### CLI Options

```
lpb research TOPIC [OPTIONS]

Options:
  -d, --discipline       Academic discipline (economics, history, political_science, ...)
  -l, --language         Language code (en, zh, fr, de, ...)
  -yf, --year-from       Start year filter
  -yt, --year-to         End year filter
  -n, --max-papers       Max papers to analyze (default: 50)
  --depth                Review depth: quick|standard|deep
  --paper-type           research_article|review|essay|commentary
  --discipline-type      humanities (interpretive) | social_science (hypothesis-driven)
  -w, --target-words     Target paper length (default: 8000)
  -o, --output-dir       Output directory (default: output/)
  --format               Output format: markdown|latex
  --provider             LLM provider: anthropic|openai
  --model                LLM model name
  --sources              Comma-separated data sources
```

### YAML Config

```yaml
# config/local.yaml
research:
  depth: deep
  max_papers: 60
  language: zh
llm:
  provider: anthropic
  model: claude-sonnet-4-20250514
sources:
  - openalex
  - semantic_scholar
  - crossref
  - ctext
```

## Output Structure

```
output/
├── literature_review.md    # Systematic literature review
├── gap_analysis.md         # Research gaps and opportunities
├── proposals.md            # Generated research proposals
├── paper.md                # Full paper draft (or paper.tex)
├── references.json         # Structured references
└── timeline.json           # Research development timeline
```

## Programmatic Usage

```python
import asyncio
from src.data_sources.base import Discipline
from src.pipeline.orchestrator import ResearchConfig, ResearchOrchestrator

async def main():
    config = ResearchConfig(
        topic="认知语言学中的隐喻理论演变",
        discipline=Discipline.LINGUISTICS,
        language="zh",
        depth="deep",
        max_papers=60,
        discipline_type="humanities",
    )

    orchestrator = ResearchOrchestrator(config)
    session = await orchestrator.run_full_pipeline()

    print(f"Papers: {len(session.review_result.papers)}")
    print(f"Gaps: {len(session.gap_result.gaps)}")
    print(session.draft.to_markdown())

asyncio.run(main())
```

## Architecture

```
src/
├── data_sources/           # Academic database connectors
│   ├── base.py             # DataSource ABC, Paper model
│   ├── openalex.py         # OpenAlex (free, 240M+ works)
│   ├── semantic_scholar.py # Semantic Scholar (AI-powered)
│   ├── crossref.py         # CrossRef (DOI metadata)
│   ├── core_ac.py          # CORE (open access full text)
│   ├── ctext.py            # Chinese Text Project (classical texts)
│   └── aggregator.py       # Multi-source search & dedup
├── pipeline/               # Research pipeline
│   ├── literature_review.py # Systematic review generation
│   ├── gap_analyzer.py     # Research gap identification
│   ├── hypothesis_generator.py # Question/hypothesis generation
│   └── orchestrator.py     # Pipeline orchestration
├── paper_engine/           # Paper writing
│   ├── outliner.py         # Structured outline generation
│   └── writer.py           # Section-by-section writing
├── utils/
│   └── llm.py              # LLM provider abstraction
└── cli.py                  # CLI interface
```

## Key Design Decisions

1. **Humanities-first**: Unlike AI Scientist (ML-focused) or Karpathy's AutoResearch (experiment-driven), LPB is designed for text-based, interpretive, and argumentative research.

2. **Multi-source aggregation**: Searches across multiple academic databases in parallel, deduplicates, and ranks results.

3. **Discipline-aware**: Supports both hypothesis-driven (social science) and interpretive (humanities) research paradigms.

4. **Citation integrity**: Only cites papers that were actually found and analyzed. Never fabricates references.

5. **Multilingual**: First-class support for Chinese-language research, including classical text databases.

6. **Bring Your Own Credentials**: Users can provide their own institutional database access for premium sources.

## Supported Disciplines

Economics, History, Political Science, Sociology, Philosophy, Literature, Linguistics, Anthropology, Law, Education, Psychology, Art History, Religious Studies, Area Studies

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check src/
```

## License

MIT
