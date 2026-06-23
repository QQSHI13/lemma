"""
Lemma - Markdown extension for math wiki cross-references.

Adds:
  [[ref:Page Title]]   → Link to another page by title
  [[thm:label]]         → Reference a labeled theorem
  [[eq:label]]          → Reference a labeled equation
  {#thm:label}          → Attach a label to a theorem block
  {#eq:label}           → Attach a label to an equation
  [@citation-key]       → Citation reference

This extension runs during markdown->HTML conversion.
It emits placeholder HTML that the build script later resolves.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from markdown import Markdown
from markdown.inlinepatterns import InlineProcessor
from markdown.postprocessors import Postprocessor
from markdown.extensions import Extension
from typing import Match

# ===== Inline patterns =====

# [[ref:Page Title or slug]]
REF_PATTERN = r'\[\[ref:(.+?)\]\]'

# [[thm:label]] or [[eq:label]]
LABEL_REF_PATTERN = r'\[\[(thm|eq|def|lem|cor):([a-zA-Z0-9_-]+)\]\]'

# [@citation-key]
CITE_PATTERN = r'\[@([a-zA-Z0-9_-]+)\]'


class RefInlineProcessor(InlineProcessor):
    """Handle [[ref:Page Title]] → placeholder link."""

    def handleMatch(self, m: Match, data: str) -> tuple[ET.Element | str, int, int]:
        target = m.group(1).strip()
        el = ET.Element('lemma-ref')
        el.set('target', target)
        el.text = target
        return el, m.start(), m.end()


class LabelRefProcessor(InlineProcessor):
    """Handle [[thm:label]] / [[eq:label]] → placeholder label reference."""

    def handleMatch(self, m: Match, data: str) -> tuple[ET.Element | str, int, int]:
        kind = m.group(1)   # thm, eq, def, lem, cor
        label = m.group(2)
        el = ET.Element(f'lemma-{kind}-ref')
        el.set('label', label)
        # Display as "Theorem ?" — the build script will fill in the number
        label_names = {'thm': 'Theorem', 'eq': 'Equation', 'def': 'Definition',
                       'lem': 'Lemma', 'cor': 'Corollary'}
        name = label_names.get(kind, kind)
        el.text = f'{name} ?'
        return el, m.start(), m.end()


class CiteProcessor(InlineProcessor):
    """Handle [@citation-key] → citation reference."""

    def handleMatch(self, m: Match, data: str) -> tuple[ET.Element | str, int, int]:
        key = m.group(1)
        el = ET.Element('lemma-cite')
        el.set('key', key)
        el.text = f'[{key}]'
        return el, m.start(), m.end()


# ===== Label extraction from blocks =====

# Labels on display math: $$ ... $$ {#eq:label}
EQ_LABEL_PATTERN = re.compile(r'\$\$\s*(.*?)\s*\$\$\s*\{#(eq|thm|def|lem|cor):([a-zA-Z0-9_-]+)\}', re.DOTALL)

# Labels on admonitions (theorem/proof blocks)
# These are handled by the admonition parser if needed.
ADMON_LABEL_PATTERN = re.compile(r'\{#(thm|def|lem|cor):([a-zA-Z0-9_-]+)\}')


class LemmaLabelPreprocessor:
    """Extract labels from content before markdown processing."""
    pass


class LemmaMathExtension(Extension):
    """Markdown extension that adds lemma cross-reference syntax."""

    def extendMarkdown(self, md: Markdown) -> None:
        md.inlinePatterns.register(RefInlineProcessor(REF_PATTERN, md), 'lemma-ref', 175)
        md.inlinePatterns.register(LabelRefProcessor(LABEL_REF_PATTERN, md), 'lemma-label-ref', 174)
        md.inlinePatterns.register(CiteProcessor(CITE_PATTERN, md), 'lemma-cite', 173)


def makeExtension(**kwargs) -> LemmaMathExtension:
    return LemmaMathExtension(**kwargs)