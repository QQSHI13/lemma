"""
Lemma - Markdown extension for math wiki cross-references + math environments.

Adds:
  [[ref:Page Title]]   → Link to another page by title
  [[thm:label]]         → Reference a labeled theorem
  [[eq:label]]          → Reference a labeled equation
  {#thm:label}          → Attach a label to a theorem block
  [@citation-key]       → Citation reference
  :::theorem {#label}   → Theorem environment (styled admonition)
  :::proof              → Proof environment
  :::definition {#label}→ Definition environment
  :::lemma {#label}     → Lemma environment
  :::corollary {#label} → Corollary environment
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from markdown import Markdown
from markdown.inlinepatterns import InlineProcessor
from markdown.extensions import Extension
from typing import Match

# ===== Inline patterns =====

REF_PATTERN = r'\[\[ref:(.+?)\]\]'
LABEL_REF_PATTERN = r'\[\[(thm|eq|def|lem|cor):([a-zA-Z0-9_-]+)\]\]'
CITE_PATTERN = r'\[@([a-zA-Z0-9_-]+)\]'

# Math environment colors
ENV_COLORS = {
    'theorem':  'border-left: 4px solid #e74c3c; background: #fdf2f2;',  # red
    'proof':    'border-left: 4px solid #7f8c8d; background: #f8f9fa;',  # gray
    'definition': 'border-left: 4px solid #2ecc71; background: #f0faf4;', # green
    'lemma':    'border-left: 4px solid #3498db; background: #f0f7ff;',  # blue
    'corollary':'border-left: 4px solid #9b59b6; background: #f5f0fa;',  # purple
}

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
        kind = m.group(1)
        label = m.group(2)
        el = ET.Element(f'lemma-{kind}-ref')
        el.set('label', label)
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


class LemmaMathExtension(Extension):
    """Markdown extension adding lemma cross-reference syntax + math environments."""

    def extendMarkdown(self, md: Markdown) -> None:
        # Register postprocessor for ::: environments FIRST (runs before HTML output)

        # Register inline patterns
        md.inlinePatterns.register(RefInlineProcessor(REF_PATTERN, md), 'lemma-ref', 175)
        md.inlinePatterns.register(LabelRefProcessor(LABEL_REF_PATTERN, md), 'lemma-label-ref', 174)
        md.inlinePatterns.register(CiteProcessor(CITE_PATTERN, md), 'lemma-cite', 173)


def makeExtension(**kwargs) -> LemmaMathExtension:
    return LemmaMathExtension(**kwargs)