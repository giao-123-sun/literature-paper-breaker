"""Paper writing engine.

Generates full academic papers section by section,
with proper citations and academic style.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field

from ..data_sources.base import Paper
from ..utils.llm import LLMClient
from .outliner import PaperOutline, Section

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """\
You are a world-class academic writer in the humanities and social sciences.
Your writing is characterized by:
- Crystal-clear argumentation
- Sophisticated but accessible prose
- Rigorous engagement with sources
- Original analytical insights
- Appropriate disciplinary conventions

Rules:
- ONLY cite papers that were provided to you. NEVER fabricate citations.
- Use [AuthorYear] citation format in-text.
- Build arguments logically, with each paragraph advancing the thesis.
- Maintain academic register without being obscure.
- Show, don't just tell - use evidence and examples.
- Acknowledge counter-arguments and limitations.

Write in the same language as the outline and topic."""


@dataclass
class PaperDraft:
    """A complete paper draft."""

    title: str
    abstract: str = ""
    sections: list[dict] = field(default_factory=list)  # {title, content}
    references: list[str] = field(default_factory=list)
    word_count: int = 0
    full_text: str = ""

    def to_markdown(self) -> str:
        """Export the draft as markdown."""
        lines = [f"# {self.title}\n"]
        if self.abstract:
            lines.append(f"**Abstract:** {self.abstract}\n")

        for section in self.sections:
            level = section.get("level", 2)
            prefix = "#" * level
            lines.append(f"\n{prefix} {section['title']}\n")
            lines.append(section.get("content", ""))

        if self.references:
            lines.append("\n## References\n")
            for ref in self.references:
                lines.append(f"- {ref}")

        return "\n".join(lines)

    def to_latex(self) -> str:
        """Export the draft as LaTeX."""
        lines = [
            "\\documentclass[12pt]{article}",
            "\\usepackage[utf8]{inputenc}",
            "\\usepackage{natbib}",
            "\\usepackage{hyperref}",
            "",
            f"\\title{{{self.title}}}",
            "\\date{\\today}",
            "",
            "\\begin{document}",
            "\\maketitle",
            "",
        ]

        if self.abstract:
            lines.extend([
                "\\begin{abstract}",
                self.abstract,
                "\\end{abstract}",
                "",
            ])

        section_cmds = {2: "\\section", 3: "\\subsection", 4: "\\subsubsection"}
        for section in self.sections:
            level = section.get("level", 2)
            cmd = section_cmds.get(level, "\\section")
            lines.append(f"\n{cmd}{{{section['title']}}}")
            lines.append(section.get("content", ""))

        if self.references:
            lines.extend([
                "",
                "\\begin{thebibliography}{99}",
            ])
            for ref in self.references:
                lines.append(f"\\bibitem{{{ref[:20]}}} {ref}")
            lines.append("\\end{thebibliography}")

        lines.append("\\end{document}")
        return "\n".join(lines)


class PaperWriter:
    """Writes academic papers section by section."""

    def __init__(self, llm: LLMClient):
        self.llm = llm

    async def write(
        self,
        outline: PaperOutline,
        papers: list[Paper],
        *,
        style: str = "analytical",  # analytical, argumentative, descriptive, comparative
    ) -> PaperDraft:
        """Write a complete paper from an outline.

        Args:
            outline: Paper outline with sections
            papers: Reference papers to cite
            style: Writing style
        """
        draft = PaperDraft(title=outline.title)

        # Write abstract
        draft.abstract = await self._write_abstract(outline, papers)

        # Write each section
        context_so_far = ""
        for section in outline.sections:
            section_content = await self._write_section(
                section, outline, papers, context_so_far, style
            )
            draft.sections.append(section_content)
            context_so_far += f"\n\n## {section_content['title']}\n{section_content['content']}"

        # Generate references list
        draft.references = self._generate_references(papers)

        # Calculate word count
        draft.full_text = draft.to_markdown()
        draft.word_count = len(draft.full_text.split())

        return draft

    async def _write_abstract(
        self, outline: PaperOutline, papers: list[Paper]
    ) -> str:
        prompt = f"""Write an academic abstract (200-300 words) for a paper titled:
"{outline.title}"

Outline:
{self._format_outline_brief(outline)}

The abstract should cover:
1. Research question/problem
2. Methodology/approach
3. Key findings/arguments
4. Significance/contribution

Draft abstract (if available): {outline.abstract_draft}"""

        return await self.llm.generate(
            prompt, system=SYSTEM_PROMPT, max_tokens=1024
        )

    async def _write_section(
        self,
        section: Section,
        outline: PaperOutline,
        papers: list[Paper],
        context: str,
        style: str,
    ) -> dict:
        """Write a single section."""
        refs = self._format_refs_for_section(papers, section.citations_needed)

        prompt = f"""Paper title: "{outline.title}"
Writing style: {style}

You are writing the section: "{section.title}"
Description: {section.description}
Target length: ~{section.estimated_words} words

Key points to cover:
{chr(10).join(f"- {p}" for p in section.key_points)}

Available references for this section:
{refs}

{"Previous sections (for context/continuity):" + context[-3000:] if context else "This is the first section."}

Write this section now. Use proper academic prose with in-text citations [AuthorYear].
Only cite papers from the provided references. Build a coherent argument."""

        content = await self.llm.generate(
            prompt,
            system=SYSTEM_PROMPT,
            max_tokens=max(2048, section.estimated_words * 2),
        )

        result = {"title": section.title, "content": content, "level": 2}

        # Write subsections if any
        if section.subsections:
            sub_context = content
            for sub in section.subsections:
                sub_content = await self._write_subsection(
                    sub, section, outline, papers, sub_context, style
                )
                result["content"] += f"\n\n### {sub.title}\n\n{sub_content}"
                sub_context += f"\n{sub_content}"

        return result

    async def _write_subsection(
        self,
        subsection: Section,
        parent: Section,
        outline: PaperOutline,
        papers: list[Paper],
        context: str,
        style: str,
    ) -> str:
        refs = self._format_refs_for_section(papers, subsection.citations_needed)

        prompt = f"""Paper: "{outline.title}"
Parent section: "{parent.title}"
Subsection: "{subsection.title}"
Description: {subsection.description}
Target: ~{subsection.estimated_words} words

Key points:
{chr(10).join(f"- {p}" for p in subsection.key_points)}

References:
{refs}

Context from parent section:
{context[-2000:]}

Write this subsection with academic rigor and proper citations."""

        return await self.llm.generate(
            prompt,
            system=SYSTEM_PROMPT,
            max_tokens=max(1024, subsection.estimated_words * 2),
        )

    async def revise(
        self, draft: PaperDraft, feedback: str
    ) -> PaperDraft:
        """Revise a draft based on feedback."""
        prompt = f"""Here is an academic paper draft:

{draft.full_text[:15000]}

Feedback for revision:
{feedback}

Please revise the paper addressing all feedback points.
Maintain the same structure but improve the content as directed.
Keep all existing valid citations."""

        revised_text = await self.llm.generate(
            prompt, system=SYSTEM_PROMPT, max_tokens=16384
        )

        # Parse revised text back into sections
        revised_draft = PaperDraft(title=draft.title)
        revised_draft.references = draft.references
        revised_draft.full_text = revised_text
        revised_draft.word_count = len(revised_text.split())

        # Simple section parsing from markdown
        current_section = {"title": "Body", "content": "", "level": 2}
        for line in revised_text.split("\n"):
            if line.startswith("## "):
                if current_section["content"].strip():
                    revised_draft.sections.append(current_section)
                current_section = {
                    "title": line[3:].strip(),
                    "content": "",
                    "level": 2,
                }
            elif line.startswith("### "):
                current_section["content"] += f"\n{line}\n"
            else:
                current_section["content"] += f"\n{line}"
        if current_section["content"].strip():
            revised_draft.sections.append(current_section)

        return revised_draft

    @staticmethod
    def _format_outline_brief(outline: PaperOutline) -> str:
        lines = []
        for s in outline.sections:
            lines.append(f"- {s.title}: {s.description}")
            for sub in s.subsections:
                lines.append(f"  - {sub.title}")
        return "\n".join(lines)

    @staticmethod
    def _format_refs_for_section(
        papers: list[Paper], citation_keys: list[str]
    ) -> str:
        lines = []
        for p in papers[:30]:
            first_author = p.authors[0].split()[-1] if p.authors else "Unknown"
            key = f"[{first_author}{p.year or 'nd'}]"
            authors = ", ".join(p.authors[:3])
            line = f"{key} {authors}. \"{p.title}\"."
            if p.journal:
                line += f" {p.journal}."
            if p.abstract:
                line += f" Summary: {p.abstract[:200]}"
            lines.append(line)
        return "\n".join(lines)

    @staticmethod
    def _generate_references(papers: list[Paper]) -> list[str]:
        refs = []
        for p in papers:
            refs.append(p.to_citation(style="apa"))
        return sorted(refs)
